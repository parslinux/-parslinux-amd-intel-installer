#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Setup Script
"""

import os
import subprocess
try:
    from setuptools import setup, find_packages
except ImportError:
    # Minimal fallback runner when python-setuptools is not installed
    def find_packages():
        return []

    def setup(**kwargs):
        import sys
        import shutil

        if any("clean" in arg for arg in sys.argv):
            return

        if any("build" in arg for arg in sys.argv):
            print("Build: pure Python application ready.")
            return

        if any("install" in arg for arg in sys.argv):
            root = ""
            prefix = "/usr"
            for arg in sys.argv[1:]:
                if arg.startswith("--root="):
                    root = arg.split("=", 1)[1]
                elif arg.startswith("--prefix="):
                    prefix = arg.split("=", 1)[1]

            # Install data_files
            for dest, files in kwargs.get("data_files", []):
                clean_dest = dest.lstrip("/")
                target_dir = os.path.join(root, clean_dest) if root else dest
                os.makedirs(target_dir, exist_ok=True)
                for src in files:
                    if os.path.isfile(src):
                        shutil.copy2(src, target_dir)

            # Install scripts
            for script in kwargs.get("scripts", []):
                target_bin = (
                    os.path.join(root, prefix.lstrip("/"), "bin")
                    if root
                    else os.path.join(prefix, "bin")
                )
                os.makedirs(target_bin, exist_ok=True)
                dest_file = os.path.join(target_bin, os.path.basename(script))
                shutil.copy2(script, dest_file)
                os.chmod(dest_file, 0o755)

            print(f"Install complete (target root: '{root}', prefix: '{prefix}').")
            return

        print(f"Setuptools not present; ignoring unsupported arguments: {sys.argv[1:]}")



def create_mo_files():
    podir = "data/po"
    mo = []
    if os.path.exists(podir):
        for po in os.listdir(podir):
            if po.endswith(".po"):
                lang = po.split(".po")[0]
                lang_dir = f"mo/{lang}/LC_MESSAGES"
                os.makedirs(lang_dir, exist_ok=True)
                mo_file = f"{lang_dir}/parslinux-amd-intel-installer.mo"
                msgfmt_cmd = f"msgfmt {podir}/{po} -o {mo_file}"
                subprocess.call(msgfmt_cmd, shell=True)
                mo.append((f"/usr/share/locale/{lang}/LC_MESSAGES", [mo_file]))
    return mo


version = "1.0.0"
ver_path = "src/__version__"
if os.path.exists(ver_path):
    try:
        with open(ver_path) as f:
            version = f.read().strip()
    except Exception:
        pass

icon_source = "images/parslinux-amd-intel-installer.svg" if os.path.isfile("images/parslinux-amd-intel-installer.svg") else "parslinux-amd-intel-installer.svg"

data_files = [
    ("/usr/share/applications", ["org.parslinux.amd-intel-installer.desktop"]),
    ("/usr/share/metainfo", ["data/org.parslinux.amd-intel-installer.metainfo.xml"]),
    ("/usr/share/polkit-1/actions", ["org.parslinux.pkexec.parslinux-amd-intel-installer.policy"]),
    ("/usr/share/icons/hicolor/scalable/apps", [icon_source]),
    ("/usr/bin", ["parslinux-amd-intel-installer"]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer", [
        "parslinux-amd-intel-installer",
        icon_source,
        "pni-disable-gpu.sh",
        "update_translations.sh"
    ]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer/images", [
        "images/parslinux-amd-intel-installer.svg"
    ]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer/src", [
        "src/Main.py",
        "src/MainWindow.py",
        "src/amd_intel.py",
        "src/detector.py",
        "src/kernel_config.py",
        "src/monitor.py",
        "src/tray.py",
        "src/package.py",
        "src/__version__"
    ]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer/ui", [
        "ui/ui.glade",
        "ui/driver_toggle.glade"
    ]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer/data", [
        "data/style.css"
    ]),
    ("/usr/share/parslinux/parslinux-amd-intel-installer/data/assets", [
        "data/assets/amd_logo.svg",
        "data/assets/intel_logo.svg",
        "data/assets/amd_intel_logo.svg",
        "data/assets/amd_logo.png",
        "data/assets/intel_logo.png",
        "data/assets/amd_intel_logo.png",
        "data/assets/parslinux-logo.svg",
        "data/assets/video_card.svg",
        "data/assets/video_card_disabled.svg"
    ]),
] + create_mo_files()

setup(
    name="parslinux-amd-intel-installer",
    version=version,
    packages=find_packages(),
    scripts=["parslinux-amd-intel-installer"],
    data_files=data_files,
    author="ParsLinux Developers",
    author_email="dev@parslinux.org",
    description="ParsLinux AMD & Intel Graphics Driver Installer & GPU Manager",
    long_description=open("README.md").read() if os.path.isfile("README.md") else "",
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="amd intel radeon arc iris driver graphics installer parslinux hybrid vulkan vaapi",
    url="https://parslinux.org",
)
