#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Kernel Module Parameters Manager
Manages /etc/modprobe.d/ configuration for:
- AMD: Overclocking & PowerPlay feature mask (amdgpu.ppfeaturemask=0xffffffff)
- Intel: GuC/HuC hardware video decoding & compute acceleration (i915.enable_guc=3)
"""

import os
import shutil
from locale import gettext as _

AMDGPU_CONF_PATH = "/etc/modprobe.d/amdgpu.conf"
I915_CONF_PATH = "/etc/modprobe.d/i915.conf"
XE_CONF_PATH = "/etc/modprobe.d/xe.conf"

AMDGPU_SYS_PARAM = "/sys/module/amdgpu/parameters/ppfeaturemask"
I915_SYS_PARAM = "/sys/module/i915/parameters/enable_guc"


def get_kernel_module_status():
    """
    Returns current runtime and persistent modprobe configuration
    for AMD and Intel graphics drivers.
    """
    # 1. AMD Status
    amd_loaded = os.path.isdir("/sys/module/amdgpu")
    amd_ppfeaturemask_val = ""
    amd_oc_unlocked = False

    if os.path.isfile(AMDGPU_SYS_PARAM):
        try:
            with open(AMDGPU_SYS_PARAM, "r") as f:
                val = f.read().strip()
                amd_ppfeaturemask_val = val
                # 0xffffffff or 4294967295 or 0xffff7fff indicates unlocked
                if val in ("0xffffffff", "4294967295", "-1") or val.startswith("0xffff"):
                    amd_oc_unlocked = True
        except Exception:
            pass

    amd_conf_active = False
    if os.path.isfile(AMDGPU_CONF_PATH):
        try:
            with open(AMDGPU_CONF_PATH, "r") as f:
                content = f.read()
                if "ppfeaturemask=0xffffffff" in content or "ppfeaturemask=0xffff" in content:
                    amd_conf_active = True
        except Exception:
            pass

    # 2. Intel Status
    intel_i915_loaded = os.path.isdir("/sys/module/i915")
    intel_xe_loaded = os.path.isdir("/sys/module/xe")
    intel_guc_val = ""
    intel_guc_active = False

    if os.path.isfile(I915_SYS_PARAM):
        try:
            with open(I915_SYS_PARAM, "r") as f:
                val = f.read().strip()
                intel_guc_val = val
                # enable_guc=3 enables both GuC and HuC firmware
                if val in ("3", "2", "1"):
                    intel_guc_active = True
        except Exception:
            pass

    intel_conf_active = False
    if os.path.isfile(I915_CONF_PATH):
        try:
            with open(I915_CONF_PATH, "r") as f:
                content = f.read()
                if "enable_guc=3" in content or "enable_guc" in content:
                    intel_conf_active = True
        except Exception:
            pass

    return {
        "amd": {
            "loaded": amd_loaded,
            "runtime_mask": amd_ppfeaturemask_val,
            "runtime_unlocked": amd_oc_unlocked,
            "conf_path": AMDGPU_CONF_PATH,
            "conf_active": amd_conf_active,
        },
        "intel": {
            "loaded": (intel_i915_loaded or intel_xe_loaded),
            "is_xe": intel_xe_loaded,
            "runtime_guc": intel_guc_val,
            "runtime_active": intel_guc_active,
            "conf_path": I915_CONF_PATH,
            "conf_active": intel_conf_active,
        },
    }


def generate_apply_command(enable_amd_oc: bool, enable_intel_guc: bool) -> str:
    """
    Generates a secure bash script snippet executed via pkexec
    to apply module options and regenerate the system initramfs.
    """
    commands = ["set -e"]

    # Handle AMD ppfeaturemask
    if enable_amd_oc:
        commands.append(
            f'printf "# ParsLinux AMD Optimization\\noptions amdgpu ppfeaturemask=0xffffffff\\n" > "{AMDGPU_CONF_PATH}"'
        )
    else:
        commands.append(f'rm -f "{AMDGPU_CONF_PATH}"')

    # Handle Intel GuC / HuC
    if enable_intel_guc:
        commands.append(
            f'printf "# ParsLinux Intel Optimization\\noptions i915 enable_guc=3\\n" > "{I915_CONF_PATH}"'
        )
    else:
        commands.append(f'rm -f "{I915_CONF_PATH}"')

    # Update initramfs depending on distro
    if shutil.which("update-initramfs"):
        commands.append("update-initramfs -u")
    elif shutil.which("mkinitcpio"):
        commands.append("mkinitcpio -P")
    elif shutil.which("dracut"):
        commands.append("dracut --force")

    return " && ".join(commands)
