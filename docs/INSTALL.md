# 🚀 Kurulum ve Yapılandırma Kılavuzu (`INSTALL.md`)

Bu belge, **ParsLinux AMD & Intel Installer** (`parslinux-amd-intel-installer`) aracının ParsLinux ve diğer Linux dağıtımlarına kurulumu, yapılandırılması ve kaldırılması adımlarını içerir.

---

## 1. Otomatik Kurulum (Tavsiye Edilen)

Depoyu yerel bilgisayarınıza indirin ve kurulum betiğini root yetkileriyle çalıştırın:

```bash
git clone git@github.com:parslinux/-parslinux-amd-intel-installer.git
cd -parslinux-amd-intel-installer
sudo ./install.sh
```

Betiğin gerçekleştirdiği adımlar:
1. Gerekli bağımlılıkları (`python3`, `python3-gi`, `gir1.2-gtk-4.0`, `gir1.2-vte-2.91`, `polkit`, `pciutils`) denetler ve kurar.
2. Kaynak kodları `/usr/share/parslinux/parslinux-amd-intel-installer/` dizinine yerleştirir.
3. Çalıştırılabilir ikili dosyayı `/usr/bin/parslinux-amd-intel-installer` altına sembolik bağlar.
4. Masaüstü kısayolunu (`org.parslinux.amd-intel-installer.desktop`) ve AppStream meta verilerini kopyalar.
5. PolicyKit kuralını (`org.parslinux.pkexec.parslinux-amd-intel-installer.policy`) yetkilendirme dizinine kurar.
6. İkon ve masaüstü önbelleklerini yeniler.

---

## 2. Paket Yöneticisi ile Kurulum

### Debian / ParsLinux (.deb)
```bash
# Önceden derlenmiş paketi kurun:
sudo dpkg -i dist/parslinux-amd-intel-installer_1.0.0-1_all.deb
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
sudo apt purge parslinux-amd-intel-installer
```
