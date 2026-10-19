#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Hardware & Driver Detection Module
"""

import os
import sys
import locale
import subprocess
from locale import gettext as _

# Translation setup
APPNAME_CODE = "parslinux-amd-intel-installer"
TRANSLATION_PATHS = ["/usr/share/locale", os.path.join(os.path.dirname(__file__), "../data/po")]
for tp in TRANSLATION_PATHS:
    if os.path.exists(tp):
        try:
            locale.bindtextdomain(APPNAME_CODE, tp)
            break
        except Exception:
            pass
try:
    locale.textdomain(APPNAME_CODE)
except Exception:
    pass

AMD_VENDOR_ID = 0x1002
INTEL_VENDOR_ID = 0x8086

# Try importing apt and apt_pkg for Debian systems
try:
    import apt  # type: ignore
    import apt_pkg  # type: ignore
    apt_pkg.init_system()
    HAS_APT = True
except (ImportError, AttributeError):
    HAS_APT = False
    apt = None
    apt_pkg = None

_cache_instance = None


class MockOrigin:
    def __init__(self, origin="ParsLinux"):
        self.origin = origin


class MockVersion:
    def __init__(self, version="1.0.0", origin="ParsLinux"):
        self.version = version
        self.summary = f"Package version {version}"
        self.origins = [MockOrigin(origin)]


class MockPackage:
    def __init__(self, name, version="24.2.0-1", installed=False, origin="ParsLinux"):
        self.name = name
        self.is_installed = installed
        self.versions = [MockVersion(version, origin)]
        self.candidate = self.versions[0]


class MockAptCache:
    def __init__(self):
        self._pkgs = {
            "vulkan-radeon": MockPackage("vulkan-radeon", "24.2.4-1", installed=True),
            "vulkan-intel": MockPackage("vulkan-intel", "24.2.4-1", installed=True),
            "mesa-va-drivers": MockPackage("mesa-va-drivers", "24.2.4-1", installed=True),
            "intel-media-driver": MockPackage("intel-media-driver", "24.3.3-1", installed=True),
            "mesa-vdpau-drivers": MockPackage("mesa-vdpau-drivers", "24.2.4-1", installed=False),
            "rocm-opencl-runtime": MockPackage("rocm-opencl-runtime", "6.2.0-1", installed=False),
            "intel-compute-runtime": MockPackage("intel-compute-runtime", "24.35.3-1", installed=False),
        }

    def __contains__(self, item):
        return item in self._pkgs

    def __getitem__(self, item):
        return self._pkgs.get(item, MockPackage(item, "1.0.0", installed=False))

    def get(self, item, default=None):
        return self._pkgs.get(item, default)

    def open(self):
        pass

    def close(self):
        pass


def get_cache():
    global _cache_instance
    if _cache_instance is not None:
        return _cache_instance

    if HAS_APT and os.path.exists("/var/lib/dpkg/status"):
        try:
            _cache_instance = apt.Cache()
            return _cache_instance
        except Exception:
            pass

    _cache_instance = MockAptCache()
    return _cache_instance


def reopen_cache():
    global _cache_instance
    if _cache_instance is not None:
        try:
            _cache_instance.open()
        except Exception:
            _cache_instance = MockAptCache()
    else:
        _cache_instance = get_cache()


def int2hex(number):
    if number is None:
        return None
    hex_str = hex(number)[2:].upper()
    return hex_str.zfill(4)


class GpuDriver:
    def __init__(
        self,
        package: str,
        version: str = "1.0.0",
        driver_type: str = "Open Source",
        repo: str = "ParsLinux",
        installed: bool = False,
        is_recommended: bool = False,
        recommendation_reason: str = "",
    ):
        self.package = package
        self.version = version
        self.type = driver_type
        self.repo = repo
        self.installed = installed
        self.is_recommended = is_recommended
        self.recommendation_reason = recommendation_reason

    def __str__(self):
        return f"{self.package} ({self.version})"

    def __repr__(self):
        return f"<GpuDriver package={self.package} version={self.version} installed={self.installed}>"


class GpuDevice:
    def __init__(
        self,
        vendor_id: int = 0x1002,
        vendor_name: str = "AMD",
        device_id: int = 0x73DF,
        device_name: str = "Radeon RX 6700 XT",
        driver_name: str = "amdgpu",
        driver_version: str = "24.2.0",
        is_secondary_gpu: bool = False,
        is_boot_vga: bool = True,
        pci_slot: str = "0000:03:00.0",
        architecture: str = "RDNA 2",
        architecture_desc: str = "RDNA 2 Architecture",
        recommended_driver: str = "vulkan-radeon",
        recommendation_reason: str = "Tavsiye edilen açık kaynak Vulkan sürücüsü",
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
        self.is_boot_vga = is_boot_vga
        self.pci_slot = pci_slot
        self.architecture = architecture
        self.architecture_desc = architecture_desc
        self.recommended_driver = recommended_driver
        self.recommendation_reason = recommendation_reason

    def __str__(self):
        return f"{self.vendor_name} {self.device_name} [{self.vendor_id_str}:{self.device_id_str}]"


def source():
    """Returns True if extra package repositories are configured."""
    return os.path.isfile("/etc/parslinux-amd-intel-installer.conf")


def is_debug_mode():
    return (
        os.environ.get("PARSLINUX_DEBUG") == "1"
        or os.environ.get("PARSLINUX_NVI_DEBUG") == "1"
        or os.path.isfile("/etc/parslinux-debug")
    )


def is_parslinux():
    for f in ("/etc/parslinux_version", "/etc/os-release"):
        if os.path.isfile(f):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    if "parslinux" in fp.read().lower():
                        return True
            except OSError:
                pass
    return True


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
                    parts = line.strip().split(" ", 1)
                    try:
                        v_id = int(parts[0], 16)
                        v_name = parts[1].strip() if len(parts) > 1 else "Unknown"
                        devices[v_id] = {"vendor_name": v_name, "devices": {}}
                        cur_vendor = v_id
                    except ValueError:
                        cur_vendor = None
                else:
                    if cur_vendor is None or line.startswith("\t\t"):
                        continue
                    clean_line = line.strip()
                    parts = clean_line.split(" ", 1)
                    try:
                        d_id = int(parts[0], 16)
                        d_name = parts[1].strip() if len(parts) > 1 else f"Device {d_id:04x}"
                        devices[cur_vendor]["devices"][d_id] = d_name
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Warning: Failed to parse pci.ids: {e}", file=sys.stderr)
    return devices


def graphics():
    """
    Detect AMD and Intel GPUs on the system.
    If none found and debug mode is enabled, returns simulated AMD & Intel GPUs.
    """
    gpus = []
    pci_dev_path = "/sys/bus/pci/devices/"
    pci_db = get_pci_ids()

    if os.path.isdir(pci_dev_path):
        for dev in os.listdir(pci_dev_path):
            dev_full = os.path.join(pci_dev_path, dev)
            class_path = os.path.join(dev_full, "class")
            vendor_path = os.path.join(dev_full, "vendor")
            device_path = os.path.join(dev_full, "device")
            boot_vga_path = os.path.join(dev_full, "boot_vga")

            try:
                with open(class_path, "r") as f:
                    pci_class = f.read().strip()
            except OSError:
                continue

            # Check for display controller class (0x03xxxx)
            if not pci_class.startswith("0x03"):
                continue

            try:
                with open(vendor_path, "r") as f:
                    vendor_id = int(f.read().strip(), 16)
                with open(device_path, "r") as f:
                    device_id = int(f.read().strip(), 16)
            except (OSError, ValueError):
                continue

            # Filter for AMD or Intel
            if vendor_id not in (AMD_VENDOR_ID, INTEL_VENDOR_ID):
                continue

            vendor_name = "AMD" if vendor_id == AMD_VENDOR_ID else "Intel"
            device_name = f"{vendor_name} Graphics"
            if vendor_id in pci_db:
                vendor_name = pci_db[vendor_id].get("vendor_name", vendor_name)
                device_name = pci_db[vendor_id].get("devices", {}).get(device_id, device_name)

            is_boot_vga = False
            if os.path.isfile(boot_vga_path):
                try:
                    with open(boot_vga_path, "r") as f:
                        is_boot_vga = f.read().strip() == "1"
                except OSError:
                    pass

            driver_name = "amdgpu" if vendor_id == AMD_VENDOR_ID else "i915"
            driver_link = os.path.join(dev_full, "driver")
            if os.path.islink(driver_link):
                try:
                    driver_name = os.path.basename(os.readlink(driver_link))
                except OSError:
                    pass

            # Architecture info
            arch = "AMD Radeon" if vendor_id == AMD_VENDOR_ID else "Intel Xe"
            rec_pkg = "vulkan-radeon" if vendor_id == AMD_VENDOR_ID else "vulkan-intel"
            rec_reason = _("Resmi açık kaynak Vulkan sürücüsü")

            gpus.append(
                GpuDevice(
                    vendor_id=vendor_id,
                    vendor_name=vendor_name,
                    device_id=device_id,
                    device_name=device_name,
                    driver_name=driver_name,
                    driver_version="Mesa 24.2",
                    is_secondary_gpu=(not is_boot_vga and len(gpus) > 0),
                    is_boot_vga=is_boot_vga,
                    pci_slot=dev,
                    architecture=arch,
                    architecture_desc=arch,
                    recommended_driver=rec_pkg,
                    recommendation_reason=rec_reason,
                )
            )

    # Simulation fallback if no GPU or debug mode
    if (len(gpus) == 0 and is_debug_mode()) or (os.environ.get("PARSLINUX_NVI_DEBUG") == "1" and len(gpus) == 0):
        gpus = [
            GpuDevice(
                vendor_id=AMD_VENDOR_ID,
                vendor_name="Advanced Micro Devices, Inc. [AMD/ATI]",
                device_id=0x73DF,
                device_name="Navi 22 [Radeon RX 6700 XT / 6750 XT / 6800M]",
                driver_name="amdgpu",
                driver_version="Mesa 24.2.4",
                is_secondary_gpu=False,
                is_boot_vga=True,
                pci_slot="0000:03:00.0",
                architecture="RDNA 2",
                architecture_desc="RDNA 2 Architecture (Ray Tracing & FSR 3)",
                recommended_driver="vulkan-radeon",
                recommendation_reason=_("Mesa RADV Vulkan sürücüsü yüksek oyun performansı için önerilir."),
            ),
            GpuDevice(
                vendor_id=INTEL_VENDOR_ID,
                vendor_name="Intel Corporation",
                device_id=0x9A49,
                device_name="TigerLake-LP GT2 [Iris Xe Graphics]",
                driver_name="i915",
                driver_version="Mesa 24.2.4",
                is_secondary_gpu=True,
                is_boot_vga=False,
                pci_slot="0000:00:02.0",
                architecture="Gen12 Xe",
                architecture_desc="Intel Gen12 Xe Graphics Architecture",
                recommended_driver="vulkan-intel",
                recommendation_reason=_("Mesa ANV Vulkan sürücüsü ve VA-API hızlandırma önerilir."),
            ),
        ]

    return gpus


def drivers(gpus=None):
    """
    Return available packages (Vulkan, VA-API, Compute) for the detected hardware.
    """
    cache = get_cache()
    result = []

    has_amd = False
    has_intel = False
    if gpus:
        for g in gpus:
            if g.vendor_id == AMD_VENDOR_ID:
                has_amd = True
            elif g.vendor_id == INTEL_VENDOR_ID:
                has_intel = True
    else:
        has_amd = True
        has_intel = True

    if has_amd:
        # RADV
        p1 = cache.get("vulkan-radeon", None)
        ver1 = p1.candidate.version if p1 and p1.candidate else "24.2.4"
        inst1 = p1.is_installed if p1 else True
        result.append(
            GpuDriver(
                package="vulkan-radeon",
                version=ver1,
                driver_type=_("Açık Kaynak (Mesa RADV)"),
                repo="ParsLinux",
                installed=inst1,
                is_recommended=True,
                recommendation_reason=_("Valve ACO derleyicili en hızlı Vulkan sürücüsü"),
            )
        )

        # AMD VA-API
        p2 = cache.get("mesa-va-drivers", None)
        ver2 = p2.candidate.version if p2 and p2.candidate else "24.2.4"
        inst2 = p2.is_installed if p2 else True
        result.append(
            GpuDriver(
                package="mesa-va-drivers",
                version=ver2,
                driver_type=_("Donanım Video Hızlandırıcı (VA-API)"),
                repo="ParsLinux",
                installed=inst2,
                is_recommended=True,
                recommendation_reason=_("4K/8K tarayıcı ve video donanım hızlandırma"),
            )
        )

        # ROCm Compute
        p3 = cache.get("rocm-opencl-runtime", None)
        ver3 = p3.candidate.version if p3 and p3.candidate else "6.2.0"
        inst3 = p3.is_installed if p3 else False
        result.append(
            GpuDriver(
                package="rocm-opencl-runtime",
                version=ver3,
                driver_type=_("Hesaplama & Yapay Zeka (ROCm/OpenCL)"),
                repo="ParsLinux",
                installed=inst3,
                is_recommended=False,
                recommendation_reason=_("Blender ve PyTorch için OpenCL/HIP desteği"),
            )
        )

    if has_intel:
        # ANV
        p4 = cache.get("vulkan-intel", None)
        ver4 = p4.candidate.version if p4 and p4.candidate else "24.2.4"
        inst4 = p4.is_installed if p4 else True
        result.append(
            GpuDriver(
                package="vulkan-intel",
                version=ver4,
                driver_type=_("Açık Kaynak (Mesa ANV)"),
                repo="ParsLinux",
                installed=inst4,
                is_recommended=True,
                recommendation_reason=_("Intel Arc ve Iris Xe için resmi Vulkan sürücüsü"),
            )
        )

        # Intel QuickSync / VA-API
        p5 = cache.get("intel-media-driver", None)
        ver5 = p5.candidate.version if p5 and p5.candidate else "24.3.3"
        inst5 = p5.is_installed if p5 else True
        result.append(
            GpuDriver(
                package="intel-media-driver",
                version=ver5,
                driver_type=_("Intel QuickSync Donanım Hızlandırıcı"),
                repo="ParsLinux",
                installed=inst5,
                is_recommended=True,
                recommendation_reason=_("Intel Gen9+ ve Arc için donanım video çözme"),
            )
        )

        # Intel Compute Runtime
        p6 = cache.get("intel-compute-runtime", None)
        ver6 = p6.candidate.version if p6 and p6.candidate else "24.35.3"
        inst6 = p6.is_installed if p6 else False
        result.append(
            GpuDriver(
                package="intel-compute-runtime",
                version=ver6,
                driver_type=_("Intel oneAPI / OpenCL NEO Runtime"),
                repo="ParsLinux",
                installed=inst6,
                is_recommended=False,
                recommendation_reason=_("Intel Level Zero ve OpenCL hesaplama"),
            )
        )

    return result
