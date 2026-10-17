# 🏛️ ParsLinux Nvidia Installer Mimari Belgesi (`ARCHITECTURE.md`)

Bu belge, **ParsLinux Nvidia Installer** (`parslinux-nvidia-installer`) aracının teknik mimarisini, bileşenler arası veri akışını, güvenlik modelini ve sistem entegrasyonunu açıklamaktadır.

---

## 1. Sistem Genel Bakışı

ParsLinux Nvidia Installer, ParsLinux işletim sisteminde NVIDIA grafik kartı bulunan sistemler için uygun resmi kapalı kaynaklı sürücüleri veya açık kaynaklı `nouveau` sürücülerini tespit eden, kullanıcıya görsel arayüz sunan ve kurulum işlemlerini güvenli bir şekilde gerçekleştiren bir sistem yönetim aracıdır.

```
+--------------------------------------------------------------------+
|                         Kullanıcı Katmanı                          |
|             (parslinux-nvidia-installer / run.sh)                  |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                         Grafiksel Arayüz                           |
|       src/Main.py  <--->  src/MainWindow.py  <--->  ui/ui.glade    |
|                      (Gtk 3, GtkApplication)                       |
+--------------------------------------------------------------------+
        |                                            |
        v                                            v
+-----------------------+                +-----------------------+
|  Donanım Tespiti      |                |  VTE Terminal         |
|  (src/nvidia.py)      |                |  (Canlı Çıktı Ekranı) |
|  - lspci & PCI IDs    |                +-----------------------+
|  - python3-apt / Mock |                            |
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
|  - apt-get install / purge                                         |
|  - DKMS çekirdek modülü derleme                                    |
|  - GPU devre dışı bırakma / açma                                   |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                     Donanım & Çekirdek Seviyesi                    |
|  - Linux Kernel / DKMS (nvidia.ko)                                 |
|  - /sys/bus/pci donanım denetimi                                  |
|  - pni-disable-gpu.service (Systemd servisi)                       |
+--------------------------------------------------------------------+
```

---

## 2. Dizin ve Dosya Yapısı

