# 📝 Değişiklik Günlüğü (`CHANGELOG.md`)

Tüm önemli değişiklikler bu dosyada belgelenecektir. Format [Keep a Changelog](https://keepachangelog.com/) standardına uygundur.

---

## [1.0.0] - 2026-10-19

### 🎉 İlk Kararlı Sürüm (AMD & Intel Mimarisi)
- **AMD & Intel Birleşik Grafik Yöneticisi**:
  - AMD Radeon (RDNA 1/2/3/3.5, Polaris, Vega) ve Intel (Arc Battlemage/Alchemist, Iris Xe, UHD) donanımlarını tek panelde birleştiren sistem.
- **Akıllı Donanım Tespiti (`src/detector.py`)**:
  - `lspci`, `sysfs`, `hwdata` ve DRM yollarını tarayarak birincil/ikincil GPU rollerini ve mimariyi tespit eder.
- **Vulkan & Grafik Katmanları**:
  - AMD için RADV (`vulkan-radeon`) ve AMDVLK, Intel için ANV (`vulkan-intel`) tek tıkla kurulum ve yönetimi.
  - 32-bit oyun uyumluluk katmanları (`lib32` / `i386`).
- **Donanım Video Hızlandırma (VA-API / QuickSync)**:
  - Tarayıcılarda ve video oynatıcılarda sıfır CPU kullanımı için `mesa-va-drivers` ve `intel-media-driver` entegrasyonu.
- **Melez Grafik & PRIME Yönetimi**:
  - Dizüstü bilgisayarlarda pil tasarrufu (iGPU) veya harici GPU ile oyun (`DRI_PRIME=1`) geçişi.
- **Hesaplama ve AI (Compute)**:
  - AMD ROCm / OpenCL ve Intel oneAPI / Compute Runtime desteği.
- **Çift Dağıtım Paketleme**:
  - Debian tabanlı (.deb) ve Arch Linux tabanlı (.pkg.tar.zst) paket desteği.
