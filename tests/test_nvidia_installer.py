#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ParsLinux Nvidia Installer - Unit & Integration Test Suite
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

import nvidia
import package

class TestNvidiaModel(unittest.TestCase):
    def test_nvidia_device_model(self):
        dev = nvidia.NvidiaDevice(
            vendor_id=0x10DE,
            vendor_name="NVIDIA Corporation",
            device_id=0x2503,
            device_name="GeForce RTX 3060",
            driver_name="nvidia",
            driver_version="550.120",
            is_secondary_gpu=False,
        )
        self.assertEqual(dev.vendor_id_str, "10DE")
        self.assertEqual(dev.device_id_str, "2503")
        self.assertFalse(dev.is_secondary_gpu)
        self.assertEqual(dev.device_name, "GeForce RTX 3060")

    def test_int2hex(self):
        self.assertEqual(nvidia.int2hex(0x10DE), "10DE")
        self.assertEqual(nvidia.int2hex(0x00FF), "00FF")
        self.assertEqual(nvidia.int2hex(0), "0000")
        self.assertIsNone(nvidia.int2hex(None))

    def test_nvidia_driver_equality(self):
        d1 = nvidia.NvidiaDriver("nvidia-driver", "550.120", "Proprietary", "NVIDIA", True)
        d2 = nvidia.NvidiaDriver("nvidia-driver", "550.120", "Proprietary", "NVIDIA", False)
        d3 = nvidia.NvidiaDriver("nvidia-driver", "535.183", "Proprietary", "Debian", False)
        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)
        self.assertIn("nvidia-driver", str(d1))

    def test_debug_mode_graphics(self):
        # Enable debug flag
        os.environ["PARSLINUX_NVI_DEBUG"] = "1"
        try:
            gpus = nvidia.graphics()
            self.assertGreater(len(gpus), 0)
            self.assertTrue(any("NVIDIA" in g.vendor_name or "NVIDIA" in g.device_name for g in gpus))
            
            # Drivers detection with simulated GPUs
            drvs = nvidia.drivers(gpus)
            self.assertGreater(len(drvs), 0)
            pkg_names = [d.package for d in drvs]
            self.assertIn("xserver-xorg-video-nouveau", pkg_names)
        finally:
            os.environ.pop("PARSLINUX_NVI_DEBUG", None)


class TestPackageSecurity(unittest.TestCase):
    def test_allowed_package_names(self):
        self.assertTrue(package._is_allowed_package("xserver-xorg-video-nouveau"))
        self.assertTrue(package._is_allowed_package("nvidia-driver"))
        self.assertTrue(package._is_allowed_package("nvidia-tesla-470-driver"))
        self.assertTrue(package._is_allowed_package("nvidia-driver=550.120-1"))
        self.assertTrue(package._is_allowed_package("linux-headers-6.6.0-pars-amd64"))

    def test_rejected_unsafe_package_names(self):
        # Prevent option injection or path traversal
        self.assertFalse(package._is_allowed_package("--reinstall"))
        self.assertFalse(package._is_allowed_package("curl"))
        self.assertFalse(package._is_allowed_package("../../../etc/shadow"))
        self.assertFalse(package._is_allowed_package("nvidia-driver; rm -rf /"))
        self.assertFalse(package._is_allowed_package(""))
        self.assertFalse(package._is_allowed_package("nvidia-driver=550.120;reboot"))

    def test_split_pkg(self):
        name, ver = package._split_pkg("nvidia-driver=550.120-1")
        self.assertEqual(name, "nvidia-driver")
        self.assertEqual(ver, "550.120-1")

        name2, ver2 = package._split_pkg("xserver-xorg-video-nouveau")
        self.assertEqual(name2, "xserver-xorg-video-nouveau")
        self.assertIsNone(ver2)

    def test_cuda_repo_distro_detection(self):
        distro = package.cuda_repo_distro()
        self.assertTrue(distro.startswith("debian"))
        self.assertIn(distro, ("debian12", "debian13"))


class TestMonitorAndTelemetry(unittest.TestCase):
    def test_gpu_telemetry_simulated(self):
        import monitor
        data = monitor.get_gpu_telemetry(simulated=True)
        self.assertTrue(data["available"])
        self.assertTrue(data["simulated"])
        self.assertIn("RTX 4070 Ti", data["name"])
        self.assertGreaterEqual(data["temp"], 30)
        self.assertLessEqual(data["temp"], 90)
        self.assertGreater(data["vram_total"], 0)
        self.assertGreaterEqual(data["vram_used"], 0)
        self.assertGreaterEqual(data["power"], 10)

    def test_prime_profile_detection(self):
        import monitor
        profile = monitor.get_prime_profile()
        self.assertIn(profile, ("integrated", "on-demand", "nvidia"))

    def test_ai_stack_detection(self):
        import monitor
        status = monitor.get_ai_stack_status()
        self.assertIn("cuda", status)
        self.assertIn("cudnn", status)
        self.assertIn("tensorrt", status)
        self.assertIn("installed", status["cuda"])

    def test_prime_mode_validation(self):
        self.assertFalse(package.set_prime_mode("invalid_mode"))
        self.assertFalse(package.set_prime_mode(""))

    def test_ai_package_whitelisting(self):
        self.assertTrue(package._is_allowed_package("nvidia-cuda-toolkit"))
        self.assertTrue(package._is_allowed_package("libcudnn8"))
        self.assertTrue(package._is_allowed_package("libcudnn8-dev"))
        self.assertTrue(package._is_allowed_package("libnvinfer8"))
        self.assertTrue(package._is_allowed_package("tensorrt"))
        self.assertTrue(package._is_allowed_package("nvidia-prime"))


class TestMetadataAndFiles(unittest.TestCase):
    def test_desktop_file_syntax(self):
        desktop_file = os.path.join(PROJECT_DIR, "org.parslinux.nvidia-installer.desktop")
        self.assertTrue(os.path.isfile(desktop_file))
        with open(desktop_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=ParsLinux Nvidia Installer", content)
        self.assertIn("Exec=parslinux-nvidia-installer", content)
        self.assertIn("Icon=parslinux-nvidia-installer", content)

    def test_polkit_policy_syntax(self):
        policy_file = os.path.join(PROJECT_DIR, "org.parslinux.pkexec.parslinux-nvidia-installer.policy")
        self.assertTrue(os.path.isfile(policy_file))
        tree = ET.parse(policy_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "policyconfig")
        action_ids = [a.attrib.get("id") for a in root.findall("action")]
        self.assertIn("org.parslinux.pkexec.parslinux-nvidia-installer", action_ids)

    def test_metainfo_xml_syntax(self):
        metainfo_file = os.path.join(PROJECT_DIR, "data/org.parslinux.nvidia-installer.metainfo.xml")
        self.assertTrue(os.path.isfile(metainfo_file))
        tree = ET.parse(metainfo_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "component")
        self.assertEqual(root.find("id").text, "org.parslinux.nvidia-installer")

    def test_glade_ui_files_valid_xml(self):
        for glade in ("ui/ui.glade", "ui/driver_toggle.glade"):
            path = os.path.join(PROJECT_DIR, glade)
            self.assertTrue(os.path.isfile(path))
            tree = ET.parse(path)
            self.assertEqual(tree.getroot().tag, "interface")


if __name__ == "__main__":
    unittest.main()
