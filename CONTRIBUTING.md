# 🤝 Katkıda Bulunma Kılavuzu (Contributing Guide)

ParsLinux projesine ve `parslinux-nvidia-installer` aracına katkı sağlamak istediğiniz için teşekkür ederiz!

## 🌿 Geliştirme Ortamı Kurulumu

1. Projeyi yerel makinenize klonlayın:
   ```bash
   git clone https://github.com/parslinux/parslinux-nvidia-installer.git
   cd parslinux-nvidia-installer
   ```
2. Geliştirme bağımlılıklarını kurun:
   - **Debian / ParsLinux:** `sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-vte-2.91 gir1.2-polkit-1.0 pciutils gnupg gettext`
   - **Arch / CachyOS:** `sudo pacman -S python python-gobject gtk3 vte3 polkit hwdata gnupg gettext`
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
