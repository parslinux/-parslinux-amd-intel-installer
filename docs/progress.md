# 📊 İlerleme ve Yol Haritası (`progress.md`)

## 📌 Tamamlanan Görevler (v1.0.0 Sürümü)

### 1. Mimari ve Temel Altyapı
- [x] Tüm proje dokümantasyonu ve mimarisinin **ParsLinux AMD & Intel Installer** çatısına dönüştürülmesi.
- [x] NVIDIA ve Nouveau kalıntılarının kod, varlık, CSS ve yapılandırmalardan tamamen temizlenmesi.
- [x] GitHub remote adresinin `git@github.com:parslinux/-parslinux-amd-intel-installer.git` olarak güncellenmesi.
- [x] Yeni AMD & Intel mimari kılavuzunun oluşturulması (`docs/AMD_INTEL_DRIVER_GUIDE.md`).
- [x] GTK4 ve libadwaita standartlarında modern görsel tasarım ve Pango markup uyumluluğu.

### 2. Donanım Tespiti & Mimari Motoru (`src/detector.py`)
- [x] PCI Vendor ID `0x1002` (AMD) ve `0x8086` (Intel) aygıtlarının çok katmanlı tespiti (`pci.ids`, `lspci`, `sysfs`).
- [x] Harici dGPU ve Dahili iGPU rollerinin otomatik tespiti ve melez (Hybrid) GPU çiftlerinin sınıflandırılması.
- [x] Mimari eşleme motoru:
  - AMD: RDNA 3 / 3.5, RDNA 2, RDNA 1, Vega (GCN 5), Polaris (GCN 4), Eski GCN.
  - Intel: Arc Battlemage (Xe2-HPG), Arc Alchemist (Xe-HPG), Meteor/Lunar Lake (Xe-LPG), Iris Xe, UHD Graphics, Legacy HD Graphics.
- [x] Akıllı sürücü ve Vulkan katmanı öneri sistemi (`vulkan-radeon`, `vulkan-intel`, `mesa-va-drivers`, `intel-media-driver`).

### 3. Paket Yöneticisi & Güvenlik (`src/package.py`)
- [x] Çift dağıtım desteği: Debian / ParsLinux (`apt`) ve Arch Linux / CachyOS (`pacman`).
- [x] Güvenli paket adı doğrulama listesi (Allowlist) ve komut enjeksiyonu koruması.
- [x] 32-bit multilib oyun kütüphaneleri, Vulkan ICD'leri ve donanım video hızlandırma kütüphaneleri otomasyonu.
- [x] Geliştirici & AI kütüphaneleri kurulum betikleri (AMD ROCm / HIP ve Intel oneAPI / Level Zero).

### 4. Arayüz ve Kullanıcı Deneyimi (`src/MainWindow.py` & `ui/ui.glade`)
- [x] 4 ana fonksiyonel sekme:
  - 🎮 **Sürücüler:** Otomatik önerilen Vulkan/VA-API sürücüleri, sürüm bilgileri ve tek tıkla kurulum.
  - 📊 **Donanım & Güç:** Canlı sıcaklık, fan devri, güç tüketimi (Watt) ve özel fan/güç sınırı kaydırıcıları.
  - 🕹️ **Oyun:** Tespit edilen oyun başlatıcıları (Steam, Heroic, Lutris, Bottles), dGPU ile çalıştırma ve MangoHud kontrolü.
  - 🧠 **Yapay Zeka & Compute:** ROCm, oneAPI ve OpenCL kütüphaneleri tek tıkla kurulum paneli.
- [x] Donanım bulunmayan veya sanal makinelerde geliştirici testleri için `--debug` simülasyon modu.
- [x] Gerçek zamanlı VTE terminal günlüğü ve operasyon çıktısı takibi.

### 5. Canlı Telemetri ve Güç Yönetimi (`src/monitor.py` & `src/tray.py`)
- [x] `/sys/class/hwmon` ve `/sys/class/drm` üzerinden gerçek zamanlı sensör okuma.
- [x] AMD & Intel grafik kartları için dinamik güç profilleri ve PRIME render offload (`DRI_PRIME=1`) desteği.
- [x] Masaüstü sistem tepsisi (AppIndicator / Tray) canlı sıcaklık ve GPU durumu göstergesi.

### 6. Test, Paketleme ve CI/CD
- [x] Otomatik birim test takımı (`tests/test_installer.py`) — 16/16 test başarıyla geçiyor.
- [x] Çift paketleme betiği (`./package.sh`): Debian `.deb` ve Arch Linux `.pkg.tar.zst` paket oluşturucu.
- [x] Setuptools bağımsız fallback mekanizması (`setup.py`).
- [x] Yüksek çözünürlüklü otomatik ekran görüntüsü yakalama aracı (`scripts/capture_screenshots.py`).

---

## 🎯 Gelecek Hedefler (v1.1.0 & v1.2.0 Yol Haritası)

### v1.1.0 — Gelişmiş Ayarlar & Çekirdek Yapılandırması
- [x] **Kernel Modül Parametreleri Yöneticisi (`src/kernel_config.py`):**
  - AMD: `/etc/modprobe.d/amdgpu.conf` üzerinden `amdgpu.ppfeaturemask=0xffffffff` overclock kilidi açma.
  - Intel: `/etc/modprobe.d/i915.conf` ve `xe.conf` üzerinden `enable_guc=3` (GuC/HuC donanım hızlandırma) aktivasyonu.
  - Sisteme kaydetme ve otomatik `update-initramfs` / `mkinitcpio` / `dracut` tetikleme altyapısı.
- [x] **MangoHud Önayar Yapılandırıcısı (Presets):**
  - Kompakt FPS Modu, Ayrıntılı Donanım Modu, Yayıncı Modu ve Benchmark Modu hazır profilleri.
  - GTK4 açılır menü (DropDown) ile anlık profil değişimi.
- [x] **GameMode (Feral Interactive) Entegrasyonu:**
  - `gamemoderun` durum tespiti ve tek tıkla sistem paket yöneticisinden kurulum.
- [x] **Sistem Geri Yükleme / Timeshift Entegrasyonu:**
  - Timeshift kontrolü ve sürücü/kütüphane kurulumları öncesi yedek alma yönlendirmesi.

### v1.2.0 — Kapsamlı Benchmark ve Performans Araçları
- [ ] **Dahili Grafik Benchmark Aracı:**
  - `vkmark` ve `glmark2` ile AMD vs Intel karşılaştırmalı performans testi ve FPS raporlaması.
- [ ] **Wayland Masaüstü Uygulama GPU Atayıcısı:**
  - GNOME, KDE Plasma ve Hyprland masaüstlerinde `.desktop` dosyalarına sağ tıkla veya arayüzden varsayılan GPU atama sihirbazı.
- [ ] **Çoklu Dil Çevirileri (i18n):**
  - Almanca (`de`), İspanyolca (`es`), Fransızca (`fr`) ve Rusça (`ru`) dil dosyalarının eklenmesi.
