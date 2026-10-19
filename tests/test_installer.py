#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux AMD & Intel Installer - Unit & Integration Test Suite
"""
import unittest
import os
import sys
import xml.etree.ElementTree as ET

# Add src to path
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import amd_intel
import detector
import monitor
import package


class TestGpuModel(unittest.TestCase):
    def test_amd_device_model(self):
        dev = amd_intel.GpuDevice(
            vendor_id=0x1002,
            vendor_name="Advanced Micro Devices, Inc.",
            device_id=0x73DF,
            device_name="Radeon RX 6700 XT",
            driver_name="amdgpu",
            driver_version="Mesa 24.2.4",
            is_secondary_gpu=False,
            is_boot_vga=True,
            architecture="RDNA 2",
        )
        self.assertEqual(dev.vendor_id_str, "1002")
        self.assertEqual(dev.device_id_str, "73DF")
        self.assertFalse(dev.is_secondary_gpu)
        self.assertEqual(dev.device_name, "Radeon RX 6700 XT")

    def test_intel_device_model(self):
        dev = amd_intel.GpuDevice(
            vendor_id=0x8086,
            vendor_name="Intel Corporation",
            device_id=0x9A49,
            device_name="TigerLake-LP GT2 [Iris Xe Graphics]",
            driver_name="i915",
            driver_version="Mesa 24.2.4",
            is_secondary_gpu=True,
            is_boot_vga=False,
            architecture="Gen12 Xe",
        )
        self.assertEqual(dev.vendor_id_str, "8086")
        self.assertEqual(dev.device_id_str, "9A49")
        self.assertTrue(dev.is_secondary_gpu)

    def test_int2hex(self):
        self.assertEqual(amd_intel.int2hex(0x1002), "1002")
        self.assertEqual(amd_intel.int2hex(0x8086), "8086")
        self.assertEqual(amd_intel.int2hex(0x00FF), "00FF")
        self.assertEqual(amd_intel.int2hex(0), "0000")
        self.assertIsNone(amd_intel.int2hex(None))

    def test_debug_mode_graphics(self):
        os.environ["PARSLINUX_DEBUG"] = "1"
        try:
            gpus = amd_intel.graphics()
            self.assertGreater(len(gpus), 0)
            self.assertTrue(any(g.vendor_id in (0x1002, 0x8086) for g in gpus))

            mock_gpus = [
                amd_intel.GpuDevice(vendor_id=0x1002, vendor_name="AMD"),
                amd_intel.GpuDevice(vendor_id=0x8086, vendor_name="Intel")
            ]
            drvs = amd_intel.drivers(mock_gpus)
            self.assertGreater(len(drvs), 0)
            pkg_names = [d.package for d in drvs]
            self.assertIn("vulkan-radeon", pkg_names)
            self.assertIn("vulkan-intel", pkg_names)
        finally:
            os.environ.pop("PARSLINUX_DEBUG", None)


class TestPackageSecurity(unittest.TestCase):
    def test_allowed_package_names(self):
        self.assertTrue(package._is_allowed_package("vulkan-radeon"))
        self.assertTrue(package._is_allowed_package("vulkan-intel"))
        self.assertTrue(package._is_allowed_package("mesa-va-drivers"))
        self.assertTrue(package._is_allowed_package("intel-media-driver"))
        self.assertTrue(package._is_allowed_package("rocm-opencl-runtime"))
        self.assertTrue(package._is_allowed_package("intel-compute-runtime"))
        self.assertTrue(package._is_allowed_package("mangohud"))
        self.assertTrue(package._is_allowed_package("timeshift"))

    def test_command_injection_rejection(self):
        self.assertFalse(package._is_allowed_package("vulkan-radeon; rm -rf /"))
        self.assertFalse(package._is_allowed_package("mesa-va-drivers && reboot"))
        self.assertFalse(package._is_allowed_package("../../etc/passwd"))
        self.assertFalse(package._is_allowed_package("vulkan-intel|reboot"))

    def test_package_version_split(self):
        name, ver = package._split_pkg("vulkan-radeon=24.2.4-1")
        self.assertEqual(name, "vulkan-radeon")
        self.assertEqual(ver, "24.2.4-1")


class TestDetector(unittest.TestCase):
    def test_architecture_identification_amd(self):
        arch, desc, rec_pkg, _ = detector.identify_architecture(0x1002, 0x73DF, "Navi 22 [Radeon RX 6700 XT]")
        self.assertEqual(arch, "RDNA 2")
        self.assertEqual(rec_pkg, "vulkan-radeon")

    def test_architecture_identification_intel(self):
        arch, desc, rec_pkg, _ = detector.identify_architecture(0x8086, 0x9A49, "TigerLake-LP GT2 [Iris Xe Graphics]")
        self.assertEqual(arch, "Intel Iris Xe")
        self.assertEqual(rec_pkg, "vulkan-intel")

    def test_hardware_report_generation(self):
        report = detector.generate_hardware_report()
        self.assertIn("ParsLinux", report)


class TestMonitor(unittest.TestCase):
    def test_prime_profile_detection(self):
        profile = monitor.get_prime_profile()
        self.assertIn(profile, ("integrated", "hybrid", "performance"))

    def test_simulated_telemetry(self):
        telemetry = monitor.get_gpu_telemetry(simulated=True)
        self.assertTrue(telemetry["available"])
        self.assertTrue(telemetry["simulated"])
        self.assertGreater(telemetry["temp"], 30)
        self.assertLess(telemetry["temp"], 100)

    def test_gaming_status(self):
        status = monitor.get_gaming_status()
        self.assertIn("launchers", status)
        self.assertIn("global_offload", status)


class TestFilesystemIntegration(unittest.TestCase):
    def test_desktop_file_valid(self):
        desktop_file = os.path.join(PROJECT_DIR, "org.parslinux.amd-intel-installer.desktop")
        self.assertTrue(os.path.isfile(desktop_file))
        with open(desktop_file, "r") as f:
            content = f.read()
        self.assertIn("Exec=parslinux-amd-intel-installer", content)
        self.assertIn("Icon=parslinux-amd-intel-installer", content)

    def test_polkit_policy_valid_xml(self):
        policy_file = os.path.join(PROJECT_DIR, "org.parslinux.pkexec.parslinux-amd-intel-installer.policy")
        self.assertTrue(os.path.isfile(policy_file))
        tree = ET.parse(policy_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "policyconfig")

    def test_svg_icon_valid_xml(self):
        icon_path = os.path.join(PROJECT_DIR, "parslinux-amd-intel-installer.svg")
        self.assertTrue(os.path.isfile(icon_path))
        tree = ET.parse(icon_path)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"))


if __name__ == "__main__":
    unittest.main()
