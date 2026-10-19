#!/usr/bin/env bash
# ==============================================================================
# ParsLinux AMD & Intel Installer - Process Termination Script
# ==============================================================================
set -e

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

echo -e "${CYAN}${BOLD}=== ParsLinux AMD & Intel Installer — Process Stopper ===${NC}"

PIDS=$(pgrep -f "parslinux-amd-intel-installer" || true)

if [ -z "$PIDS" ]; then
    echo -e "${GREEN}✓ No running ParsLinux AMD & Intel Installer processes found.${NC}"
    exit 0
fi

echo -e "${YELLOW}Found running processes with PIDs: $PIDS${NC}"
for pid in $PIDS; do
    echo -e "Stopping PID: $pid..."
    kill "$pid" 2>/dev/null || true
done

sleep 1

# Force kill any stuck processes
REMAINING=$(pgrep -f "parslinux-amd-intel-installer" || true)
if [ -n "$REMAINING" ]; then
    echo -e "${RED}Force killing remaining PIDs: $REMAINING${NC}"
    for pid in $REMAINING; do
        kill -9 "$pid" 2>/dev/null || true
    done
fi

echo -e "${GREEN}✓ All ParsLinux AMD & Intel Installer processes terminated.${NC}"
