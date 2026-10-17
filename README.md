# 🎮 ParsLinux Nvidia Installer

[![License: GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)](LICENSE)
[![ParsLinux](https://img.shields.io/badge/ParsLinux-Ecosystem-orange.svg)](https://parslinux.org)
[![Python 3](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![GTK 3](https://img.shields.io/badge/GUI-GTK%203-blue.svg)](https://www.gtk.org/)

**ParsLinux Nvidia Installer**, ParsLinux işletim sisteminde resmi NVIDIA grafik sürücülerini tek tıkla kurmayı, güncellemeyi, kaldırmayı ve dizüstü bilgisayarlardaki melez (Optimus/hybrid) GPU'ları yönetmeyi sağlayan modern grafiksel sistem aracıdır.

Pardus projesinin `pardus-nvidia-installer` aracından forklanarak ParsLinux mimarisine, çoklu dağıtım paketleme sistemine ve ParsLinux görsel kimliğine uyarlanmıştır.

---

## 🚀 Temel Özellikler

- 🔍 **Akıllı Donanım Tespiti:** Sistemdeki PCI veriyolunu tarayarak NVIDIA kartlarını otomatik algılar.
- 🎯 **Donanıma Özel Sürücü Önerisi:** Kartınızın mimarisine (`RTX`, `GTX`, `Tesla 470`, `Nouveau`) en uygun sürücüyü filtreleyerek sunar.
- 🌐 **Resmi NVIDIA CUDA Depo Entegrasyonu:** Tek tıkla resmi NVIDIA CUDA / sürücü deposunu ekleyip güncel kararlı sürücülere erişim sağlar.
- ⚡ **Melez GPU Güç Tasarrufu (Hybrid/Optimus):** Dizüstü bilgisayarlarda harici NVIDIA kartını açılışta güvenle devre dışı bırakıp batarya ömrünü uzatma olanağı.
- 🛡️ **Güvenli Çekirdek Filtresi:** Birincil ekran bağdaştırıcısını (`boot_vga=1`) asla kaldırmaz; siyah ekran riskini önler.
- 🖥️ **Entegre VTE Terminali:** Kurulum ve kaldırma adımlarını gerçek zamanlı terminal günlüğüyle takip etme imkanı.
- 🧪 **Geliştirici & Sanal Makine Simülasyonu:** NVIDIA kartı bulunmayan cihazlarda dahi `--debug` moduyla tam arayüz testi.
- 📦 **Çift Paketleme Desteği:** Hem Debian tabanlı sistemler için `.deb` hem de Arch Linux / CachyOS için `.pkg.tar.zst` paketleme.

---

## 🛠️ Sistem Gereksinimleri

| Bileşen | Paket Adı (Debian / ParsLinux) | Paket Adı (Arch Linux / CachyOS) |
|---|---|---|
| **Python** | `python3` (3.8+) | `python` |
| **GObject Introspection** | `python3-gi`, `gir1.2-gtk-3.0` | `python-gobject`, `gtk3` |
| **Terminal Bileşeni** | `gir1.2-vte-2.91` | `vte3` |
| **Yetkilendirme (Polkit)** | `gir1.2-polkit-1.0`, `policykit-1` | `polkit` |
| **Donanım Tanıma** | `pciutils` | `hwdata` |
| **GPG Doğrulama** | `gnupg` | `gnupg` |

---

## 💻 Kullanım ve Hızlı Başlangıç

### Geliştirici / Yerel Çalıştırma
```bash
# Donanım tespiti yaparak başlatma (kart yoksa otomatik simülasyon)
./run.sh

# Simüle edilmiş RTX 3060 kartı ile demo modu
./run.sh --debug

# Master kontrol paneli
./manage.sh
```

### Sistem Kurulumu
```bash
# Otomatik bağımlılık kontrolü ve sisteme kurulum
./install.sh

# Sistemden temiz kaldırma
./uninstall.sh
```

### Paket Derleme (.deb ve .pkg.tar.zst)
```bash
# Otomatik tespit ve derleme
./package.sh

# Sadece Debian paketi (.deb) derleme
./package.sh --deb

# Sadece Arch paketi (.pkg.tar.zst) derleme
./package.sh --arch
```

### Testleri Çalıştırma
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
# veya
./manage.sh test
```

---

## 📁 Proje Dizin Yapısı

```
parslinux-nvidia-installer/
├── parslinux-nvidia-installer      # Ana ikili başlatıcı (CLI / GUI)
├── pardus-nvidia-installer         # Geriye dönük uyumluluk sembolik bağı
├── org.parslinux.nvidia-installer.desktop # XDG masaüstü kısayolu
├── org.parslinux.pkexec.parslinux-nvidia-installer.policy # Polkit güvenlik politikası
├── pni-disable-gpu.service         # Melez kart açılış systemd servisi
├── pni-disable-gpu.sh              # Melez kart PCI yönetim betiği
├── nvidia.pub                      # Resmi NVIDIA GPG imza anahtarları
├── setup.py                        # Python kurulum betiği
├── meson.build                     # Meson derleme tanımı
├── PKGBUILD / .SRCINFO             # Arch Linux / CachyOS paket tanımları
├── debian/                         # Debian paketleme ve betikleri
│   ├── control, changelog, rules, postinst, postrm, copyright
├── src/
│   ├── Main.py                     # Gtk.Application giriş noktası ve CLI argümanları
│   ├── MainWindow.py               # Pencere yönetimi, VTE terminali ve etkileşim
│   ├── nvidia.py                   # PCI tarayıcısı, pci.ids ayrıştırıcı ve sürücü modeli
│   └── package.py                  # Pkexec altında çalışan ayrıcalıklı kurulum motoru
├── ui/
│   ├── ui.glade                    # Glade ana arayüz tasarımı
│   └── driver_toggle.glade         # Sürücü seçim kartı bileşeni
├── data/
│   ├── nvidia-pci.json             # PCI aygıt kimlikleri ve sürücü eşleme tablosu
│   ├── org.parslinux.nvidia-installer.metainfo.xml # AppStream metaverisi
│   ├── assets/                     # ParsLinux logosu ve kart ikonları
│   └── po/                         # Yerelleştirme dosyaları (Türkçe, Portekizce vb.)
├── docs/                           # Detaylı teknik belgeler
├── tests/                          # Kapsamlı birim ve entegrasyon testleri
├── run.sh                          # Geliştirme başlatma betiği
├── stop.sh                         # Süreç durdurma betiği
├── install.sh                      # Kurulum betiği
├── uninstall.sh                    # Kaldırma betiği
├── package.sh                      # Paketleyici
└── manage.sh                       # Terminal kontrol paneli
```

---

## ⚖️ Lisans

Bu proje **GNU Genel Kamu Lisansı Sürüm 3 (GPL-3.0-or-later)** ile lisanslanmıştır.  
Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
