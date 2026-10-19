# 📦 ParsLinux AMD & Intel Installer — Paketleme ve Dağıtım Kılavuzu

Bu belge, `parslinux-amd-intel-installer` aracının paketleme standartlarını, dosya yerleşimlerini ve dağıtım süreçlerini açıklar.

---

## 1. Dosya Yerleşim Standartları (Filesystem Hierarchy)

| Kaynak Yol | Hedef Sistem Yolu | İzin | Açıklama |
|---|---|---|---|
| `parslinux-amd-intel-installer` | `/usr/bin/parslinux-amd-intel-installer` | `0755` | Ana çalıştırılabilir ikili dosya |
| `parslinux-amd-intel-installer.svg` | `/usr/share/icons/hicolor/scalable/apps/` | `0644` | Hicolor ölçeklenebilir uygulama ikonu |
| `org.parslinux.amd-intel-installer.desktop` | `/usr/share/applications/` | `0644` | XDG masaüstü kısayolu |
| `org.parslinux.pkexec.parslinux-amd-intel-installer.policy` | `/usr/share/polkit-1/actions/` | `0644` | PolicyKit yetki kuralı |
| `data/org.parslinux.amd-intel-installer.metainfo.xml` | `/usr/share/metainfo/` | `0644` | AppStream / Yazılım Merkezi metaverisi |
| `src/*` | `/usr/share/parslinux/parslinux-amd-intel-installer/src/` | `0644/0755` | Uygulama Python modülleri |
| `ui/*` | `/usr/share/parslinux/parslinux-amd-intel-installer/ui/` | `0644` | Glade / GTK4 arayüz tanımları |
| `data/assets/*` | `/usr/share/parslinux/parslinux-amd-intel-installer/data/assets/` | `0644` | ParsLinux logoları ve grafik kartı görselleri |

---

## 2. Otomatik Paket İnşası (`package.sh`)

Paketleme aracı bağımlılıkları otomatik algılar ve inşa eder:

```bash
# Otomatik tespit ve derleme
./package.sh

# Sadece Debian (.deb)
./package.sh --deb

# Sadece Arch Linux (.pkg.tar.zst)
./package.sh --arch
```

Çıktılar `dist/` dizinine yerleştirilir:
- `dist/parslinux-amd-intel-installer_1.0.0-1_all.deb`
- `dist/parslinux-amd-intel-installer-1.0.0-1-any.pkg.tar.zst`
