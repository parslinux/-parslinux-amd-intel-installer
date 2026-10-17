#!/usr/bin/env bash
# ==============================================================================
# ParsLinux Nvidia Installer - System Uninstallation Script
# ==============================================================================
set -e

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

echo -e "${CYAN}${BOLD}=== ParsLinux Nvidia Installer — Uninstaller ===${NC}"

echo -e "${YELLOW}Stopping any running processes...${NC}"
./stop.sh 2>/dev/null || true

echo -e "${BLUE}▶ Removing installed files...${NC}"

sudo rm -f /usr/bin/parslinux-nvidia-installer
sudo rm -f /usr/bin/pardus-nvidia-installer
sudo rm -rf /usr/share/parslinux/parslinux-nvidia-installer
sudo rm -rf /usr/share/pardus/pardus-nvidia-installer
sudo rm -f /usr/share/applications/org.parslinux.nvidia-installer.desktop
sudo rm -f /usr/share/applications/tr.org.pardus.pardus-nvidia-installer.desktop
sudo rm -f /usr/share/metainfo/org.parslinux.nvidia-installer.metainfo.xml
sudo rm -f /usr/share/polkit-1/actions/org.parslinux.pkexec.parslinux-nvidia-installer.policy
sudo rm -f /usr/share/polkit-1/actions/tr.org.pardus.pkexec.pardus-nvidia-installer.policy
sudo rm -f /usr/share/icons/hicolor/scalable/apps/parslinux-nvidia-installer.svg
sudo rm -f /usr/share/icons/hicolor/scalable/apps/pardus-nvidia-installer.svg
sudo rm -f /lib/systemd/system/pni-disable-gpu.service
sudo rm -f /usr/share/locale/*/LC_MESSAGES/parslinux-nvidia-installer.mo
sudo rm -f /usr/share/locale/*/LC_MESSAGES/pardus-nvidia-installer.mo

# Clean python-egg-info
sudo rm -rf /usr/lib/python*/dist-packages/parslinux_nvidia_installer* 2>/dev/null || true
sudo rm -rf /usr/lib/python*/site-packages/parslinux_nvidia_installer* 2>/dev/null || true

echo -e "${BLUE}▶ Updating caches...${NC}"
sudo update-desktop-database -q /usr/share/applications 2>/dev/null || true
sudo systemctl daemon-reload 2>/dev/null || true

echo -e "${GREEN}${BOLD}✓ ParsLinux Nvidia Installer has been cleanly uninstalled from your system.${NC}"
