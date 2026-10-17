# 🌐 Yerel Depoda Barındırma Kılavuzu (`SELF_HOSTING_GUIDE.md`)

Bu belge, `parslinux-nvidia-installer` paketinin ve resmi NVIDIA sürücülerinin kurumsal ağlarda, intranet ortamlarında veya yerel ParsLinux APT depolarında nasıl barındırılacağını açıklar.

---

## 1. Reprepro ile Yerel APT Deposu Kurulumu

```bash
# Gerekli araçları kurun
sudo apt install reprepro gnupg nginx

# Depo kök dizini
sudo mkdir -p /var/www/repo/conf
```

`/var/www/repo/conf/distributions` yapılandırma dosyası:
```ini
Origin: ParsLinux
Label: ParsLinux Driver Repository
Codename: pars
Architectures: amd64 all
Components: main contrib non-free
Description: ParsLinux Official & Proprietary Drivers Repository
SignWith: default
```

---

## 2. Paketi Yerel Depoya Ekleme

Derlenen `.deb` paketini depoya dahil etmek için:

```bash
reprepro -b /var/www/repo includedeb pars dist/parslinux-nvidia-installer_1.0.0-1_all.deb
```

---

## 3. İstemci Sistemlerde Depoyu Tanımlama

İstemci ParsLinux makinelerinde `/etc/apt/sources.list.d/parslinux-local.list` dosyası oluşturulur:

```ini
deb [trusted=yes] http://repo.yerel.ag/repo pars main contrib non-free
```

Ardından istemcide önbellek güncellenir ve kurulum yapılabilir:
```bash
sudo apt update
sudo apt install parslinux-nvidia-installer
```
