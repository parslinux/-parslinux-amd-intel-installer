# 📦 Flatpak ve Grafik Entegrasyonu (`FLATPAK_PACKAGING.md`)

Bu belge, **ParsLinux AMD & Intel Installer** aracının sistem grafik katmanları ve Flatpak oyun/grafik ekosistemiyle nasıl entegre çalıştığını açıklar.

---

## 1. Neden Sistem Düzeyinde Paketleme?

- **Mesa ve Çekirdek Entegrasyonu**: Vulkan (`vulkan-radeon`, `vulkan-intel`) ve VA-API (`mesa-va-drivers`, `intel-media-driver`) sürücüleri sistem geneli grafik alt yapısını ve donanım video hızlandırmasını yapılandırır.
- **Root Yetkileri**: Paket kurulumu ve sistem geneli ortam değişkenleri PolicyKit doğrulaması gerektirir.

Bu nedenlerle `parslinux-amd-intel-installer` ana sistem paketi (`.deb` / Arch PKGBUILD) olarak çalışır.

---

## 2. Flatpak Uygulamalarıyla Uyumluluk

ParsLinux üzerinde Flatpak ile çalışan oyunlar (Steam, Heroic vb.) ve medya oynatıcılar, ana sistemdeki Mesa sürücülerini otomatik olarak tanır:
- Flatpak Mesa GL/Vulkan çalışma zamanı (`org.freedesktop.Platform.GL.default`) sistemdeki GPU ile kusursuz uyum sağlar.
- `DRI_PRIME=1` komutu Flatpak oyunlarında doğrudan harici GPU'yu devreye sokar.
