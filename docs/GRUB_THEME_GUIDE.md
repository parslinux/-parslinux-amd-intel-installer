# 🖥️ Önyükleyici ve Grafik Modu Kılavuzu (`GRUB_THEME_GUIDE.md`)

Bu belge, NVIDIA tescilli grafik sürücülerinin ParsLinux GRUB önyükleyicisi ve çekirdek açılış parametreleri ile uyumluluğunu açıklamaktadır.

---

## 1. Çekirdek Açılış Parametreleri

NVIDIA sürücülerinin Wayland ve yüksek çözünürlüklü konsol kipinde sorunsuz çalışması için `/etc/default/grub` dosyasına aşağıdaki parametreler eklenir:

```ini
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nvidia-drm.modeset=1"
```

Değişiklik yapıldıktan sonra önyükleyici yapılandırması güncellenmelidir:
```bash
sudo update-grub
```

---

## 2. Olası Açılış Kilitlenmelerinde GRUB Müdahalesi

Eğer yeni bir sürücü kurulduktan sonra masaüstü açılmazsa:
1. Bilgisayar açılırken GRUB menüsünde sistem girdisini seçip `e` tuşuna basın.
2. `linux` ile başlayan satırın sonuna `nomodeset` parametresini ekleyin.
3. `F10` veya `Ctrl+X` ile açılışı başlatın.
4. Sistem temel grafik kipinde açıldıktan sonra `parslinux-nvidia-installer` ile sürücüyü onarın veya Nouveau'ya geri dönün.
