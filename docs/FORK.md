# 🐆 ParsLinux Fork Raporu & Teknik Değişiklikler

## 📌 Kaynak Bilgisi
- **Kaynak Proje:** `pardus-nvidia-installer`
- **Kaynak Depo:** `https://github.com/pardus/pardus-nvidia-installer`
- **Hedef Proje:** `parslinux-nvidia-installer`
- **Sürüm:** `1.0.0`
- **Tarih:** 17 Ekim 2026

---

## 🛠️ Gerçekleştirilen Başlıca Dönüşümler

### 1. Markalama ve İsimlendirme Standardizasyonu
- İkili komut adı `pardus-nvidia-installer` -> `parslinux-nvidia-installer` olarak güncellendi; geriye dönük uyumluluk için sembolik bağ korundu.
- Sistem kurulum dizini `/usr/share/pardus/pardus-nvidia-installer` yerine modern `/usr/share/parslinux/parslinux-nvidia-installer` hiyerarşisine taşındı.
- Masaüstü dosyası `org.parslinux.nvidia-installer.desktop` ve AppStream dosyası `data/org.parslinux.nvidia-installer.metainfo.xml` olarak standartlaştırıldı.
- PolicyKit kimliği `org.parslinux.pkexec.parslinux-nvidia-installer` olarak tanımlandı, geriye dönük Pardus kuralları için ikincil eylem kaydı eklendi.
- Eski Pardus logoları kaldırılarak ParsLinux kurumsal SVG ikonları (`parslinux-logo.svg`, `parslinux-nvidia-installer.svg`) entegre edildi.

### 2. Donanım & Çevre Bağımsızlığı (Simülasyon / Debug Desteği)
- **Sorun:** Orijinal araç yalnızca fiziksel NVIDIA kartı takılı olan ve `python3-apt` kurulu Debian sistemlerde açılıyordu; sanal makinelerde veya geliştirici ortamlarında (Intel/AMD GPU) hata veriyor veya boş pencere açıyordu.
- **Çözüm:** 
  - `PARSLINUX_NVI_DEBUG=1` ortam değişkeni, `--debug` bayrağı veya `/etc/parslinux-nvi.debug` dosyası ile tam donanım simülasyonu eklendi.
  - Fiziksel kart bulunmadığında geliştiriciye otomatik olarak örnek NVIDIA RTX donanımı ve sürücü seçenekleri sunularak arayüzün test edilebilmesi sağlandı.
  - `apt` kütüphanesinin bulunmadığı sistemlerde (Arch / CachyOS / Fedora geliştirme ortamları) MockAptCache motoru devreye girerek çökmeler engellendi.

### 3. Çoklu Dağıtım ve PCI Veriyolu Uyumluluğu
- Debian'daki `/usr/share/misc/pci.ids` yoluna ek olarak Arch/Fedora dağıtımlarında kullanılan `/usr/share/hwdata/pci.ids` ve `/usr/share/pci.ids` yolları da tarayıcıya eklendi.
- Dağıtım tespit mekanizması (`_debian_major()`) ParsLinux kimliğini (`/etc/parslinux_version`, `ID=parslinux`, `DEBIAN_CODENAME`) otomatik tanıyacak şekilde genişletildi.

### 4. Çift Paketleme Desteği
- Debian tabanlı sistemler için `debian/` dizini güncellendi.
- Arch Linux / CachyOS tabanlı sistemler için `PKGBUILD` ve `.SRCINFO` oluşturuldu.
- `package.sh` betiğine `ar` ve `tar` tabanlı yerel `.deb` ve `makepkg` tabanlı `.pkg.tar.zst` derleyicileri eklendi.

### 5. Geliştirici ve Operasyonel Araçlar
- `run.sh`: Yerel geliştirme ve simülasyon başlatıcısı.
- `stop.sh`: Güvenli süreç durdurucu.
- `install.sh`: Bağımlılık denetimli tek komutla kurulum.
- `uninstall.sh`: Sistemden eksiksiz temizleme.
- `manage.sh`: İnteraktif TUI master yönetim konsolu.
- `tests/test_nvidia_installer.py`: Güvenlik, model, ayrıştırıcı ve XML doğrulama birim testleri.
