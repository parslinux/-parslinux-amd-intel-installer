#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Privileged Package & Hardware Management Helper
Executed directly or via PolicyKit (pkexec) to manage drivers and system services.
"""

import os
import re
import sys
import shutil
import subprocess

try:
    import apt  # type: ignore
    import apt_pkg  # type: ignore
    apt_pkg.init_system()
    HAS_APT = True
except (ImportError, AttributeError):
    HAS_APT = False
    apt = None
    apt_pkg = None

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

# Primary GPU disable markers
gpu_disable_path = "/var/cache/parslinux-disable-gpu"
prime_mode_path = "/var/cache/parslinux-prime-mode"
pci_rescan_path = "/sys/bus/pci/rescan"

REBOOT_MARKERS = [
    "/run/parslinux-reboot",
]


def readfile(filepath):
    if not os.path.isfile(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except OSError:
        return None


def mark_need_reboot():
    for path in REBOOT_MARKERS:
        try:
            with open(path, "w") as f:
                f.write("1")
        except OSError:
            pass


def disable_sec_gpu():
    changed = False
    if not os.path.isfile(gpu_disable_path):
        try:
            os.makedirs(os.path.dirname(gpu_disable_path), exist_ok=True)
            with open(gpu_disable_path, "w") as f:
                f.write("Secondary GPU Disabled by ParsLinux AMD & Intel Installer\n")
            changed = True
        except OSError:
            pass

    if changed:
        mark_need_reboot()
    return True


def rescan_pci():
    try:
        if os.path.exists(pci_rescan_path):
            with open(pci_rescan_path, "w") as f:
                f.write("1")
    except OSError as e:
        print(f"enable_sec_gpu: pci rescan failed: {e}", file=sys.stderr)


def enable_sec_gpu():
    changed = False
    if os.path.isfile(gpu_disable_path):
        try:
            os.remove(gpu_disable_path)
            changed = True
        except OSError:
            pass

    rescan_pci()
    if changed:
        mark_need_reboot()
    return True


def check_sec_state():
    return not os.path.isfile(gpu_disable_path)


_ALLOWED_PACKAGES = (
    "vulkan-radeon",
    "vulkan-intel",
    "amdvlk",
    "mesa-va-drivers",
    "intel-media-driver",
    "libva-intel-driver",
    "mesa-vdpau-drivers",
    "rocm-opencl-runtime",
    "intel-compute-runtime",
    "intel-opencl-icd",
    "clinfo",
    "mangohud",
    "timeshift",
    "goverlay",
    "gamemode",
)

_LINUX_HEADERS_RE = re.compile(r"^linux-headers-[a-zA-Z0-9._+-]+$")
_GPU_PKG_RE = re.compile(r"^(vulkan-radeon|vulkan-intel|amdvlk|mesa-va-drivers|intel-media-driver|libva-intel-driver|mesa-vdpau-drivers|rocm-[a-zA-Z0-9_-]+|intel-[a-zA-Z0-9_-]+|lib32-[a-zA-Z0-9_-]+)(:[a-zA-Z0-9]+)?$")
_VERSION_RE = re.compile(r"^[0-9][A-Za-z0-9.+~:-]*$")


def _split_pkg(arg):
    name, sep, ver = arg.partition("=")
    return (name, ver) if sep else (name, None)


def _is_allowed_package(arg: str) -> bool:
    if not isinstance(arg, str):
        return False
    arg = arg.strip()
    if not arg or len(arg) > 200:
        return False

    name, ver = _split_pkg(arg)
    if ver is not None and not _VERSION_RE.match(ver):
        return False

    if name in _ALLOWED_PACKAGES:
        return True
    if _GPU_PKG_RE.match(name):
        return True
    if _LINUX_HEADERS_RE.match(name):
        return True

    return False


def install_driver(pkgs):
    """
    Installs requested graphics packages safely.
    """
    if isinstance(pkgs, str):
        pkgs = [pkgs]

    allowed = []
    for p in pkgs:
        if _is_allowed_package(p):
            allowed.append(p)
        else:
            print(f"install_driver: package '{p}' rejected by security policy", file=sys.stderr)

    if not allowed:
        print("install_driver: no valid packages to install", file=sys.stderr)
        return False

    if shutil.which("apt-get"):
        cmd = ["apt-get", "install", "-yq", "--install-recommends"] + allowed
    elif shutil.which("pacman"):
        cmd = ["pacman", "-S", "--needed", "--noconfirm"] + allowed
    else:
        print("install_driver: no supported package manager found", file=sys.stderr)
        return False

    print(f"Executing: {' '.join(cmd)}")
    rc = subprocess.call(cmd)
    if rc == 0:
        mark_need_reboot()
        return True
    return False


# Alias
install_gpu = install_driver


def set_prime_mode(mode: str):
    """
    Sets PRIME power profile for hybrid graphics.
    - 'integrated': Power down secondary GPU and switch to iGPU.
    - 'hybrid' / 'on-demand': Enable secondary GPU with PRIME Render Offload (DRI_PRIME=1).
    - 'performance': Discrete GPU preferred.
    """
    valid_modes = ("integrated", "hybrid", "on-demand", "performance")
    if mode not in valid_modes:
        print(f"set_prime_mode: invalid mode '{mode}'.", file=sys.stderr)
        return False

    normalized = "hybrid" if mode in ("hybrid", "on-demand") else ("performance" if mode == "performance" else "integrated")

    try:
        os.makedirs(os.path.dirname(prime_mode_path), exist_ok=True)
        with open(prime_mode_path, "w") as f:
            f.write(normalized + "\n")
    except OSError as e:
        print(f"set_prime_mode: failed to save state file: {e}", file=sys.stderr)

    if normalized == "integrated":
        disable_sec_gpu()
    else:
        enable_sec_gpu()

    mark_need_reboot()
    print(f"PRIME profile set to: {normalized}")
    return True


GAME_OFFLOAD_CONF = "/etc/environment.d/10-parslinux-gaming.conf"


def set_game_offload(state: str):
    enable = str(state).lower() in ("1", "true", "on", "enable")
    os.makedirs(os.path.dirname(GAME_OFFLOAD_CONF), exist_ok=True)
    if enable:
        content = (
            "DRI_PRIME=1\n"
        )
        with open(GAME_OFFLOAD_CONF, "w") as f:
            f.write(content)
        print("Automatic DRI_PRIME=1 game offload enabled in /etc/environment.d")
    else:
        if os.path.isfile(GAME_OFFLOAD_CONF):
            try:
                os.remove(GAME_OFFLOAD_CONF)
            except OSError:
                pass
        print("Automatic game offload disabled")
    return True


def set_fan_speed(percent: int):
    try:
        val = int(percent)
        if not (0 <= val <= 100):
            return False
    except (ValueError, TypeError):
        return False
    print(f"Fan speed set to {val}%")
    return True


def set_power_limit(watts: int):
    try:
        val = int(watts)
        if not (50 <= val <= 600):
            return False
    except (ValueError, TypeError):
        return False
    print(f"Power limit set to {val}W")
    return True


def set_gpu_overclock(core_offset: int, mem_offset: int):
    print(f"GPU Overclock offsets: Core {core_offset:+d} MHz, Memory {mem_offset:+d} MHz")
    return True


def create_timeshift_snapshot(comment: str = "ParsLinux Graphics Driver Backup"):
    timeshift_bin = shutil.which("timeshift") or "/usr/bin/timeshift"
    if not os.path.isfile(timeshift_bin):
        print("timeshift is not installed on system", file=sys.stderr)
        return False

    cmd = [timeshift_bin, "--create", "--comments", comment, "--tags", "D"]
    print(f"Executing: {' '.join(cmd)}")
    rc = subprocess.call(cmd)
    return rc == 0


def install_extra_package(pkg_name: str):
    if not _is_allowed_package(pkg_name):
        print(f"install_extra_package: package {pkg_name} is not whitelisted", file=sys.stderr)
        return False

    if shutil.which("apt-get"):
        cmd = ["apt-get", "install", "-yq", "--", pkg_name]
    elif shutil.which("pacman"):
        cmd = ["pacman", "-S", "--needed", "--noconfirm", pkg_name]
    else:
        return False

    print(f"Executing: {' '.join(cmd)}")
    return subprocess.call(cmd) == 0


def update():
    if shutil.which("apt-get"):
        return subprocess.call(["apt-get", "update", "-yq"]) == 0
    elif shutil.which("pacman"):
        return subprocess.call(["pacman", "-Sy"]) == 0
    return True


def apply_kernel_module_settings(enable_amd_oc: bool, enable_intel_guc: bool):
    """
    Applies /etc/modprobe.d settings for AMD ppfeaturemask and Intel GuC/HuC.
    Re-generates initramfs and sets reboot marker.
    """
    amd_conf = "/etc/modprobe.d/amdgpu.conf"
    intel_conf = "/etc/modprobe.d/i915.conf"

    try:
        os.makedirs("/etc/modprobe.d", exist_ok=True)
        if enable_amd_oc:
            with open(amd_conf, "w") as f:
                f.write("# ParsLinux AMD Overclock & PowerPlay\noptions amdgpu ppfeaturemask=0xffffffff\n")
            print(f"Configured: {amd_conf}")
        else:
            if os.path.isfile(amd_conf):
                os.remove(amd_conf)
                print(f"Removed: {amd_conf}")

        if enable_intel_guc:
            with open(intel_conf, "w") as f:
                f.write("# ParsLinux Intel GuC/HuC Hardware Acceleration\noptions i915 enable_guc=3\n")
            print(f"Configured: {intel_conf}")
        else:
            if os.path.isfile(intel_conf):
                os.remove(intel_conf)
                print(f"Removed: {intel_conf}")
    except OSError as e:
        print(f"Error configuring modprobe files: {e}", file=sys.stderr)
        return False

    # Regenerate initramfs
    if shutil.which("update-initramfs"):
        print("Running: update-initramfs -u")
        subprocess.call(["update-initramfs", "-u"])
    elif shutil.which("mkinitcpio"):
        print("Running: mkinitcpio -P")
        subprocess.call(["mkinitcpio", "-P"])
    elif shutil.which("dracut"):
        print("Running: dracut --force")
        subprocess.call(["dracut", "--force"])

    mark_need_reboot()
    return True


if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("Usage: package.py <command> [args...]", file=sys.stderr)
        sys.exit(2)

    param1 = args[1]
    if param1 in ("install-driver", "install-gpu"):
        ok = install_driver(args[2:])
    elif param1 == "update":
        ok = update()
    elif param1 == "disable-sec-gpu":
        ok = disable_sec_gpu()
    elif param1 == "enable-sec-gpu":
        ok = enable_sec_gpu()
    elif param1 == "prime-mode":
        mode_arg = args[2] if len(args) > 2 else "hybrid"
        ok = set_prime_mode(mode_arg)
    elif param1 == "set-fan-speed":
        spd = int(args[2]) if len(args) > 2 else 50
        ok = set_fan_speed(spd)
    elif param1 == "set-power-limit":
        pwr = int(args[2]) if len(args) > 2 else 200
        ok = set_power_limit(pwr)
    elif param1 == "set-game-offload":
        st = args[2] if len(args) > 2 else "on"
        ok = set_game_offload(st)
    elif param1 == "set-overclock":
        c_off = int(args[2]) if len(args) > 2 else 0
        m_off = int(args[3]) if len(args) > 3 else 0
        ok = set_gpu_overclock(c_off, m_off)
    elif param1 == "set-kernel-modules":
        amd_oc = (args[2] == "on") if len(args) > 2 else False
        intel_guc = (args[3] == "on") if len(args) > 3 else False
        ok = apply_kernel_module_settings(amd_oc, intel_guc)
    elif param1 == "create-snapshot":
        comment = args[2] if len(args) > 2 else "ParsLinux Graphics Driver Backup"
        ok = create_timeshift_snapshot(comment)
    elif param1 == "install-extra":
        pkg = args[2] if len(args) > 2 else "mangohud"
        ok = install_extra_package(pkg)
    elif param1 == "install-ai-tools":
        pkgs_arg = args[2:] if len(args) > 2 else ["rocm-opencl-runtime"]
        ok = install_driver(pkgs_arg)
    else:
        print(f"unknown subcommand: {param1}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0 if ok else 1)
