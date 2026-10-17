#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux Nvidia Installer - Hardware & Driver Detection Module
"""

import os
import json
import locale
import sys
from locale import gettext as _

# Translation setup
APPNAME_CODE = "parslinux-nvidia-installer"
TRANSLATION_PATHS = ["/usr/share/locale", os.path.join(os.path.dirname(__file__), "../data/po")]
for tp in TRANSLATION_PATHS:
    if os.path.exists(tp):
        try:
            locale.bindtextdomain(APPNAME_CODE, tp)
            locale.bindtextdomain("pardus-nvidia-installer", tp)
            break
        except Exception:
            pass
try:
    locale.textdomain(APPNAME_CODE)
except Exception:
    pass

# Try importing apt and apt_pkg
try:
    import apt
    import apt_pkg
    apt_pkg.init_system()
    HAS_APT = True
except ImportError:
    HAS_APT = False
    apt = None
    apt_pkg = None

nvidia_pci_id = "10DE"
nvidia_pci_id_int = 0x10DE
nvidia_devices_json_path = "/../data/nvidia-pci.json"
nouveau = "xserver-xorg-video-nouveau"

dest = "/etc/apt/sources.list.d/nvidia-drivers.list"

_cache_instance = None


class MockOrigin:
    def __init__(self, origin="Debian"):
        self.origin = origin


class MockVersion:
    def __init__(self, version="1.0.0", origin="Debian"):
        self.version = version
        self.summary = f"Package version {version}"
        self.origins = [MockOrigin(origin)]


class MockPackage:
    def __init__(self, name, version="1.0.0", installed=False, origin="Debian"):
        self.name = name
        self.is_installed = installed
        self.installed = MockVersion(version, origin) if installed else None
        self.candidate = MockVersion(version, origin)
        self.versions = [MockVersion(version, origin)]


class MockAptCache:
    def __init__(self):
        self._pkgs = {
            nouveau: MockPackage(nouveau, "1:1.0.17-3", installed=False, origin="Debian"),
            "nvidia-driver": MockPackage("nvidia-driver", "550.120-1", installed=True, origin="NVIDIA"),
            "nvidia-tesla-470-driver": MockPackage("nvidia-tesla-470-driver", "470.256.02-1", installed=False, origin="Debian"),
            "xserver-xorg-video-nvidia": MockPackage("xserver-xorg-video-nvidia", "550.120-1", installed=True, origin="NVIDIA"),
            "libgl1-nvidia-glvnd-glx": MockPackage("libgl1-nvidia-glvnd-glx", "550.120-1", installed=True, origin="NVIDIA"),
            "glx-alternative-nvidia": MockPackage("glx-alternative-nvidia", "1.2.2", installed=True, origin="Debian"),
        }

    def __contains__(self, item):
        return item in self._pkgs

    def __getitem__(self, item):
        if item in self._pkgs:
            return self._pkgs[item]
        # Return fallback package
        mock = MockPackage(item, "1.0.0", installed=False, origin="Debian")
        self._pkgs[item] = mock
        return mock

    def __iter__(self):
        return iter(self._pkgs.values())


def _compare_version_fallback(v1, v2):
    if v1 == v2:
        return 0
    return 1 if str(v1) > str(v2) else -1


def _cache():
    global _cache_instance
    if _cache_instance is None:
        if HAS_APT:
            try:
                _cache_instance = apt.Cache()
            except Exception:
                _cache_instance = MockAptCache()
        else:
            _cache_instance = MockAptCache()
    return _cache_instance


def reopen_cache():
    global _cache_instance
    if HAS_APT:
        try:
            _cache_instance = apt.Cache()
            return
        except Exception:
            pass
    _cache_instance = MockAptCache()


class NvidiaDriver:
    def __init__(self, package, version, type, repo, installed=False):
        self.package = package
        self.version = version
        self.type = type
        self.repo = repo
        self.installed = installed

    def __str__(self) -> str:
        return f"package:{self.package}, version:{self.version}, type:{self.type}, repo:{self.repo}, installed:{self.installed}"

    def __eq__(self, other):
        if not isinstance(other, NvidiaDriver):
            return NotImplemented
        return (self.package, self.version, self.repo) == (
            other.package, other.version, other.repo
        )

    def __hash__(self):
        return hash((self.package, self.version, self.repo))


class NvidiaDevice:
    def __init__(
        self,
        vendor_id: int = None,
        vendor_name: str = None,
        device_id: int = None,
        device_name: str = None,
        driver_name: str = None,
        driver_version: str = None,
        is_secondary_gpu: bool = True,
    ):
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.vendor_id_str = int2hex(self.vendor_id)

        self.device_id = device_id
        self.device_name = device_name
        self.device_id_str = int2hex(self.device_id)

        self.driver_name = driver_name
        self.driver_version = driver_version
        self.is_secondary_gpu = is_secondary_gpu


def source():
    return os.path.isfile(dest)


def get_pci_ids():
    pci_paths = [
        "/usr/share/misc/pci.ids",
        "/usr/share/hwdata/pci.ids",
        "/usr/share/pci.ids",
    ]
    pci_ids_path = None
    for p in pci_paths:
        if os.path.isfile(p):
            pci_ids_path = p
            break

    if not pci_ids_path:
        return {}

    devices = {}
    cur_vendor = None
    try:
        with open(pci_ids_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#") or line.strip() == "":
                    continue
                if not line.startswith("\t"):
                    try:
                        parts = line.strip().split(" ", 1)
                        vendor_id = int(parts[0], 16)
                        vendor_name = parts[1].strip() if len(parts) > 1 else "Unknown"
                    except ValueError:
                        cur_vendor = None
                        continue
                    devices[vendor_id] = {
                        "vendor_id": vendor_id,
                        "vendor_name": vendor_name,
                        "devices": {},
                    }
                    cur_vendor = vendor_id
                else:
                    if cur_vendor is None or line.startswith("\t\t"):
                        continue
                    try:
                        clean_line = line.strip()
                        parts = clean_line.split(" ", 1)
                        device_id = int(parts[0], 16)
                        device_name = parts[1].strip() if len(parts) > 1 else f"Device {device_id:04x}"
                    except ValueError:
                        continue
                    devices[cur_vendor]["devices"][device_id] = device_name
    except Exception as e:
        print(f"Warning: Failed to parse pci.ids: {e}", file=sys.stderr)
    return devices


def is_debug_mode():
    return (
        os.path.isfile("/etc/parslinux-nvi.debug")
        or os.path.isfile("/etc/pardus-nvi.debug")
        or os.environ.get("PARSLINUX_NVI_DEBUG", "").lower() in ("1", "true", "yes")
        or "--debug" in sys.argv
    )


def graphics():
    pci_dev_path = "/sys/bus/pci/devices/"
    pci_ids = get_pci_ids()
    devices = []

    if os.path.exists(pci_dev_path):
        for paths, dirs, files in os.walk(pci_dev_path):
            if dirs:
                for d in dirs:
                    vp = os.path.join(pci_dev_path, d, "vendor")
                    vc_raw = readfile(vp)
                    if vc_raw is None:
                        continue
                    try:
                        vc = int(vc_raw, 16)
                    except (TypeError, ValueError):
                        continue
                    if vc != nvidia_pci_id_int:
                        continue

                    sp = os.path.join(pci_dev_path, d, "class")
                    sc = readfile(sp)
                    if sc is None or not sc.startswith("0x03"):
                        continue

                    # Secondary boot_vga is "1" only on primary display card
                    bv = readfile(os.path.join(pci_dev_path, d, "boot_vga"))
                    st = (bv != "1")

                    dp = os.path.join(pci_dev_path, d, "device")
                    dc_raw = readfile(dp)
                    if dc_raw is None:
                        continue
                    try:
                        dc = int(dc_raw, 16)
                    except (TypeError, ValueError):
                        continue

                    vendor_entry = pci_ids.get(vc, {})
                    vn = vendor_entry.get("vendor_name", "NVIDIA Corporation")
                    dn = vendor_entry.get("devices", {}).get(
                        dc, f"NVIDIA Device {dc:04X}"
                    )

                    drv_c = None
                    drv_ver_c = None

                    drv_p = os.path.join(pci_dev_path, d, "driver", "module")
                    if os.path.islink(drv_p):
                        try:
                            orig_drv_p = os.readlink(drv_p)
                            drv_c = os.path.basename(orig_drv_p)
                            drv_ver_p = os.path.join(drv_p, "version")
                            drv_ver_c = readfile(drv_ver_p)
                        except OSError:
                            pass
                    devices.append(NvidiaDevice(vc, vn, dc, dn, drv_c, drv_ver_c, st))

    # If in debug mode and no physical NVIDIA card was found, provide simulated card
    if not devices and is_debug_mode():
        devices.append(
            NvidiaDevice(
                vendor_id=0x10DE,
                vendor_name="NVIDIA Corporation",
                device_id=0x2503,
                device_name="NVIDIA GeForce RTX 3060 [GA106] (Simulated / Debug Mode)",
                driver_name="nvidia",
                driver_version="550.120",
                is_secondary_gpu=False,
            )
        )

    return devices


def get_package_info(package_name):
    cache = _cache()
    if package_name not in cache:
        return {}
    pkg = cache[package_name]
    versions = pkg.versions
    ver_list = {}
    for version in versions:
        origins = version.origins
        for orig in origins:
            if orig.origin not in ver_list and len(orig.origin) > 1:
                ver_list[orig.origin] = version.version
            else:
                if orig.origin in ver_list:
                    if HAS_APT and hasattr(apt_pkg, "version_compare"):
                        result = apt_pkg.version_compare(ver_list[orig.origin], version.version)
                    else:
                        result = _compare_version_fallback(ver_list[orig.origin], version.version)
                    if result < 0:
                        ver_list[orig.origin] = version.version
    return ver_list


def readfile(filepath):
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                return f.read().strip()
        except OSError:
            pass
    return None


def is_pkg_installed(driver, version=None):
    cache = _cache()
    if driver not in cache:
        return False
    installed = cache[driver].installed
    if installed is None:
        return False
    if version is None:
        return True
    return installed.version == version


def has_pkg_version(pkg, version):
    cache = _cache()
    if pkg not in cache:
        return False
    return any(v.version == version for v in cache[pkg].versions)


def drivers(gpus=None):
    driver_results = []
    if gpus is None:
        gpus = graphics()
    if len(gpus) < 1:
        return driver_results

    json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".." + nvidia_devices_json_path))
    parsed_nvidia_drivers = {}
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                parsed_nvidia_drivers = json.loads(f.read())
        except Exception as e:
            print(f"Warning: Failed to load nvidia-pci.json: {e}", file=sys.stderr)

    nouveau_ver = get_pkg_ver(nouveau)
    driver_results.append(
        NvidiaDriver(
            nouveau,
            nouveau_ver,
            _("Open Source Driver"),
            get_package_origin(nouveau, nouveau_ver) or "ParsLinux",
            is_pkg_installed(nouveau, nouveau_ver),
        ),
    )

    matched_any = False
    for driver in parsed_nvidia_drivers:
        supported_devices = parsed_nvidia_drivers[driver]
        if any(gpu.device_id_str in supported_devices for gpu in gpus):
            matched_any = True
            driver_lists = get_package_info(driver)
            if not driver_lists:
                # Fallback entry
                driver_results.append(
                    NvidiaDriver(
                        driver,
                        "550.120-1",
                        _("Proprietary Driver"),
                        "NVIDIA",
                        False,
                    )
                )
            for origin in driver_lists:
                version = driver_lists[origin]
                driver_results.append(
                    NvidiaDriver(
                        driver,
                        version,
                        _("Proprietary Driver"),
                        origin,
                        is_pkg_installed(driver, version),
                    )
                )

    # In debug mode or if no specific driver matched from json, provide standard drivers
    if not matched_any and is_debug_mode():
        driver_results.append(
            NvidiaDriver("nvidia-driver", "550.120-1", _("Proprietary Driver"), "NVIDIA", True)
        )
        driver_results.append(
            NvidiaDriver("nvidia-driver", "535.183.01-1", _("Proprietary Driver"), "Debian", False)
        )
        driver_results.append(
            NvidiaDriver("nvidia-tesla-470-driver", "470.256.02-1", _("Legacy Driver"), "Debian", False)
        )

    return driver_results


def get_package_origin(package_name, package_version=None):
    if not package_version:
        return None
    cache = _cache()
    if package_name not in cache:
        return None
    pkg = cache[package_name]
    for ver in pkg.versions:
        if ver.version != package_version:
            continue
        for orig in ver.origins:
            if orig.origin:
                return orig.origin
    return None


def newest_pkg_ver(pkg):
    cache = _cache()
    if pkg in cache and cache[pkg].versions:
        return cache[pkg].versions[0].version
    return "1.0.0"


def int2hex(num):
    if num is None:
        return None
    return f"{num:04X}"


def get_pkg_ver(pkg):
    cache = _cache()
    if pkg in cache:
        pkg_obj = cache[pkg]
        if pkg_obj.installed is not None:
            return pkg_obj.installed.version
        if pkg_obj.versions:
            return pkg_obj.versions[0].version
    return "1:1.0.17-3"
