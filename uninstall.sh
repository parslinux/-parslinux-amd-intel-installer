#!/usr/bin/env bash
# ==============================================================================
# ParsLinux AMD & Intel Installer - System Uninstallation Script
# ==============================================================================
set -e

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

echo -e "${CYAN}${BOLD}=== ParsLinux AMD & Intel Installer — Uninstaller ===${NC}"

echo -e "${YELLOW}Stopping any running processes...${NC}"
./stop.sh 2>/dev/null || true

echo -e "${BLUE}▶ Removing installed files...${NC}"

sudo rm -f /usr/bin/parslinux-amd-intel-installer
sudo rm -rf /usr/share/parslinux/parslinux-amd-intel-installer
sudo rm -f /usr/share/applications/org.parslinux.amd-intel-installer.desktop
sudo rm -f /usr/share/metainfo/org.parslinux.amd-intel-installer.metainfo.xml
sudo rm -f /usr/share/polkit-1/actions/org.parslinux.pkexec.parslinux-amd-intel-installer.policy
sudo rm -f /usr/share/icons/hicolor/scalable/apps/parslinux-amd-intel-installer.svg
sudo rm -f /usr/share/locale/*/LC_MESSAGES/parslinux-amd-intel-installer.mo

# Clean python-egg-info
sudo rm -rf /usr/lib/python*/dist-packages/parslinux_amd_intel_installer* 2>/dev/null || true
sudo rm -rf /usr/lib/python*/site-packages/parslinux_amd_intel_installer* 2>/dev/null || true

echo -e "${BLUE}▶ Updating caches...${NC}"
sudo update-desktop-database -q /usr/share/applications 2>/dev/null || true

echo -e "${GREEN}${BOLD}✓ ParsLinux AMD & Intel Installer has been cleanly uninstalled from your system.${NC}"
