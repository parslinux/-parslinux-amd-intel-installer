# 📦 ParsLinux Nvidia Installer — Paketleme ve Dağıtım Kılavuzu

Bu belge, `parslinux-nvidia-installer` aracının paketleme standartlarını, dosya yerleşimlerini ve dağıtım süreçlerini açıklar.

---

## 📂 Dosya Sistemi Yerleşim Haritası

| Kaynak Yol | Hedef Sistem Yolu | İzin | Açıklama |
|---|---|---|---|
| `parslinux-nvidia-installer` | `/usr/bin/parslinux-nvidia-installer` | `0755` | Ana çalıştırılabilir ikili dosya |
| `parslinux-nvidia-installer.svg` | `/usr/share/icons/hicolor/scalable/apps/` | `0644` | Hicolor ölçeklenebilir uygulama ikonu |
| `org.parslinux.nvidia-installer.desktop` | `/usr/share/applications/` | `0644` | XDG masaüstü kısayolu |
| `org.parslinux.pkexec.parslinux-nvidia-installer.policy` | `/usr/share/polkit-1/actions/` | `0644` | PolicyKit yetki kuralı |
| `data/org.parslinux.nvidia-installer.metainfo.xml` | `/usr/share/metainfo/` | `0644` | AppStream / Yazılım Merkezi metaverisi |
| `src/*` | `/usr/share/parslinux/parslinux-nvidia-installer/src/` | `0644/0755` | Uygulama Python modülleri |
| `ui/*` | `/usr/share/parslinux/parslinux-nvidia-installer/ui/` | `0644` | Glade arayüz tanımları |
| `data/nvidia-pci.json` | `/usr/share/parslinux/parslinux-nvidia-installer/data/` | `0644` | PCI donanım ve sürücü eşleme tablosu |
| `data/assets/*` | `/usr/share/parslinux/parslinux-nvidia-installer/data/assets/` | `0644` | ParsLinux logoları ve grafik kartı görselleri |
| `pni-disable-gpu.sh` | `/usr/share/parslinux/parslinux-nvidia-installer/pni-disable-gpu.sh` | `0755` | Melez kart boot yönetim betiği |
| `pni-disable-gpu.service` | `/lib/systemd/system/pni-disable-gpu.service` | `0644` | Systemd açılış servisi |
| `mo/*` | `/usr/share/locale/<dil>/LC_MESSAGES/parslinux-nvidia-installer.mo` | `0644` | Derlenmiş gettext yerelleştirmeleri |

---

## 🛠️ Paket Derleme

### 1. Debian (.deb) Paketi
```bash
./package.sh --deb
```
Çıktı: `dist/parslinux-nvidia-installer_1.0.0-1_all.deb`

### 2. Arch Linux (.pkg.tar.zst) Paketi
```bash
./package.sh --arch
```
Çıktı: `dist/parslinux-nvidia-installer-1.0.0-1-any.pkg.tar.zst`

---

## 🚀 ParsLinux ISO ve Canlı Ortam Entegrasyonu

Canlı ISO kalıbında yer alması için `pars-desktop-gnome` veya `pars-gaming` meta paketine şu bağımlılık eklenir:

```
Depends: parslinux-nvidia-installer
```
Kurulum sırasında `pni-disable-gpu.service` servisi otomatik etkinleştirilir ve sistem ilk açıldığında donanımı taramaya hazır hale gelir.
