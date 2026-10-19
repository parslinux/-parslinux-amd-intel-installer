# 🌍 Çeviri ve Yerelleştirme Rehberi (`TRANSLATION_GUIDE.md`)

Bu rehber, **ParsLinux AMD & Intel Installer** arayüzünün ve sistem iletilerinin çoklu dil desteğine (GNU gettext) nasıl katkı sağlanacağını açıklar.

---

## 1. Çeviri Dosyalarının Konumu

- `po/parslinux-amd-intel-installer.pot`: Ana şablon dosyası
- `po/tr.po`: Türkçe çeviriler
- `po/en.po`: İngilizce çeviriler

---

## 2. Yeni Dil Ekleme

```bash
msginit -i po/parslinux-amd-intel-installer.pot -o po/de.po -l de_DE.UTF-8
```
