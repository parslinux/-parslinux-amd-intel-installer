# 🔗 Dağıtım Entegrasyonu ve Uygulama Bağlama (`UYGULAMA_BAGLAMA.md`)

Bu belge, `parslinux-amd-intel-installer` paketinin ParsLinux dağıtım ekosistemine, ISO kalıplarına ve masaüstü ortamlarına nasıl bağlandığını açıklar.

---

## 1. Masaüstü Ortamı Entegrasyonu (XDG)

Uygulama, ParsLinux GNOME, XFCE ve KDE masaüstü ortamlarına standart XDG spesifikasyonları ile bağlanır:

- **Desktop Girişi:** `/usr/share/applications/org.parslinux.amd-intel-installer.desktop`
- **Menü Kategorisi:** `System;Settings;HardwareSettings;`
- **İkon Konumu:** `/usr/share/icons/hicolor/scalable/apps/parslinux-amd-intel-installer.svg`
- **AppStream Metainfo:** `/usr/share/metainfo/org.parslinux.amd-intel-installer.metainfo.xml`

---

## 2. PolicyKit (Ayrıcalık Yükseltme) Bağlantısı

Grafik arayüz standart kullanıcı ile çalışırken, paket kurulumları ve güç profili değişiklikleri için PolicyKit devreye girer:

- `/usr/share/polkit-1/actions/org.parslinux.pkexec.parslinux-amd-intel-installer.policy`

---

## 3. ParsLinux Canlı Medya ve ISO Kalıplarına Dahil Edilmesi

ParsLinux ISO derleme sisteminde uygulamanın kalıba dahil edilmesi için:

```bash
# ISO paket listesine ekleme:
parslinux-amd-intel-installer
```
