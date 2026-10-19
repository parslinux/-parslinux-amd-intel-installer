# 🌐 Yerel Depo ve Barındırma Kılavuzu (`SELF_HOSTING_GUIDE.md`)

Bu belge, `parslinux-amd-intel-installer` paketinin kurumsal ağlarda, intranet ortamlarında veya yerel ParsLinux APT/Pacman depolarında nasıl barındırılacağını açıklar.

---

## 1. Debian / ParsLinux APT Deposu

Yerel bir reprepro deposuna derlenen paketi eklemek için:

```bash
reprepro -b /var/www/repo includedeb pars dist/parslinux-amd-intel-installer_1.0.0-1_all.deb
```

İstemci makinelerde kurulum:
```bash
sudo apt update
sudo apt install parslinux-amd-intel-installer
```
