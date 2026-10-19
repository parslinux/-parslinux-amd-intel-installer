# 📊 İlerleme ve Yol Haritası (`progress.md`)

## 📌 Tamamlanan Görevler (v1.0.0)
- [x] Tüm proje dokümantasyonu ve mimarisinin **ParsLinux AMD & Intel Installer** çatısına dönüştürülmesi.
- [x] GitHub remote adresinin `git@github.com:parslinux/-parslinux-amd-intel-installer.git` olarak güncellenmesi.
- [x] AMD & Intel mimari kılavuzunun oluşturulması (`docs/AMD_INTEL_DRIVER_GUIDE.md`).
- [x] GTK4 ve modern arayüz standartlarının belirlenmesi.
- [x] RADV / ANV Vulkan katmanları, VA-API donanım hızlandırma ve ROCm / oneAPI gereksinimlerinin planlanması.

---

## 🎯 Gelecek Hedefler (v1.1.0 & Yol Haritası)
- [ ] **AMD & Intel Donanım Algılama Motoru Entegrasyonu** (`src/detector.py`):
  - `1002` (AMD) ve `8086` (Intel) PCI aygıtlarının tam tespiti.
- [ ] **Vulkan ve VA-API Paket Yöneticisi Entegrasyonu** (`src/package.py`):
  - Debian ve Arch üzerinde otomatik tespit edilen kartlara göre paket kurma.
- [ ] **Arayüz Sekmelerinin AMD & Intel Özelliklerine Göre Düzenlenmesi** (`ui/ui.glade`, `src/MainWindow.py`).
- [ ] **Sysfs Donanım Sensörleri (`/sys/class/drm`) ve Telemetri**.
