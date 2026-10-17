# 🌍 Çeviri ve Yerelleştirme Kılavuzu (`TRANSLATION_GUIDE.md`)

Bu rehber, **ParsLinux Nvidia Installer** arayüzünün ve sistem iletilerinin çoklu dil desteğine (GNU gettext) nasıl katkı sağlanacağını açıklar.

---

## 1. Dizin Yapısı

Çeviri kaynakları `po/` dizininde yer almaktadır:
- `po/parslinux-nvidia-installer.pot`: Ana şablon dosyası
- `po/tr.po`: Türkçe çeviriler
- `po/en.po`: İngilizce çeviriler

Derlenmiş ikili çeviriler ise `mo/` dizini altına oluşturulur.

---

## 2. Çeviri Şablonunu Güncelleme

Kod içerisine yeni metinler eklendiğinde veya var olanlar güncellendiğinde:

```bash
./update_translations.sh
```

Bu betik:
1. Python ve Glade dosyalarındaki `_("metin")` veya `translatable="yes"` ifadelerini tarar.
2. `po/` altındaki `.po` dosyalarını otomatik senkronize eder.
3. `msgfmt` ile derleyerek `mo/` dizinine `.mo` dosyalarını yazar.

---

## 3. Yeni Bir Dil Ekleme

Örneğin Almanca (`de`) desteği eklemek için:

```bash
msginit -i po/parslinux-nvidia-installer.pot -o po/de.po -l de_DE.UTF-8
```

Ardından Poedit veya herhangi bir metin editörüyle `po/de.po` dosyasını düzenleyin ve `./update_translations.sh` çalıştırın.
