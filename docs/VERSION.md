# 🔖 Sürüm Politikası (`VERSION.md`)

`parslinux-amd-intel-installer` projesi, [Semantic Versioning 2.0.0](https://semver.org/) (SemVer) standardını benimser.

---

## 1. Sürüm Numaralandırma Yapısı

`MAJOR.MINOR.PATCH` formatında:
- **MAJOR (1.x.x)**: Temel mimaride köklü değişiklikler (örneğin GTK4 / Libadwaita geçişi, Wayland native PRIME protokolü dönüşümü).
- **MINOR (x.1.x)**: Yeni donanım filtreleri, yeni GPU aileleri desteği (RDNA 4, Intel Battlemage), yeni CLI bayrakları.
- **PATCH (x.x.1)**: Hata düzeltmeleri, çeviri iyileştirmeleri, paketleme ve dokümantasyon güncellemeleri.

---

## 2. Mevcut Sürüm
- **Versiyon:** `1.0.0`
- **Çıkış Tarihi:** 19 Ekim 2026
- **Durum:** İlk Kararlı Sürüm (AMD & Intel Donanım Algılama, Vulkan/VA-API Yapılandırma, PRIME Melez Yönetimi)
- **Hedef Taban:** ParsLinux 1.0 (Debian Bookworm/Trixie tabanlı) & Arch Linux
