#!/bin/bash
# ==============================================================================
# ParsLinux Nvidia Installer - Secondary GPU Boot Disabler
# Safely powers down / detaches secondary discrete NVIDIA GPU on hybrid laptops
# ==============================================================================
set -e

# Support both ParsLinux and legacy marker paths
if [[ ! -f /var/cache/parslinux-nvi-disable-gpu && ! -f /var/cache/pni-disable-gpu ]]; then
    exit 0
fi

if grep -q "nomodeset" /proc/cmdline ; then
    echo "nomodeset detected in cmdline; skipping secondary GPU disabling."
    exit 0
fi

remove_pci(){
    local dev="$1"
    if [[ -d "/sys/bus/pci/devices/$dev/driver" ]] ; then
        local module
        module=$(basename "$(readlink -f "/sys/bus/pci/devices/$dev/driver/module" 2>/dev/null)" 2>/dev/null || true)
        if [[ -n "$module" ]]; then
            echo "Unloading driver: $module for device ($dev)"
            rmmod -f "$module" 2>/dev/null || true
        fi
    fi
    if [[ -w "/sys/bus/pci/devices/$dev/remove" ]]; then
        echo "Removing PCI device: $dev"
        echo 1 > "/sys/bus/pci/devices/$dev/remove" || true
    fi
}

has_primary=0
for d in /sys/bus/pci/devices/*/boot_vga; do
    if [ -r "$d" ] && [ "$(cat "$d" 2>/dev/null)" = "1" ]; then
        has_primary=1
        break
    fi
done

if [ "$has_primary" != "1" ]; then
    echo "No boot_vga=1 primary identified; refusing to remove GPUs for safety."
    exit 0
fi

for dir in /sys/bus/pci/devices/*; do
    [ -d "$dir" ] || continue
    dev_name=$(basename "$dir")
    
    # Check for Nvidia vendor ID (0x10de)
    vendor=$(cat "$dir/vendor" 2>/dev/null || true)
    [ "$vendor" = "0x10de" ] || continue

    # Check for display controller classes (0x03xxxx)
    class=$(cat "$dir/class" 2>/dev/null || true)
    case "$class" in
        0x03*) ;;
        *) continue ;;
    esac

    # Never touch the primary display device
    boot_vga=$(cat "$dir/boot_vga" 2>/dev/null || true)
    if [ "$boot_vga" = "1" ]; then
        echo "Preserving boot display device: $dev_name"
        continue
    fi

    echo "Found secondary NVIDIA GPU: $dev_name"
    remove_pci "$dev_name"
done

udevadm settle --timeout=30 2>/dev/null || true
exit 0
