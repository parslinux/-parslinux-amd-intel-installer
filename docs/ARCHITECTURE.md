# 🏛️ ParsLinux AMD & Intel Installer Mimari Belgesi (`ARCHITECTURE.md`)

Bu belge, **ParsLinux AMD & Intel Installer** (`parslinux-amd-intel-installer`) aracının teknik mimarisini, bileşenler arası veri akışını, güvenlik modelini ve sistem entegrasyonunu açıklamaktadır.

---

## 1. Sistem Genel Bakışı

ParsLinux AMD & Intel Installer, ParsLinux işletim sisteminde AMD Radeon ve Intel (Iris Xe, UHD, Arc) grafik donanımları bulunan sistemler için Vulkan katmanlarını (RADV/ANV), donanım video hızlandırma kütüphanelerini (VA-API/QuickSync), 32-bit oyun paketlerini ve hesaplama/AI araçlarını (ROCm/oneAPI) tespit eden, kullanıcıya görsel arayüz sunan ve yapılandırma işlemlerini güvenli bir şekilde gerçekleştiren bir sistem yönetim aracıdır.

```
+--------------------------------------------------------------------+
|                         Kullanıcı Katmanı                          |
|             (parslinux-amd-intel-installer / run.sh)               |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                         Grafiksel Arayüz                           |
|       src/Main.py  <--->  src/MainWindow.py  <--->  ui/ui.glade    |
|                      (Gtk 4, GtkApplication)                       |
+--------------------------------------------------------------------+
        |                                            |
        v                                            v
+-----------------------+                +-----------------------+
|  Donanım Tespiti      |                |  VTE Terminal         |
|  (src/detector.py)    |                |  (Canlı Çıktı Ekranı) |
|  - lspci & PCI IDs    |                +-----------------------+
|  - sysfs & DRM        |                            |
+-----------------------+                            |
                                                     v
+--------------------------------------------------------------------+
|                     Ayrıcalık Yükseltme Katmanı                    |
|       PolicyKit (pkexec) : org.parslinux.pkexec.policy             |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                     Yetkili Yürütücü Katmanı                       |
|                       src/package.py                               |
|  - apt-get / pacman paket yönetimi                                 |
|  - VA-API & Vulkan yapılandırma                                    |
|  - PRIME & Melez GPU güç yönetimi                                  |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                     Donanım & Çekirdek Seviyesi                    |
|  - Linux Kernel (amdgpu, i915, xe)                                 |
|  - /sys/class/drm ve /sys/bus/pci donanım denetimi                 |
|  - Mesa / Vulkan / VA-API katmanları                               |
+--------------------------------------------------------------------+
```

---

## 2. Dizin ve Dosya Yapısı

```
parslinux-amd-intel-installer/
├── .claudeignore                      # LLM bağlam dışlama kuralları
├── data/
│   ├── assets/                        # Vektörel grafik varlıkları
│   │   ├── parslinux-logo.svg         # ParsLinux resmi logosu
│   │   ├── video_card.svg             # Aktif GPU vektör ikonu
│   │   └── video_card_disabled.svg    # Pasif GPU vektör ikonu
│   ├── org.parslinux.amd-intel-installer.metainfo.xml # AppStream meta verisi
│   └── style.css                      # Modern koyu tema CSS stilleri
├── debian/                            # Debian paketleme tanımları
├── dist/                              # Üretilen binary paketler (.deb, .pkg.tar.zst)
├── docs/                              # Proje dokümantasyon seti
├── images/                            # Masaüstü uygulama ikonu
├── po/                                # Çoklu dil çeviri kaynakları (.po)
├── src/
│   ├── Main.py                        # Gtk.Application giriş noktası ve CLI ayrıştırıcı
│   ├── MainWindow.py                  # Sekmeli ana pencere denetleyicisi ve sinyaller
│   ├── detector.py                    # PCI donanım tespiti ve sürücü/kart eşleme motoru
│   ├── monitor.py                     # Canlı sensör telemetrisi, PRIME ve donanım takibi
│   ├── package.py                     # Root yetkisiyle çalışan paket yönetim arka ucu
│   └── tray.py                        # Sistem tepsisi (AppIndicator / Tray) göstergesi
├── tests/                             # Birim testleri
├── ui/
│   └── ui.glade                       # GtkBuilder arayüz yerleşim dosyası
├── install.sh                         # Sistem geneline kurulum betiği
├── uninstall.sh                       # Sistemden kaldırma betiği
├── package.sh                         # Paket inşa betiği
├── run.sh                             # Geliştirme başlatıcı betiği
└── stop.sh                            # Uygulama sonlandırma betiği
```

