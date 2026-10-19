# Maintainer: ParsLinux Developers <dev@parslinux.org>
pkgname=parslinux-amd-intel-installer
pkgver=1.0.0
pkgrel=1
pkgdesc="ParsLinux AMD Radeon & Intel Graphics Driver Installer and Hybrid GPU Manager"
arch=('any')
url="https://parslinux.org"
license=('GPL-3.0-or-later')
depends=(
    'python'
    'python-gobject'
    'gtk4'
    'vte4'
    'polkit'
    'hwdata'
    'pciutils'
)
optdepends=(
    'vulkan-radeon: AMD Vulkan driver (RADV)'
    'vulkan-intel: Intel Vulkan driver (ANV)'
    'mesa-va-drivers: AMD VA-API hardware video acceleration'
    'intel-media-driver: Intel modern VA-API hardware video acceleration'
    'rocm-opencl-runtime: AMD OpenCL and ROCm runtime'
    'intel-compute-runtime: Intel OpenCL NEO and Level Zero runtime'
)
makedepends=(
    'python-setuptools'
    'gettext'
)

build() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    python3 setup.py build
}

package() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    python3 setup.py install --root="$pkgdir" --prefix=/usr --optimize=1
}
