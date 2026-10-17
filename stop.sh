#!/usr/bin/env bash
# ==============================================================================
# ParsLinux Nvidia Installer - Process Termination Script
# ==============================================================================
set -e

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

echo -e "${CYAN}${BOLD}=== ParsLinux Nvidia Installer — Process Stopper ===${NC}"

PIDS=$(pgrep -f "parslinux-nvidia-installer|pardus-nvidia-installer" || true)

if [ -z "$PIDS" ]; then
    echo -e "${GREEN}✓ No running ParsLinux Nvidia Installer processes found.${NC}"
    exit 0
fi

echo -e "${YELLOW}Found running processes with PIDs: $PIDS${NC}"
for pid in $PIDS; do
    echo -e "Stopping PID: $pid..."
    kill "$pid" 2>/dev/null || true
done

sleep 1

# Force kill any stuck processes
REMAINING=$(pgrep -f "parslinux-nvidia-installer|pardus-nvidia-installer" || true)
if [ -n "$REMAINING" ]; then
    echo -e "${RED}Force killing remaining PIDs: $REMAINING${NC}"
    for pid in $REMAINING; do
        kill -9 "$pid" 2>/dev/null || true
    done
fi

echo -e "${GREEN}✓ All ParsLinux Nvidia Installer processes terminated.${NC}"
