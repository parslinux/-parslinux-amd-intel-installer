# 🐆 ParsLinux Fork Raporu & Teknik Değişiklikler

## 📌 Kaynak Bilgisi
- **Kaynak Temel:** `parslinux-graphics-installer` (Ayrıştırılmış Açık Kaynak Tabanı)
- **Hedef Proje:** `parslinux-amd-intel-installer`
- **Sürüm:** `1.0.0`
- **Tarih:** 19 Ekim 2026

---

## 🛠️ Gerçekleştirilen Başlıca Dönüşümler

### 1. Markalama ve İsimlendirme Standardizasyonu
- İkili komut adı `parslinux-amd-intel-installer` olarak güncellendi.
- Sistem kurulum dizini modern `/usr/share/parslinux/parslinux-amd-intel-installer` hiyerarşisine taşındı.
- Masaüstü dosyası `org.parslinux.amd-intel-installer.desktop` ve AppStream dosyası `data/org.parslinux.amd-intel-installer.metainfo.xml` olarak standartlaştırıldı.
- PolicyKit kimliği `org.parslinux.pkexec.parslinux-amd-intel-installer` olarak tanımlandı.

### 2. Donanım Kapsamı & AMD/Intel Dönüşümü
- Eski tek marka kısıtlamaları kaldırılarak hem AMD Radeon hem de Intel (Arc/Iris/UHD) mimarileri ve melez GPU yapılandırmaları için dönüştürüldü.
- Vulkan katmanları (`RADV`, `ANV`, `AMDVLK`) ve 32-bit multilib oyun kütüphaneleri yönetimi eklendi.
- Donanım video hızlandırma (VA-API / QuickSync) optimizasyonları eklendi.
- AMD ROCm ve Intel oneAPI / OpenCL hesaplama kütüphaneleri entegrasyonu sağlandı.

### 3. Çoklu Dağıtım ve PCI Veriyolu Uyumluluğu
- Hem Debian hem Arch Linux / CachyOS paket yapılandırmaları (`.deb` ve `.pkg.tar.zst`) sağlandı.
- PCI veritabanı tarayıcısı `1002` (AMD) ve `8086` (Intel) aygıtlarını tanıyacak şekilde uyarlandı.