---

## 3. Temel Bileşenler ve Görevleri

### 3.1. `src/Main.py`
- `Gtk.Application` sınıfından türetilmiştir (`id: org.parslinux.amd-intel-installer`).
- CLI argümanlarını (`--debug`, `--details`, `--detect`, `--json`, `--tray`, `--version`) işler.
- `Gio.ApplicationFlags.NON_UNIQUE` bayrağı sayesinde geliştirme sırasında yerel testlerin engelsiz çalışmasını sağlar.
- `--tray` seçeneğiyle doğrudan sistem tepsisi arka plan sürecini ayağa kaldırır.

### 3.2. `src/MainWindow.py`
- Sekmeli modern GTK4 arayüzünü (Sürücüler & Katmanlar, Donanım & Sensörler, Oyun & Video, Hesaplama / AI) kontrol eder.
- Canlı telemetri zamanlayıcısını (3 saniyelik periyot) yönetir ve sensör barlarını günceller.
- PRIME güç profili kontrollerini (Entegre Tasarruf / Melez / Harici Performans) yönetir.
- Canlı terminal çıktısı için `Vte.Terminal` bileşenini barındırır.

### 3.3. `src/detector.py`
- `/usr/share/hwdata/pci.ids` veya `/usr/share/misc/pci.ids` veritabanını tarayarak PCI donanım kimliklerini ayrıştırır.
- Sistemdeki VGA ve 3D denetleyici aygıtları arasında `1002` (AMD) ve `8086` (Intel) kodlarını arar.
- Birincil (boot_vga) ve ikincil (Optimus/PRIME) rolleri güvenli bir şekilde ayrıştırır.

### 3.4. `src/monitor.py`
- `sysfs` (`/sys/class/drm/card*/device/hwmon`) ve ilgili araçlar üzerinden donanım telemetrisini (GPU sıcaklığı, fan hızı %, VRAM kullanımı, güç çekimi) okur.
- Fiziksel kart olmayan ortamlarda dinamik dalgalanan simüle telemetri verisi üretir.
- Sistemde yüklü oyun platformlarını (Steam, Lutris, Heroic, Bottles) ve AI araçlarını (ROCm, oneAPI, OpenCL) tespit eder.

### 3.5. `src/tray.py`
- `AppIndicator3` / `AyatanaAppIndicator3` katmanlarını destekler.
- Panelde aktif GPU sıcaklığını ve modunu canlı gösterir.
- Kullanıcının sağ tık menüsünden tek tıkla güç modu veya ana pencereyi açmasına imkan tanır.

### 3.6. `src/package.py`
- Yalnızca `root` yetkisiyle çalıştırılır (`pkexec` koruması altında).
- Desteklenen komutlar:
  - `install-vulkan`, `install-vaapi`, `install-compute`: Vulkan, VA-API ve OpenCL/ROCm paketlerini kurma/güncelleme.
  - `prime-mode <integrated|hybrid|performance>`: Melez grafik güç modu yapılandırması.
  - `set-game-offload <1|0>`: Global `DRI_PRIME` ortam değişkenleri yapılandırması.
- Katı regex ve argüman doğrulaması ile komut enjeksiyonunu engeller.

---

## 4. Güvenlik Modeli

1. **En Az Yetki İlkesi (Least Privilege)**: Grafiksel arayüz (`MainWindow.py`) ve sistem tepsisi (`tray.py`) standart kullanıcı haklarıyla çalışır.
2. **PolicyKit Doğrulaması**: Sadece paket kurma veya sistem genelinde güç profili atama gibi kritik adımlarda `pkexec` üzerinden `org.parslinux.pkexec.parslinux-amd-intel-installer.policy` kuralı tetiklenir.
3. **Komut Enjeksiyonu Koruması**: `package.py` parametreleri doğrudan kabuğa gönderilmez; katı argüman kontrolleri ve filtrelerden geçirilir.
