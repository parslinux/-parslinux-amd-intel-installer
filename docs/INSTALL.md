# 🚀 Kurulum ve Yapılandırma Kılavuzu (`INSTALL.md`)

Bu belge, **ParsLinux Nvidia Installer** (`parslinux-nvidia-installer`) aracının ParsLinux ve diğer Linux dağıtımlarına kurulumu, yapılandırılması ve kaldırılması adımlarını içerir.

---

## 1. Otomatik Kurulum (Tavsiye Edilen)

Depoyu yerel bilgisayarınıza indirin ve kurulum betiğini root yetkileriyle çalıştırın:

```bash
git clone https://github.com/parslinux/parslinux-nvidia-installer.git
cd parslinux-nvidia-installer
sudo ./install.sh
```

Betiğin gerçekleştirdiği adımlar:
1. Gerekli bağımlılıkları (`python3`, `python3-gi`, `gir1.2-gtk-3.0`, `gir1.2-vte-2.91`, `polkit`, `pciutils`) denetler ve kurar.
2. Kaynak kodları `/usr/share/parslinux/parslinux-nvidia-installer/` dizinine yerleştirir.
3. Çalıştırılabilir ikili dosyayı `/usr/bin/parslinux-nvidia-installer` altına sembolik bağlar.
4. Masaüstü kısayolunu (`org.parslinux.nvidia-installer.desktop`) ve AppStream meta verilerini kopyalar.
5. PolicyKit kuralını (`org.parslinux.pkexec.parslinux-nvidia-installer.policy`) yetkilendirme dizinine kurar.
6. Systemd GPU güç tasarruf servisini (`pni-disable-gpu.service`) kaydeder.
7. İkon ve masaüstü önbelleklerini yeniler.

---

## 2. Paket Yöneticisi ile Kurulum

### Debian / ParsLinux (.deb)
```bash
# Önceden derlenmiş paketi kurun:
sudo dpkg -i dist/parslinux-nvidia-installer_1.0.0-1_all.deb
sudo apt install -f
```

### Arch Linux / CachyOS (.pkg.tar.zst)
```bash
# PKGBUILD üzerinden derleyip kurun:
makepkg -si
```

---

## 3. Sistemden Kaldırma

Uygulamayı ve tüm sistem bileşenlerini temiz bir şekilde kaldırmak için:

```bash
sudo ./uninstall.sh
```

Veya Debian paket yöneticisi ile:
```bash
sudo apt purge parslinux-nvidia-installer
```
