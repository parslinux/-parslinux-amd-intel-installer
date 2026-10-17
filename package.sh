#!/usr/bin/env bash
# ==============================================================================
# ParsLinux Nvidia Installer - Packaging Script (.deb & .pkg.tar.zst)
# ==============================================================================
set -e

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

DIST_DIR="$PROJECT_DIR/dist"
mkdir -p "$DIST_DIR"

echo -e "${CYAN}${BOLD}=== ParsLinux Nvidia Installer — Package Builder ===${NC}"

show_help() {
    echo -e "Usage: ${BOLD}./package.sh [OPTIONS]${NC}"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help manual"
    echo "  --deb         Build only Debian / ParsLinux (.deb) package"
    echo "  --arch        Build only Arch Linux (.pkg.tar.zst) package"
    echo "  --clean       Clean previous build artifacts"
    echo "  --all         Try to build both formats if tools are installed"
    echo ""
    echo "Examples:"
    echo "  ./package.sh          # Auto-detects OS and builds appropriate package"
    echo "  ./package.sh --arch   # Build Arch Linux package"
    echo "  ./package.sh --deb    # Build Debian package"
    echo "  ./package.sh --clean  # Remove build artifacts"
}

CLEAN_FIRST=false
TARGET_FORMAT="auto"

for arg in "$@"; do
    case "$arg" in
        -h|--help)
            show_help
            exit 0
            ;;
        --clean)
            CLEAN_FIRST=true
            ;;
        --deb)
            TARGET_FORMAT="deb"
            ;;
        --arch)
            TARGET_FORMAT="arch"
            ;;
        --all)
            TARGET_FORMAT="all"
            ;;
    esac
done

if [ "$CLEAN_FIRST" = true ]; then
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    rm -rf build dist debian/.debhelper debian/parslinux-nvidia-installer debian/files *.deb *.tar.gz *.tar.xz *.pkg.tar.zst pkg src/__pycache__ tests/__pycache__ mo
    echo -e "${GREEN}✓ Cleaned successfully.${NC}"
    exit 0
fi

./update_translations.sh 2>/dev/null || true

build_deb() {
    echo -e "${BLUE}▶ Building Debian (.deb) package...${NC}"
    if ! command -v dpkg-buildpackage &>/dev/null; then
        echo -e "${YELLOW}dpkg-buildpackage not found. Using direct archive packager...${NC}"
        BUILDROOT="/tmp/parslinux-nvidia-installer-deb-root"
        DEB_TMP="/tmp/parslinux-nvidia-deb-build"
        rm -rf "$BUILDROOT" "$DEB_TMP"
        mkdir -p "$BUILDROOT" "$DEB_TMP"

        python3 setup.py install --root="$BUILDROOT" --prefix=/usr --optimize=1 >/dev/null
        mkdir -p "$BUILDROOT/DEBIAN"
        cat debian/control | grep -v "^Source:" | grep -v "^Rules-Requires-Root:" | grep -v "^Build-Depends:" | grep -v "^Standards-Version:" | grep -v "^Homepage:" | grep -v "^Vcs-" > "$BUILDROOT/DEBIAN/control"
        echo "Version: 1.0.0-1" >> "$BUILDROOT/DEBIAN/control"
        echo "Architecture: all" >> "$BUILDROOT/DEBIAN/control"

        cp debian/postinst "$BUILDROOT/DEBIAN/postinst" 2>/dev/null || true
        chmod 755 "$BUILDROOT/DEBIAN/postinst" 2>/dev/null || true
        cp debian/postrm "$BUILDROOT/DEBIAN/postrm" 2>/dev/null || true
        chmod 755 "$BUILDROOT/DEBIAN/postrm" 2>/dev/null || true

        if command -v dpkg-deb &>/dev/null; then
            dpkg-deb --build --root-owner-group "$BUILDROOT" "$DIST_DIR/parslinux-nvidia-installer_1.0.0-1_all.deb"
        elif command -v ar &>/dev/null; then
            echo "2.0" > "$DEB_TMP/debian-binary"
            (cd "$BUILDROOT/DEBIAN" && tar -czf "$DEB_TMP/control.tar.gz" *)
            (cd "$BUILDROOT" && tar --exclude="./DEBIAN" -czf "$DEB_TMP/data.tar.gz" ./*)
            (cd "$DEB_TMP" && ar -rc "$DIST_DIR/parslinux-nvidia-installer_1.0.0-1_all.deb" debian-binary control.tar.gz data.tar.gz)
        else
            echo -e "${RED}✗ Error: Neither dpkg-deb nor ar available.${NC}"
            rm -rf "$BUILDROOT" "$DEB_TMP"
            return 1
        fi

        rm -rf "$BUILDROOT" "$DEB_TMP"
        echo -e "${GREEN}✓ Successfully built: $DIST_DIR/parslinux-nvidia-installer_1.0.0-1_all.deb${NC}"
        return 0
    fi

    dpkg-buildpackage -us -uc -b
    mv ../parslinux-nvidia-installer_*.deb "$DIST_DIR/" 2>/dev/null || true
    echo -e "${GREEN}✓ Debian package built in $DIST_DIR/${NC}"
}

build_arch() {
    echo -e "${BLUE}▶ Building Arch Linux (.pkg.tar.zst) package...${NC}"
    if ! command -v makepkg &>/dev/null; then
        echo -e "${RED}✗ Error: makepkg not available on this system!${NC}"
        return 1
    fi
    makepkg -f --nodeps
    mv *.pkg.tar.zst "$DIST_DIR/" 2>/dev/null || true
    echo -e "${GREEN}✓ Arch Linux package built in $DIST_DIR/${NC}"
}

if [ "$TARGET_FORMAT" = "deb" ]; then
    build_deb
elif [ "$TARGET_FORMAT" = "arch" ]; then
    build_arch
elif [ "$TARGET_FORMAT" = "all" ]; then
    build_deb || true
    build_arch || true
else
    # Auto-detection
    if command -v pacman &>/dev/null && command -v makepkg &>/dev/null; then
        build_arch
        # Also try deb building if dpkg-deb is present
        if command -v dpkg-deb &>/dev/null; then
            build_deb || true
        fi
    elif command -v dpkg-buildpackage &>/dev/null || command -v dpkg-deb &>/dev/null; then
        build_deb
    else
        echo -e "${RED}Could not auto-determine packager. Use --deb or --arch.${NC}"
        exit 1
    fi
fi

echo -e "\n${GREEN}${BOLD}✓ Packaging process completed. Artifacts in dist/:${NC}"
ls -lh "$DIST_DIR"