```
parslinux-nvidia-installer/
├── .claudeignore                      # LLM bağlam dışlama kuralları
├── data/
│   ├── assets/                        # Vektörel grafik varlıkları
│   │   ├── parslinux-logo.svg         # ParsLinux resmi logosu
│   │   ├── video_card.svg             # Aktif GPU vektör ikonu
│   │   └── video_card_disabled.svg    # Pasif GPU vektör ikonu
│   ├── org.parslinux.nvidia-installer.metainfo.xml # AppStream meta verisi
│   └── style.css                      # Modern koyu tema CSS stilleri
├── debian/                            # Debian paketleme tanımları
├── dist/                              # Üretilen binary paketler (.deb, .pkg.tar.zst)
├── docs/                              # Proje dokümantasyon seti
├── images/                            # Masaüstü uygulama ikonu
├── po/                                # Çoklu dil çeviri kaynakları (.po)
├── src/
│   ├── Main.py                        # Gtk.Application giriş noktası ve CLI ayrıştırıcı
│   ├── MainWindow.py                  # 4 sekmeli ana pencere denetleyicisi ve sinyaller
│   ├── monitor.py                     # Canlı sensör telemetrisi, PRIME ve oyun tespiti
│   ├── nvidia.py                      # PCI donanım tespiti ve sürücü eşleme motoru
│   ├── package.py                     # Root yetkisiyle çalışan paket yönetim arka ucu
│   └── tray.py                        # Sistem tepsisi (AppIndicator / Tray) göstergesi
├── tests/                             # Birim testleri (20 test)
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
- `Gtk.Application` sınıfından türetilmiştir (`id: org.parslinux.nvidia-installer`).
- CLI argümanlarını (`--debug`, `--details`, `--remove`, `--tray`, `--version`) işler.
- `Gio.ApplicationFlags.NON_UNIQUE` bayrağı sayesinde geliştirme sırasında yerel testlerin engelsiz çalışmasını sağlar.
- `--tray` seçeneğiyle doğrudan sistem tepsisi arka plan sürecini (`NvidiaTrayApp`) ayağa kaldırır.

### 3.2. `src/MainWindow.py`
- 4 sekmeli `Gtk.StackSwitcher` arayüzünü (Sürücüler, Donanım & Güç, Oyun, Yapay Zeka) kontrol eder.
- Canlı telemetri zamanlayıcısını (3 saniyelik periyot) yönetir ve sensör barlarını günceller.
- Kullanıcı etkileşimli fan hızı (%20-%100) ve güç tüketim sınırı (TDP) kaydırıcılarını dinler.
- PRIME güç profili butonlarını (Tasarruf, Hibrit, Performans) yönetir.
- Canlı terminal çıktısı için `Vte.Terminal` bileşenini barındırır.

### 3.3. `src/monitor.py`
- `nvidia-smi` üzerinden donanım telemetrisini (çekirdek sıcaklığı, fan hızı %, VRAM kullanımı, güç çekimi) okur.
- Fiziksel kart olmayan ortamlarda dinamik dalgalanan simüle telemetri verisi üretir.
- PRIME profil durumunu ve melez grafik varlığını (`glxinfo`, `lspci`, `xrandr`) kontrol eder.
- Sistemde yüklü oyun platformlarını (Steam, Lutris, Heroic, Bottles) ve AI geliştirici araçlarını (CUDA, cuDNN, TensorRT) tespit eder.
- Global NVIDIA PRIME offload durumunu (`/etc/environment.d/10-nvidia-gaming.conf`) denetler.

### 3.4. `src/tray.py`
- `AppIndicator3`, `AyatanaAppIndicator3` ve `Gtk.StatusIcon` fallback katmanlarını destekler.
- Panelde GPU sıcaklığını ve aktif güç profilini canlı gösterir (`45°C • Hibrit`).
- Kullanıcının sağ tık menüsünden tek tıkla Tasarruf/Hibrit/Performans profili seçmesine imkan tanır.
- Ana kontrol panelini (`parslinux-nvidia-installer`) hızlıca başlatır.

### 3.5. `src/nvidia.py`
- `/usr/share/hwdata/pci.ids` veya `/usr/share/misc/pci.ids` veritabanını tarayarak PCI donanım kimliklerini ayrıştırır.
- Sistemdeki VGA ve 3D denetleyici aygıtları arasında `10de` (NVIDIA) kodunu arar.
- Debian/ParsLinux APT önbelleğini denetleyerek mevcut çekirdek başlıkları (`linux-headers`) ve uyumlu sürücü paketlerini listeler.
- Geliştirme ortamında veya Debian harici sistemlerde güvenli `MockAptCache` katmanına düşer.

### 3.6. `src/package.py`
- Yalnızca `root` yetkisiyle çalıştırılır (`pkexec` koruması altında).
- Desteklenen komutlar:
  - `install-nvidia`, `install-nouveau`, `update`: Sürücü yükleme/kaldırma ve depo güncelleme.
  - `disable-sec-gpu`, `enable-sec-gpu`: İkincil GPU'yu PCI veriyolundan çıkarma/ekleme.
  - `prime-mode <intel|on-demand|nvidia>`: Güç profili yapılandırması.
  - `set-fan-speed <hız>`: Manuel fan hızı ayarı.
  - `set-power-limit <watt>`: GPU maksimum güç tüketim limiti (TDP).
  - `set-game-offload <1|0>`: Global PRIME Offload ortam değişkenleri yapılandırması.
  - `install-ai-tools`: CUDA Toolkit, cuDNN ve TensorRT kurulumu.
- Katı regex doğrulaması ile komut enjeksiyonunu engeller.

---

## 4. Güvenlik Modeli

1. **En Az Yetki İlkesi (Least Privilege)**: Grafiksel arayüz (`MainWindow.py`) ve sistem tepsisi (`tray.py`) standart kullanıcı haklarıyla çalışır.
2. **PolicyKit Doğrulaması**: Sadece paket kurma, donanım fan/güç limiti değiştirme veya güç profili atama gibi kritik adımlarda `pkexec` üzerinden `org.parslinux.pkexec.parslinux-nvidia-installer.policy` kuralı tetiklenir.
3. **Komut Enjeksiyonu Koruması**: `package.py` parametreleri doğrudan kabuğa gönderilmez; katı argüman kontrolleri ve regex filtrelerinden geçirilir.
