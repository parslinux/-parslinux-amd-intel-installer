#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux Nvidia Installer - Main Window Controller
"""

import gi
import os
import signal
import subprocess
import sys
import locale
import platform

import nvidia
import package

gi.require_version("Gtk", "3.0")
gi.require_version("Polkit", "1.0")
gi.require_version("Vte", "2.91")

from gi.repository import Gtk, GObject, GLib, Vte, Gdk
from locale import gettext as _

APPNAME_CODE = "parslinux-nvidia-installer"
TRANSLATIONS_PATH = "/usr/share/locale/"
locale.bindtextdomain(APPNAME_CODE, TRANSLATIONS_PATH)
locale.bindtextdomain("pardus-nvidia-installer", TRANSLATIONS_PATH)
locale.textdomain(APPNAME_CODE)

act_id = "org.parslinux.pkexec.parslinux-nvidia-installer"
socket_path = "/tmp/parslinux-nvidia-installer"
nouveau = "xserver-xorg-video-nouveau"
driver_packages = {
    "nouveau": "xserver-xorg-video-nouveau",
    "current": "nvidia-driver",
    470: "nvidia-tesla-470-driver",
}
pkg_opr = {"purge": ""}

cur_path = os.path.dirname(os.path.abspath(__file__))


def get_package_exec_path():
    system_path = "/usr/share/parslinux/parslinux-nvidia-installer/src/package.py"
    if os.path.isfile(system_path):
        return system_path
    local_path = os.path.join(cur_path, "package.py")
    if os.path.isfile(local_path):
        return local_path
    return "/usr/share/pardus/pardus-nvidia-installer/src/package.py"


def check_is_reboot_pending():
    return (
        os.path.isfile("/run/parslinux-nvi.reboot")
        or os.path.isfile("/run/pardus-nvi.reboot")
    )


def get_system_gpu_description():
    try:
        out = subprocess.check_output(["lspci"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            line_lower = line.lower()
            if any(term in line_lower for term in ("vga compatible", "3d controller", "display controller")):
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
    except Exception:
        pass
    return "Intel / AMD Grafik Bağdaştırıcısı"


def apply_custom_css():
    try:
        css_provider = Gtk.CssProvider()
        css_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../data/style.css"))
        if os.path.isfile(css_path):
            css_provider.load_from_path(css_path)
            screen = Gdk.Screen.get_default()
            if screen:
                Gtk.StyleContext.add_provider_for_screen(
                    screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
    except Exception as e:
        print(f"Warning: Failed to load style.css: {e}", file=sys.stderr)


class MainWindow(object):
    def __init__(self, application):
        self.application = application
        self.ui_interface_file = os.path.join(os.path.dirname(__file__), "../ui/ui.glade")
        try:
            self.gtk_builder = Gtk.Builder.new_from_file(self.ui_interface_file)
            self.gtk_builder.connect_signals(self)
        except GLib.Error as e:
            print(
                f"Failed to load UI from {self.ui_interface_file}: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

        apply_custom_css()

        self.is_debug = nvidia.is_debug_mode()

        self.ui_confirm_dialog = self.get_ui("ui_confirm_dialog")
        self.get_ui("ui_button_reboot_dlg").connect("clicked", self.do_reboot)
        self.get_ui("ui_button_exit_dlg").connect(
            "clicked", lambda x: self.application.quit()
        )

        if check_is_reboot_pending():
            self.ui_main_window = self.get_ui("ui_window_reboot")
            self.ui_main_window.set_application(application)
            self.ui_main_window.show_all()
            return

        self.driver_buttons = []
        self.active_driver = ""
        self.toggled_driver = None
        self.drv_arr = []
        self.gpu_info_arr = []
        self.initial_gpu_driver = None
        self.initial_sec_gpu_state = False
        self.state = nvidia.source()

        self.ui_gpu_info_box = self.get_ui("ui_gpu_info_box")
        self.ui_gpu_box = self.get_ui("ui_gpu_box")
        self.ui_drv_box = self.get_ui("ui_drv_box")
        self.ui_main_box = self.get_ui("ui_main_box")
        self.ui_main_window = self.get_ui("ui_main_window")

        self.ui_info_stack = self.get_ui("ui_info_stack")
        self.ui_disabled_gpu_box = self.get_ui("ui_disabled_gpu_box")
        self.ui_enabled_gpu_box = self.get_ui("ui_enabled_gpu_box")

        self.ui_apply_chg_button = self.get_ui("ui_apply_chg_button")
        self.ui_disable_check_button = self.get_ui("ui_disable_check_button")

        self.ui_apply_chg_button.connect("clicked", self.on_apply_button_clicked)
        self.ui_repo_switch = self.get_ui("ui_repo_switch")
        self.ui_repo_switch.set_state(self.state)
        self.mirror_handler_id = self.ui_repo_switch.connect(
            "state-set", self.on_nvidia_mirror_changed
        )

        self.ui_about_dialog = self.get_ui("ui_about_dialog")
        self.ui_about_button = self.get_ui("ui_about_button")

        # Set version from __version__ file
        version = "1.0.0"
        try:
            ver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__version__")
            if os.path.isfile(ver_path):
                version = open(ver_path).readline().strip()
        except Exception:
            pass
        if self.ui_about_dialog:
            self.ui_about_dialog.set_version(version)
            self.ui_about_dialog.set_program_name("ParsLinux Nvidia Installer")
            self.ui_about_dialog.set_website("https://parslinux.org")

        self.ui_info_dialog = self.get_ui("ui_info_dialog")
        self.ui_about_button.connect("clicked", self.on_about_button_clicked)

        self.nvidia_devices = nvidia.graphics()
        self.ui_controller_box = self.get_ui("ui_controller_box")
        self.ui_secondary_gpu_box = self.get_ui("ui_secondary_gpu_box")

        self.ui_main_stack = self.get_ui("ui_main_stack")
        self.ui_nvidia_box = self.get_ui("ui_nvidia_box")
        self.ui_novidia_box = self.get_ui("ui_novidia_box")
        self.ui_disable_check_button.connect(
            "clicked", self.on_disable_checkbox_checked
        )
        self.ui_enable_button = self.get_ui("ui_enable_button")
        self.ui_enable_button.connect("clicked", self.on_enable_button_clicked)

        # Simulation button in no-device view
        self.ui_btn_simulate = self.get_ui("ui_btn_simulate")
        if self.ui_btn_simulate:
            self.ui_btn_simulate.connect("clicked", self.on_simulate_clicked)

        self.ui_detected_gpu_label = self.get_ui("ui_detected_gpu_label")
        if self.ui_detected_gpu_label:
            detected = get_system_gpu_description()
            self.ui_detected_gpu_label.set_markup(
                f'<span foreground="#94A3B8"><b>Sistemdeki Donanım:</b> {detected}</span>'
            )

        marker_present = not package.check_sec_state()
        self.disabled_no_devices = (
            not self.nvidia_devices and marker_present and not self.is_debug
        )

        self.check_secondary_gpu()

        self.apt_opr = ""
        if self.disabled_no_devices:
            self.ui_main_stack.set_visible_child(self.ui_nvidia_box)
            self.ui_apply_chg_button.set_sensitive(False)
            self.ui_repo_switch.set_sensitive(False)
        else:
            self.create_gpu_drivers()

        self.vte = Vte.Terminal()
        self.update_vte_color(self.vte)
        self.ui_box_vte = self.get_ui("ui_box_vte")
        vte_scrolled = Gtk.ScrolledWindow()
        vte_scrolled.add(self.vte)
        self.ui_box_vte.pack_start(vte_scrolled, True, True, 0)
        self.vte.connect("child-exited", self.on_vte_done)

        self.get_ui("ui_button_reboot").connect("clicked", self.do_reboot)
        self.get_ui("ui_button_exit").connect(
            "clicked", lambda x: self.application.quit()
        )

        self.op_widgets = (
            self.ui_apply_chg_button,
            self.ui_repo_switch,
            self.ui_enable_button,
            self.ui_disable_check_button,
        )

        self.ui_main_window.set_application(application)
        self.ui_main_window.set_title(_("ParsLinux Nvidia Installer"))
        self.ui_main_window.show_all()

    def on_simulate_clicked(self, button):
        self.is_debug = True
        os.environ["PARSLINUX_NVI_DEBUG"] = "1"
        self.nvidia_devices = nvidia.graphics()
        self.ui_main_stack.set_visible_child_name("page_main")
        self.create_gpu_drivers()
        self.ui_apply_chg_button.set_sensitive(True)
        self.ui_repo_switch.set_sensitive(True)

    def do_reboot(self, widget):
        self.ui_confirm_dialog.set_transient_for(widget.get_toplevel())
        response = self.ui_confirm_dialog.run()
        self.ui_confirm_dialog.hide()
        if response != Gtk.ResponseType.OK:
            return
        cmd = [
            "/usr/bin/dbus-send",
            "--system",
            "--print-reply",
            "--dest=org.freedesktop.login1",
            "/org/freedesktop/login1",
            "org.freedesktop.login1.Manager.Reboot",
            "boolean:true",
        ]
        try:
            subprocess.run(cmd)
        except Exception as e:
            print(f"Reboot invocation failed: {e}", file=sys.stderr)

    def on_vte_done(self, vte, status):
        self.get_ui("ui_box_vte_buttons").show_all()

        try:
            exit_code = os.waitstatus_to_exitcode(status)
        except ValueError:
            exit_code = status
        success = exit_code == 0
        reboot_pending = check_is_reboot_pending()
        self.get_ui("ui_button_reboot").set_sensitive(success and reboot_pending)

        for w in self.op_widgets:
            w.set_sensitive(True)
        if success:
            self.ui_apply_chg_button.set_sensitive(False)
        else:
            self.ui_apply_chg_button.set_sensitive(self.check_initials())

        status_label = self.get_ui("ui_vte_status_label")
        if status_label is not None:
            if success:
                markup = f'<span foreground="mediumspringgreen">{_("Operation completed successfully.")}</span>'
            else:
                markup = f'<span foreground="tomato">{_("Operation failed (exit code {code}). Please review the log above.").format(code=exit_code)}</span>'
            status_label.set_markup(markup)

        if self.apt_opr in ("install-nvidia", "install-nouveau", "update"):
            nvidia.reopen_cache()

        if self.apt_opr == "update":
            actual = nvidia.source()
            self.ui_repo_switch.handler_block(self.mirror_handler_id)
            try:
                self.ui_repo_switch.set_state(actual)
            finally:
                self.ui_repo_switch.handler_unblock(self.mirror_handler_id)
            self.state = actual

        if (
            success
            and self.apt_opr in ("install-nvidia", "install-nouveau", "update")
            and not self.disabled_no_devices
        ):
            self.create_gpu_drivers()

    def update_vte_color(self, vte):
        style_context = self.ui_main_window.get_style_context()
        background_color = style_context.get_background_color(Gtk.StateFlags.NORMAL)
        foreground_color = style_context.get_color(Gtk.StateFlags.NORMAL)
        vte.set_color_background(background_color)
        vte.set_color_foreground(foreground_color)

    def vte_start(self, params):
        for w in self.op_widgets:
            w.set_sensitive(False)
        self.get_ui("ui_box_vte_buttons").hide()
        self.get_ui("ui_vte_status_label").set_text("")
        self.ui_main_stack.set_visible_child_name("page_vte")
        self.vte.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.environ.get("HOME", "/tmp"),
            params,
            None,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None,
            None,
        )

    def check_secondary_gpu(self):
        self.initial_sec_gpu_state = package.check_sec_state()
        if self.initial_sec_gpu_state:
            self.ui_info_stack.set_visible_child(self.ui_enabled_gpu_box)
        else:
            self.ui_info_stack.set_visible_child(self.ui_disabled_gpu_box)

        if getattr(self, "disabled_no_devices", False):
            if self.ui_disable_check_button.get_parent() is not None:
                self.ui_controller_box.remove(self.ui_disable_check_button)
            return

        if not any(dev.is_secondary_gpu for dev in self.nvidia_devices):
            if self.ui_disable_check_button.get_parent() is not None:
                self.ui_controller_box.remove(self.ui_disable_check_button)

    def create_gpu_drivers(self):
        if len(self.nvidia_devices) == 0 and not self.is_debug:
            self.ui_main_stack.set_visible_child(self.ui_novidia_box)
            return

        self.ui_main_stack.set_visible_child_name("page_main")

        for toggle in self.drv_arr:
            self.ui_gpu_box.remove(toggle)
        for gpu_info in self.gpu_info_arr:
            self.ui_gpu_info_box.remove(gpu_info)
        self.drv_arr = []
        self.gpu_info_arr = []
        self.driver_buttons = []

        for nvidia_device in self.nvidia_devices:
            gpu_info = self.gpu_box(nvidia_device.device_name)
            self.gpu_info_arr.append(gpu_info)
            self.ui_gpu_info_box.pack_start(gpu_info, True, True, 5)

        self.nvidia_drivers = nvidia.drivers(gpus=self.nvidia_devices)
        self.filtered_nvidia_drivers = []
        for index, nvidia_driver in enumerate(self.nvidia_drivers):
            if index == 0:
                self.filtered_nvidia_drivers.append(nvidia_driver)
            else:
                if self.state:
                    if nvidia_driver.repo == "NVIDIA" or nvidia_driver.installed:
                        self.filtered_nvidia_drivers.append(nvidia_driver)
                else:
                    self.filtered_nvidia_drivers.append(nvidia_driver)

        self.nvidia_drivers = self.filtered_nvidia_drivers

        for index, nvidia_driver in enumerate(self.nvidia_drivers):
            toggle = self.driver_box(
                nvidia_driver.package,
                nvidia_driver.version,
                nvidia_driver.type,
                nvidia_driver.repo,
            )

            if nvidia_driver.installed:
                self.initial_gpu_driver = nvidia_driver
                self.toggled_driver = nvidia_driver
            toggle.set_active(nvidia_driver.installed)
            toggle.connect("toggled", self.on_drv_toggled, nvidia_driver)
            self.drv_arr.append(toggle)
            self.ui_gpu_box.pack_start(toggle, True, True, 5)

        self.ui_gpu_info_box.show_all()
        self.ui_gpu_box.show_all()
        self.ui_apply_chg_button.set_sensitive(self.check_initials())

    def get_ui(self, object_name: str):
        return self.gtk_builder.get_object(object_name)

    def driver_box(self, drv_name, drv_ver, drv_type, drv_repo):
        toggle_ui = os.path.normpath(os.path.join(os.path.dirname(__file__), "../ui/driver_toggle.glade"))
        b = Gtk.Builder.new_from_file(toggle_ui)
        btn = b.get_object("ui_radio_button")
        btn.set_name(drv_name)

        name = b.get_object("ui_name_label")
        markup = self.lbl_markup(_("Driver"), drv_name)
        name.set_markup(markup)

        ver = b.get_object("ui_version_label")
        markup = self.lbl_markup(_("Version"), drv_ver)
        ver.set_markup(markup)

        markup = self.lbl_markup(_("Description"), drv_type, color="dodgerblue")
        if drv_name == nouveau:
            markup = self.lbl_markup(
                _("Description"), drv_type, color="mediumspringgreen"
            )
        lbl = b.get_object("ui_driver_label")
        lbl.set_markup(markup)

        repo = b.get_object("ui_repo_label")
        markup = self.lbl_markup("Repo", drv_repo)
        repo.set_markup(markup)

        grp = None
        if len(self.driver_buttons) > 0:
            grp = self.driver_buttons[0]
        btn.join_group(grp)
        self.driver_buttons.append(btn)
        return btn

    def gpu_box(self, device_name):
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 13)
        name_label = Gtk.Label(xalign=0)
        name_label.set_markup(f"<b>{device_name}</b>")
        box.pack_start(name_label, True, True, 0)
        return box

    def lbl_markup(self, label, desc, color=None):
        if color:
            return f'<span> <b>{label}: </b> <span foreground="{color}">{desc}</span> </span>'
        else:
            return f"<span> <b>{label}: </b> <span>{desc}</span> </span>"

    def on_drv_toggled(self, radio_button, driver):
        if radio_button.get_active():
            self.toggled_driver = driver
        self.ui_apply_chg_button.set_sensitive(self.check_initials())

    def on_enable_button_clicked(self, button):
        pkg_bin = get_package_exec_path()
        params = ["/usr/bin/pkexec", pkg_bin, "enable-sec-gpu"]
        self.vte_start(params)

    def on_apply_button_clicked(self, button):
        pkg_bin = get_package_exec_path()
        params = ["/usr/bin/pkexec", pkg_bin]
        self.apt_opr = None
        disable_request = (
            self.initial_sec_gpu_state and self.ui_disable_check_button.get_active()
        )
        if disable_request:
            self.apt_opr = "disable-sec-gpu"
            params.append(self.apt_opr)
            self.vte_start(params)
        else:
            if self.toggled_driver and self.toggled_driver.package == nouveau:
                self.apt_opr = "install-nouveau"
                params.append(self.apt_opr)
            elif self.toggled_driver:
                self.apt_opr = "install-nvidia"
                driver_arg = self.toggled_driver.package
                version = self.toggled_driver.version
                if version:
                    nvidia.reopen_cache()
                    if not nvidia.has_pkg_version(
                        self.toggled_driver.package, version
                    ):
                        self._notify_version_gone()
                        self.create_gpu_drivers()
                        return
                    driver_arg = f"{self.toggled_driver.package}={version}"
                params += [
                    self.apt_opr,
                    f"linux-headers-{platform.uname().release}",
                    "linux-headers-amd64",
                    driver_arg,
                ]
            self.vte_start(params)

    def _notify_version_gone(self):
        dialog = Gtk.MessageDialog(
            transient_for=self.ui_main_window,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=_("Selected version is no longer available"),
        )
        dialog.format_secondary_text(
            _("The package list has been refreshed. Please choose a driver again.")
        )
        dialog.run()
        dialog.destroy()

    def on_about_button_clicked(self, button):
        self.ui_about_dialog.run()
        self.ui_about_dialog.hide()

    def check_initials(self):
        sec_gpu_changes = (
            self.initial_sec_gpu_state and self.ui_disable_check_button.get_active()
        )
        if self.toggled_driver is None:
            driver_changes = False
        else:
            driver_changes = self.toggled_driver != self.initial_gpu_driver
        return sec_gpu_changes or driver_changes

    def on_disable_checkbox_checked(self, button):
        self.ui_apply_chg_button.set_sensitive(self.check_initials())

    def on_nvidia_mirror_changed(self, button, state):
        pkg_bin = get_package_exec_path()
        params = ["/usr/bin/pkexec", pkg_bin, "update"]
        self.apt_opr = "update"
        self.vte_start(params)
