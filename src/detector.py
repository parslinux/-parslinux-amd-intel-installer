#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Hardware & GPU Auto-Detection System
Provides multi-layer hardware detection, architecture identification,
and smart driver/layer recommendation for AMD Radeon and Intel GPUs.
"""

import os
import sys
import re
import subprocess
from locale import gettext as _

AMD_VENDOR_ID = 0x1002
INTEL_VENDOR_ID = 0x8086

# AMD & Intel Architecture definitions & recommended packages
ARCHITECTURES = {
    # AMD Architectures
    "RDNA 3 / 3.5": {
        "name": "AMD RDNA 3 / 3.5",
        "vendor": "AMD",
        "description": _("RDNA 3/3.5 Architecture (Radeon RX 7000 Series / Radeon 780M/890M)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("RADV (Mesa) provides ray tracing, FSR 3 and ACO shader compilation.")
    },
    "RDNA 2": {
        "name": "AMD RDNA 2",
        "vendor": "AMD",
        "description": _("RDNA 2 Architecture (Radeon RX 6000 Series / Steam Deck)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("Fully supported by amdgpu kernel module and Mesa RADV Vulkan.")
    },
    "RDNA 1": {
        "name": "AMD RDNA 1",
        "vendor": "AMD",
        "description": _("RDNA 1 Architecture (Radeon RX 5000 Series)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("Stable open-source amdgpu and Mesa RADV driver stack.")
    },
    "Vega": {
        "name": "AMD Vega / GCN 5",
        "vendor": "AMD",
        "description": _("Vega Architecture (Vega 56/64, Radeon VII, Ryzen 2000-5000 iGPU)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("Supported by amdgpu driver with mature Vulkan and VA-API.")
    },
    "Polaris": {
        "name": "AMD Polaris / GCN 4",
        "vendor": "AMD",
        "description": _("Polaris Architecture (Radeon RX 400/500 Series, RX 580/570)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("Rock solid amdgpu support with RADV Vulkan.")
    },
    "GCN Legacy": {
        "name": "AMD GCN 1-3",
        "vendor": "AMD",
        "description": _("Legacy GCN Architecture (HD 7000 / R9 200/300 Series)"),
        "recommended_package": "vulkan-radeon",
        "vaapi_package": "mesa-va-drivers",
        "reason": _("Mature kernel and Mesa support.")
    },

    # Intel Architectures
    "Intel Battlemage": {
        "name": "Intel Battlemage (Xe2)",
        "vendor": "Intel",
        "description": _("Intel Battlemage Xe2 Architecture (Arc B580 / B570 / Lunar Lake)"),
        "recommended_package": "vulkan-intel",
        "vaapi_package": "intel-media-driver",
        "reason": _("Modern Xe kernel driver with Mesa ANV Vulkan and XeSS support.")
    },
    "Intel Alchemist": {
        "name": "Intel Alchemist (Xe-HPG)",
        "vendor": "Intel",
        "description": _("Intel Arc Alchemist Architecture (A770 / A750 / A580 / A380)"),
        "recommended_package": "vulkan-intel",
        "vaapi_package": "intel-media-driver",
        "reason": _("Dedicated Intel Arc graphics with full DXVK and ANV Vulkan compatibility.")
    },
    "Intel Meteor/Lunar Lake": {
        "name": "Intel Core Ultra (Xe-LPG)",
        "vendor": "Intel",
        "description": _("Intel Core Ultra Xe Graphics (Meteor Lake / Arrow Lake)"),
        "recommended_package": "vulkan-intel",
        "vaapi_package": "intel-media-driver",
        "reason": _("Next-gen integrated Xe graphics with Intel Media Driver.")
    },
    "Intel Iris Xe": {
        "name": "Intel Iris Xe (Gen12)",
        "vendor": "Intel",
        "description": _("Intel Iris Xe Graphics (11th-14th Gen Core iGPU)"),
        "recommended_package": "vulkan-intel",
        "vaapi_package": "intel-media-driver",
        "reason": _("Supported by i915 / xe kernel modules and Intel Media Driver (iHD).")
    },
    "Intel UHD": {
        "name": "Intel UHD / HD Graphics (Gen9/9.5)",
        "vendor": "Intel",
        "description": _("Intel UHD/HD Graphics (6th-10th Gen Skylake / Kaby Lake / Comet Lake)"),
        "recommended_package": "vulkan-intel",
        "vaapi_package": "intel-media-driver",
        "reason": _("Solid VA-API QuickSync video decoding and stable 2D/3D Mesa.")
    }
}


def get_pci_database():
    """Load PCI ID names from system files."""
    paths = [
        "/usr/share/misc/pci.ids",
        "/usr/share/hwdata/pci.ids",
        "/usr/share/pci.ids",
    ]
    pci_db = {}
    db_file = None
    for p in paths:
        if os.path.isfile(p):
            db_file = p
            break
    if not db_file:
        return pci_db

    cur_vendor = None
    try:
        with open(db_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                if not line.startswith("\t"):
                    parts = line.strip().split(" ", 1)
                    try:
                        v_id = int(parts[0], 16)
                        v_name = parts[1].strip() if len(parts) > 1 else "Unknown"
                        pci_db[v_id] = {"vendor_name": v_name, "devices": {}}
                        cur_vendor = v_id
                    except ValueError:
                        cur_vendor = None
                else:
                    if cur_vendor is None or line.startswith("\t\t"):
                        continue
                    parts = line.strip().split(" ", 1)
                    try:
                        dev_id = int(parts[0], 16)
                        dev_name = parts[1].strip() if len(parts) > 1 else f"Device {dev_id:04x}"
                        pci_db[cur_vendor]["devices"][dev_id] = dev_name
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Warning: Failed to load pci.ids: {e}", file=sys.stderr)
    return pci_db


def identify_architecture(vendor_id, device_id_int, device_name=""):
    """
    Given a vendor, PCI device ID and name, determine the AMD or Intel architecture.
    """
    name_upper = (device_name or "").upper()

    if vendor_id == AMD_VENDOR_ID:
        if any(k in name_upper for k in ("RX 7", "780M", "890M", "NAVI 3", "RDNA 3", "RDNA3")):
            a = ARCHITECTURES["RDNA 3 / 3.5"]
            return "RDNA 3 / 3.5", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("RX 6", "680M", "660M", "NAVI 2", "RDNA 2", "RDNA2", "VAN GOGH")):
            a = ARCHITECTURES["RDNA 2"]
            return "RDNA 2", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("RX 5700", "RX 5600", "RX 5500", "NAVI 1", "RDNA 1")):
            a = ARCHITECTURES["RDNA 1"]
            return "RDNA 1", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("VEGA", "RADEON VII")):
            a = ARCHITECTURES["Vega"]
            return "Vega", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("RX 580", "RX 570", "RX 560", "RX 480", "RX 470", "POLARIS", "ELLESMERE")):
            a = ARCHITECTURES["Polaris"]
            return "Polaris", a["description"], a["recommended_package"], a["reason"]

        a = ARCHITECTURES["RDNA 2"]
        return "AMD Radeon", _("AMD Radeon Grafik Mimarisi"), "vulkan-radeon", _("Mesa RADV Vulkan ve VA-API sürücüsü önerilmektedir.")

    elif vendor_id == INTEL_VENDOR_ID:
        if any(k in name_upper for k in ("B580", "B570", "BATTLEMAGE", "BMG")):
            a = ARCHITECTURES["Intel Battlemage"]
            return "Intel Battlemage", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("ARC A7", "ARC A5", "ARC A3", "ALCHEMIST", "DG2")):
            a = ARCHITECTURES["Intel Alchemist"]
            return "Intel Alchemist", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("METEOR LAKE", "LUNAR LAKE", "ARROW LAKE", "CORE ULTRA")):
            a = ARCHITECTURES["Intel Meteor/Lunar Lake"]
            return "Intel Core Ultra", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("IRIS XE", "TIGER LAKE", "ALDER LAKE", "RAPTOR LAKE", "GEN12")):
            a = ARCHITECTURES["Intel Iris Xe"]
            return "Intel Iris Xe", a["description"], a["recommended_package"], a["reason"]
        if any(k in name_upper for k in ("UHD", "HD GRAPHICS", "SKYLAKE", "KABY LAKE", "COFFEE LAKE")):
            a = ARCHITECTURES["Intel UHD"]
            return "Intel UHD", a["description"], a["recommended_package"], a["reason"]

        a = ARCHITECTURES["Intel Iris Xe"]
        return "Intel Graphics", _("Intel Grafik Mimarisi"), "vulkan-intel", _("Mesa ANV Vulkan ve Intel Media Driver önerilmektedir.")

    return "Graphics Adapter", _("Genel Grafik Kartı"), "vulkan-radeon", _("Standart grafik sürücüsü")


def read_sysfs_file(path):
    """Safely read string from a sysfs file."""
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read().strip()
        except OSError:
            pass
    return None


def detect_all_system_gpus():
    """
    Comprehensive scan of all graphics adapters on the system.
    Returns a list of dictionaries with details for AMD, Intel, etc.
    """
    gpus = []
    pci_dev_path = "/sys/bus/pci/devices/"
    pci_db = get_pci_database()

    if os.path.isdir(pci_dev_path):
        for slot in sorted(os.listdir(pci_dev_path)):
            dev_path = os.path.join(pci_dev_path, slot)
            class_str = read_sysfs_file(os.path.join(dev_path, "class"))
            if not class_str or not class_str.startswith("0x03"):
                continue

            vendor_str = read_sysfs_file(os.path.join(dev_path, "vendor"))
            device_str = read_sysfs_file(os.path.join(dev_path, "device"))
            if not vendor_str or not device_str:
                continue

            try:
                v_id = int(vendor_str, 16)
                d_id = int(device_str, 16)
            except ValueError:
                continue

            v_hex = f"{v_id:04X}"
            d_hex = f"{d_id:04X}"

            v_name = "AMD" if v_id == AMD_VENDOR_ID else ("Intel" if v_id == INTEL_VENDOR_ID else "Unknown")
            d_name = f"{v_name} Graphics Device"
            if v_id in pci_db:
                v_name = pci_db[v_id].get("vendor_name", v_name)
                d_name = pci_db[v_id].get("devices", {}).get(d_id, d_name)

            boot_vga = read_sysfs_file(os.path.join(dev_path, "boot_vga"))
            is_primary = (boot_vga == "1")

            driver_module = None
            driver_link = os.path.join(dev_path, "driver")
            if os.path.islink(driver_link):
                try:
                    driver_module = os.path.basename(os.readlink(driver_link))
                except OSError:
                    pass

            is_amd = (v_id == AMD_VENDOR_ID)
            is_intel = (v_id == INTEL_VENDOR_ID)

            arch, arch_desc, rec_pkg, rec_reason = identify_architecture(v_id, d_id, d_name)

            gpus.append({
                "pci_slot": slot,
                "vendor_id": v_id,
                "vendor_id_hex": v_hex,
                "vendor_name": v_name,
                "device_id": d_id,
                "device_id_hex": d_hex,
                "device_name": d_name,
                "is_primary": is_primary,
                "is_amd": is_amd,
                "is_intel": is_intel,
                "driver_module": driver_module,
                "driver_version": "Mesa 24.2",
                "architecture": arch,
                "architecture_desc": arch_desc,
                "recommended_driver": rec_pkg,
                "recommendation_reason": rec_reason,
            })

    # lspci fallback if sysfs is empty or restricted
    if not gpus and shutil_which("lspci"):
        try:
            out = subprocess.check_output(["lspci", "-nn", "-D"], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                line_lower = line.lower()
                if any(t in line_lower for t in ("vga compatible", "3d controller", "display controller")):
                    match = re.search(r"^([0-9a-fA-F:.]+)\s+([^:]+):\s+(.+?)\s+\[([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\]", line)
                    if match:
                        slot, _, name, v_hex, d_hex = match.groups()
                        v_id = int(v_hex, 16)
                        d_id = int(d_hex, 16)
                        is_amd = (v_id == AMD_VENDOR_ID)
                        is_intel = (v_id == INTEL_VENDOR_ID)
                        arch, arch_desc, rec_pkg, rec_reason = identify_architecture(v_id, d_id, name)
                        gpus.append({
                            "pci_slot": slot,
                            "vendor_id": v_id,
                            "vendor_id_hex": v_hex.upper(),
                            "vendor_name": "AMD" if is_amd else ("Intel" if is_intel else "Graphics Adapter"),
                            "device_id": d_id,
                            "device_id_hex": d_hex.upper(),
                            "device_name": name.strip(),
                            "is_primary": ("vga" in line_lower),
                            "is_amd": is_amd,
                            "is_intel": is_intel,
                            "driver_module": None,
                            "driver_version": None,
                            "architecture": arch,
                            "architecture_desc": arch_desc,
                            "recommended_driver": rec_pkg,
                            "recommendation_reason": rec_reason,
                        })
        except Exception:
            pass

    return gpus


def shutil_which(cmd):
    """Check if command exists in PATH."""
    for p in os.environ.get("PATH", "").split(os.path.pathsep):
        full = os.path.join(p, cmd)
        if os.path.isfile(full) and os.access(full, os.X_OK):
            return full
    return None


def get_detected_gpus():
    """Returns detected AMD and Intel graphics cards."""
    all_gpus = detect_all_system_gpus()
    return [g for g in all_gpus if g.get("is_amd") or g.get("is_intel")]


def tag_recommended_driver(driver_list, gpus=None):
    """
    Given a list of GpuDriver instances and detected GPUs, determines
    which driver is the best recommendation.
    """
    if not driver_list:
        return None

    for d in driver_list:
        if getattr(d, "is_recommended", False):
            return d

    if driver_list:
        driver_list[0].is_recommended = True
        return driver_list[0]
    return None


def generate_hardware_report():
    """
    Generates a full textual diagnostic report for CLI and UI inspector.
    """
    all_gpus = detect_all_system_gpus()
    lines = []
    lines.append("=" * 66)
    lines.append("  ParsLinux AMD & Intel Donanım Algılama Raporu")
    lines.append("=" * 66)

    if not all_gpus:
        lines.append("  [!] Sistemde hiçbir PCI grafik bağdaştırıcısı algılanamadı.")
        lines.append("=" * 66)
        return "\n".join(lines)

    lines.append(f"  Toplam Tespit Edilen Grafik Birimi: {len(all_gpus)}\n")
    for idx, g in enumerate(all_gpus):
        tag = "[Birincil Görüntü (Primary)]" if g["is_primary"] else "[İkincil / Harici (Discrete)]"
        lines.append(f"  GPU #{idx + 1}: {g['device_name']}")
        lines.append(f"    ├─ Durum:       {tag}")
        lines.append(f"    ├─ Üretici:     {g['vendor_name']} (0x{g['vendor_id_hex']})")
        lines.append(f"    ├─ Donanım ID:  {g['vendor_id_hex']}:{g['device_id_hex']}")
        lines.append(f"    ├─ PCI Veriyolu:{g['pci_slot']}")
        lines.append(f"    ├─ Aktif Modül: {g['driver_module'] or 'Yüklü Değil / Bilinmiyor'}")
        if g.get("architecture"):
            lines.append(f"    ├─ Mimari:      {g.get('architecture')}")
        if g.get("recommended_driver"):
            lines.append(f"    ├─ Önerilen:    {g.get('recommended_driver')}")
            lines.append(f"    └─ Gerekçe:     {g.get('recommendation_reason', 'Otomatik tespit')}")
        else:
            lines.append(f"    └─ Not:         Standart grafik bağdaştırıcı")
        lines.append("")

    lines.append("=" * 66)
    return "\n".join(lines)
