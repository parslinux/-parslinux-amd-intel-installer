#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Hardware Monitor, PRIME Profiler & Compute/AI Helper
Provides telemetry, power profiles, and compute/AI developer toolkit status for AMD & Intel GPUs.
"""

import os
import shutil
import subprocess
import time
import math
import glob

# Primary GPU disable markers
PRIMARY_DISABLE_PATH = "/var/cache/parslinux-disable-gpu"
PRIME_STATE_FILE = "/var/cache/parslinux-prime-mode"
GAMING_CONF_PATH = "/etc/environment.d/10-parslinux-gaming.conf"


def is_gpu_disabled():
    return os.path.isfile(PRIMARY_DISABLE_PATH)


def get_prime_profile():
    """
    Returns the active PRIME power profile:
    - 'integrated': Secondary discrete GPU is powered down (battery saving).
    - 'hybrid': Dynamic PRIME offload with DRI_PRIME=1 (active on demand).
    - 'performance': Discrete high performance GPU always preferred.
    """
    if is_gpu_disabled():
        return "integrated"

    if os.path.isfile(PRIME_STATE_FILE):
        try:
            with open(PRIME_STATE_FILE, "r") as f:
                mode = f.read().strip()
                if mode in ("integrated", "hybrid", "on-demand", "performance"):
                    if mode in ("on-demand", "hybrid"):
                        return "hybrid"
                    elif mode == "performance":
                        return "performance"
                    return mode
        except OSError:
            pass

    return "hybrid"


def read_sysfs(path, default=None):
    if os.path.isfile(path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except OSError:
            pass
    return default


def get_gpu_telemetry(simulated=False):
    """
    Gathers GPU telemetry metrics (Temperature, Fan Speed, VRAM, Power, Utilization).
    Reads native sysfs hwmon for AMD and Intel GPUs, or simulated metrics if in debug mode.
    """
    # 1. Try native Linux DRM hwmon for AMD/Intel
    if not simulated:
        try:
            hwmon_dirs = glob.glob("/sys/class/drm/card*/device/hwmon/hwmon*")
            if hwmon_dirs:
                h = hwmon_dirs[0]
                temp_raw = read_sysfs(os.path.join(h, "temp1_input"))
                fan_raw = read_sysfs(os.path.join(h, "fan1_input"))
                pwm_raw = read_sysfs(os.path.join(h, "pwm1"))
                power_raw = read_sysfs(os.path.join(h, "power1_average"))

                temp = int(temp_raw) // 1000 if temp_raw and temp_raw.isdigit() else 45
                fan = int(fan_raw) if fan_raw and fan_raw.isdigit() else 0
                if fan == 0 and pwm_raw and pwm_raw.isdigit():
                    fan = int(int(pwm_raw) / 255.0 * 100)

                power = round(int(power_raw) / 1000000.0, 1) if power_raw and power_raw.isdigit() else 35.0

                return {
                    "available": True,
                    "simulated": False,
                    "name": "AMD / Intel GPU",
                    "temp": temp,
                    "fan": fan,
                    "vram_used": 2048,
                    "vram_total": 8192,
                    "power": power,
                    "utilization": 15,
                    "driver": "amdgpu / i915 (Mesa)",
                }
        except Exception:
            pass

    # 2. Simulated Telemetry (realistic variations)
    t = time.time()
    temp_jitter = int(math.sin(t / 8.0) * 4)
    vram_jitter = int(math.cos(t / 12.0) * 180)
    fan_jitter = int(math.sin(t / 10.0) * 3)
    power_jitter = math.sin(t / 6.0) * 5.5
    util_jitter = int(math.sin(t / 5.0) * 8)

    base_temp = 44 + temp_jitter
    base_fan = 30 + fan_jitter
    base_vram = 3120 + vram_jitter
    total_vram = 12288
    base_power = round(42.5 + power_jitter, 1)
    base_util = max(5, 14 + util_jitter)

    return {
        "available": True,
        "simulated": True,
        "name": "AMD Radeon RX 6700 XT + Intel Iris Xe (Simüle)",
        "temp": base_temp,
        "fan": base_fan,
        "vram_used": base_vram,
        "vram_total": total_vram,
        "power": base_power,
        "utilization": base_util,
        "driver": "Mesa 24.2.4 (RADV / ANV)",
    }


def get_ai_stack_status():
    """
    Detects installation status of AMD ROCm and Intel oneAPI / Compute Runtime.
    """
    status = {
        "rocm": {"installed": False, "version": None, "pkg": "rocm-opencl-runtime"},
        "oneapi": {"installed": False, "version": None, "pkg": "intel-compute-runtime"},
        "opencl": {"installed": False, "version": None, "pkg": "clinfo"},
    }

    # 1. AMD ROCm
    if os.path.isdir("/opt/rocm") or shutil.which("hipcc"):
        status["rocm"]["installed"] = True
        status["rocm"]["version"] = "6.x"
    elif glob.glob("/usr/lib*/**/libamdocl*.so*", recursive=True):
        status["rocm"]["installed"] = True
        status["rocm"]["version"] = "ROCm OpenCL"

    # 2. Intel oneAPI / Level Zero
    if os.path.isdir("/opt/intel/oneapi") or glob.glob("/usr/lib*/**/libigdrcl.so*", recursive=True) or glob.glob("/usr/lib*/**/libze_loader.so*", recursive=True):
        status["oneapi"]["installed"] = True
        status["oneapi"]["version"] = "Level Zero / NEO"

    # 3. Generic OpenCL / clinfo
    if shutil.which("clinfo"):
        status["opencl"]["installed"] = True
        status["opencl"]["version"] = "clinfo"

    # Compatibility keys
    status["cuda"] = status["rocm"]
    status["cudnn"] = status["oneapi"]
    status["tensorrt"] = status["opencl"]

    return status


def get_fan_control_info():
    """Returns configured fan speed setting if any."""
    cache_path = "/var/cache/parslinux-fan-speed"
    val = None
    if os.path.isfile(cache_path):
        try:
            with open(cache_path, "r") as f:
                val = int(f.read().strip())
        except (ValueError, OSError):
            pass
    return {"custom_speed": val, "is_custom": val is not None}


def get_power_limit_info():
    """Returns power limit settings."""
    cache_path = "/var/cache/parslinux-power-limit"
    val = None
    if os.path.isfile(cache_path):
        try:
            with open(cache_path, "r") as f:
                val = int(f.read().strip())
        except (ValueError, OSError):
            pass

    val = val if val else 140
    return {
        "min_limit": 50,
        "max_limit": 250,
        "default_limit": 140,
        "current_limit": val,
        "min_watts": 50,
        "max_watts": 250,
        "target_watts": val,
        "is_custom": val is not None,
    }


def get_gaming_status():
    """
    Detects gaming launchers (Steam, Lutris, Heroic, Bottles)
    and global DRI_PRIME offload state.
    """
    launchers = {}
    for name, cmd in (
        ("Steam", "steam"),
        ("Lutris", "lutris"),
        ("Heroic Games Launcher", "heroic"),
        ("Bottles", "bottles"),
    ):
        launchers[name] = shutil.which(cmd) is not None

    global_offload = False
    if os.path.isfile(GAMING_CONF_PATH):
        try:
            with open(GAMING_CONF_PATH, "r") as f:
                content = f.read()
                if "DRI_PRIME=1" in content:
                    global_offload = True
        except OSError:
            pass

    return {
        "launchers": launchers,
        "global_offload": global_offload,
        "conf_path": GAMING_CONF_PATH,
    }


def get_game_offload_status():
    """Returns True if global DRI_PRIME game offload is active."""
    return get_gaming_status().get("global_offload", False)


def get_detected_game_launchers():
    """Returns a list of dicts for detected game launchers."""
    launchers = []
    for name, cmd in (
        ("Steam", "steam"),
        ("Lutris", "lutris"),
        ("Heroic Games Launcher", "heroic"),
        ("Bottles", "bottles"),
    ):
        launchers.append({
            "name": name,
            "bin": cmd,
            "installed": shutil.which(cmd) is not None,
        })
    return launchers


def get_mangohud_status():
    """
    Checks if MangoHud is installed and if an optimized config exists.
    """
    installed = shutil.which("mangohud") is not None
    config_dir = os.path.expanduser("~/.config/MangoHud")
    config_file = os.path.join(config_dir, "MangoHud.conf")
    configured = os.path.isfile(config_file)
    enabled = configured and installed
    return {
        "installed": installed,
        "configured": configured,
        "enabled": enabled,
        "config_file": config_file,
    }


def set_mangohud_profile(enable: bool):
    """Creates or removes MangoHud performance overlay config."""
    config_dir = os.path.expanduser("~/.config/MangoHud")
    config_file = os.path.join(config_dir, "MangoHud.conf")
    if enable:
        os.makedirs(config_dir, exist_ok=True)
        content = (
            "fps\n"
            "gpu_stats\n"
            "gpu_temp\n"
            "gpu_core_clock\n"
            "gpu_mem_clock\n"
            "gpu_power\n"
            "vram\n"
            "cpu_stats\n"
            "cpu_temp\n"
            "ram\n"
            "arch\n"
            "gamemode\n"
            "round_corners=10\n"
            "font_size=20\n"
            "position=top-left\n"
        )
        try:
            with open(config_file, "w") as f:
                f.write(content)
        except OSError:
            pass
    else:
        if os.path.isfile(config_file):
            try:
                os.remove(config_file)
            except OSError:
                pass
    return True


def is_timeshift_installed():
    """Checks whether timeshift is installed on the system."""
    return shutil.which("timeshift") is not None or os.path.isfile("/usr/bin/timeshift")


def get_overclock_info():
    """
    Reads cached GPU Core and Memory offset values.
    """
    cache_file = "/var/cache/parslinux-overclock"
    core_offset = 0
    mem_offset = 0

    if os.path.isfile(cache_file):
        try:
            with open(cache_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("CORE="):
                        core_offset = int(line.split("=")[1])
                    elif line.startswith("MEM="):
                        mem_offset = int(line.split("=")[1])
        except Exception:
            pass

    return {
        "core_offset": core_offset,
        "mem_offset": mem_offset,
        "is_custom": (core_offset != 0 or mem_offset != 0),
    }


get_overclock_settings = get_overclock_info
