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
│   ├── MainWindow.py                  # Ana pencere denetleyicisi ve sinyal işleyiciler
│   ├── nvidia.py                      # PCI donanım tespiti ve sürücü eşleme motoru
│   └── package.py                     # Root yetkisiyle çalışan paket yönetim arka ucu
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
- `Gtk.Application` sınıfından türetilmiştir (`id: org.parslinux.nvidia-installer`).
- CLI argümanlarını (`--debug`, `--details`, `--remove`, `--version`) işler.
- `Gio.ApplicationFlags.NON_UNIQUE` bayrağı sayesinde geliştirme sırasında yerel testlerin engelsiz çalışmasını sağlar.

### 3.2. `src/MainWindow.py`
- Glade XML dosyasını yükler ve sinyalleri dinamik olarak bağlar.
- Sistemdeki NVIDIA GPU modelini ekrana yansıtır.
- Yüklü olan sürücü durumunu (NVIDIA kapalı kaynak veya Nouveau açık kaynak) denetler.
- Canlı terminal çıktısı için `Vte.Terminal` bileşenini yönetir.
- Simülasyon modunda donanım olmasa dahi arayüzün tam fonksiyonel test edilmesini sağlar.

### 3.3. `src/nvidia.py`
- `/usr/share/hwdata/pci.ids` veya `/usr/share/misc/pci.ids` veritabanını tarayarak PCI donanım kimliklerini ayrıştırır.
- Sistemdeki VGA ve 3D denetleyici aygıtları arasında `10de` (NVIDIA) kodunu arar.
- Debian/ParsLinux APT önbelleğini denetleyerek mevcut çekirdek başlıkları (`linux-headers`) ve uyumlu sürücü paketlerini listeler.
- Geliştirme ortamında veya Debian harici sistemlerde güvenli `MockAptCache` katmanına düşer.

### 3.4. `src/package.py`
- Yalnızca `root` yetkisiyle çalıştırılır (`pkexec` koruması altında).
- `install-nvidia`, `install-nouveau`, `update`, `disable-sec-gpu` ve `enable-sec-gpu` komutlarını icra eder.
- Yalnızca güvenli paket beyaz listesine (`nvidia-driver`, `nvidia-detect`, `linux-headers-*`, `xserver-xorg-video-nouveau`) izin veren regex doğrulaması içerir.

---

## 4. Güvenlik Modeli

1. **En Az Yetki İlkesi (Least Privilege)**: Grafiksel arayüz (`MainWindow.py`) standart kullanıcı haklarıyla çalışır.
2. **PolicyKit Doğrulaması**: Sadece paket kurma veya donanım devre dışı bırakma gibi kritik adımlarda `pkexec` üzerinden `org.parslinux.pkexec.parslinux-nvidia-installer.policy` kuralı tetiklenir.
3. **Komut Enjeksiyonu Koruması**: `package.py` parametreleri doğrudan kabuğa gönderilmez; katı argüman kontrolleri ve regex filtrelerinden geçirilir.
