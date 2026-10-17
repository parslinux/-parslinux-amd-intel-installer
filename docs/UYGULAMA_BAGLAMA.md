# 🔗 Sistem ve Dağıtım Entegrasyonu (`UYGULAMA_BAGLAMA.md`)

Bu belge, `parslinux-nvidia-installer` paketinin ParsLinux dağıtım ekosistemine, ISO kalıplarına ve masaüstü ortamlarına nasıl bağlandığını açıklar.

---

## 1. Masaüstü Ortamı (XDG) Entegrasyonu

Uygulamanın GNOME, XFCE ve KDE başlatıcı menülerinde yer alması için:
- **Desktop Girişi:** `/usr/share/applications/org.parslinux.nvidia-installer.desktop`
- **Kategoriler:** `Settings;HardwareSettings;System;`
- **İkon Konumu:** `/usr/share/icons/hicolor/scalable/apps/parslinux-nvidia-installer.svg`
- **AppStream Metainfo:** `/usr/share/metainfo/org.parslinux.nvidia-installer.metainfo.xml`

---

## 2. PolicyKit Yetkilendirme Entegrasyonu

Kullanıcı arayüzünden doğrudan paket kurulumu veya GPU kapatma çağrıldığında:
- `/usr/share/polkit-1/actions/org.parslinux.pkexec.parslinux-nvidia-installer.policy`
- Sistem yöneticisi şifre doğrulama penceresi tetiklenir ve işlem arka planda `root` yetkisiyle güvenle yürütülür.

---

## 3. `live-build` ve Calamares Entegrasyonu

Canlı ParsLinux ISO kalıbı (`ParsLinux-1.0-gnome-amd64.iso`) derlenirken:
1. `config/package-lists/drivers.list.chroot` dosyasına eklenir:
   ```bash
   parslinux-nvidia-installer
   ```
2. Calamares kurulum sihirbazının `packages` veya `post-install` modülünde NVIDIA GPU tespiti yapılarak kullanıcının ilk masaüstü açılışında bu aracı çalıştırması önerilebilir.
