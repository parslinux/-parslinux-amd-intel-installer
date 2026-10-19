# 🤝 Katkıda Bulunma Kılavuzu (Contributing Guide)

ParsLinux projesine ve `parslinux-amd-intel-installer` aracına katkı sağlamak istediğiniz için teşekkür ederiz!

## 🌿 Geliştirme Ortamı Kurulumu

1. Projeyi yerel makinenize klonlayın:
   ```bash
   git clone git@github.com:parslinux/-parslinux-amd-intel-installer.git
   cd -parslinux-amd-intel-installer
   ```
2. Geliştirme bağımlılıklarını kurun:
   - **Debian / ParsLinux:** `sudo apt install python3 python3-gi gir1.2-gtk-4.0 gir1.2-vte-2.91 gir1.2-polkit-1.0 pciutils hwdata gettext`
   - **Arch / CachyOS:** `sudo pacman -S python python-gobject gtk4 vte3 polkit hwdata pciutils gettext`
3. Uygulamayı simülasyon modunda çalıştırın:
   ```bash
   ./run.sh --debug
   ```

## 🧪 Testler

Yapılan her değişikliğin ardından birim testleri çalıştırın:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## 🌐 Çevirileri Güncelleme

Kod içerisinde yeni metinler eklendiğinde:
```bash
./update_translations.sh
```

## 📬 Pull Request Süreci

1. Yeni bir özellik dalı (feature branch) oluşturun: `git checkout -b ozellik/yeni-fonksiyon`
2. Temiz, açıklayıcı commit mesajları yazın.
3. PR göndermeden önce testlerin sorunsuz geçtiğinden emin olun.
