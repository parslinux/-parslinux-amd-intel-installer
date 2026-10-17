# 🛡️ Donanım Durumu ve Veri Koruma Kılavuzu (`DATA_SAVING_GUIDE.md`)

Bu kılavuz, grafik sürücüsü kurulumu, melez GPU güç yönetimi ve olası ekran açılmama durumlarında sistemin güvenliğini ve veri bütünlüğünü koruma yöntemlerini açıklar.

---

## 1. Durum Dosyaları ve Önbellek Yönetimi

ParsLinux Nvidia Installer, sistem genelindeki donanım kararlarını durum dosyaları ile takip eder:

- **GPU Devre Dışı Bırakma Belirteci:**
  - `/var/cache/parslinux-nvi-disable-gpu` (ve geriye dönük `/var/cache/pni-disable-gpu`)
  - Melez (Hybrid/Optimus) dizüstü bilgisayarlarda harici NVIDIA kartı kapatıldığında bu dosya oluşturulur.
  - Açılışta `pni-disable-gpu.service` servisi bu dosyanın varlığını kontrol ederek kartı uyku kipine sokar ve pil tasarrufu sağlar.
- **Yeniden Başlatma Belirteci:**
  - `/var/run/reboot-required`
  - Sürücü veya çekirdek modülü kurulduktan sonra oluşturulur; masaüstü ortamına ve kullanıcıya sistemin yeniden başlatılması gerektiğini bildirir.

---

## 2. Olası Sürücü Hatalarında Geri Alma (Rollback)

NVIDIA tescilli sürücüsü kurulduktan sonra masaüstü açılmazsa veya siyah ekranda kalırsa:

1. Açılışta GRUB ekranında `e` tuşuna basarak çekirdek parametrelerine `nomodeset` ekleyin veya Kurtarma Modunu (Recovery Mode) seçin.
2. Konsol oturumuna girin (`Ctrl+Alt+F2` - `F6`).
3. Açık kaynaklı `nouveau` sürücüsüne geri dönmek için CLI komutunu çalıştırın:
   ```bash
   sudo pkexec /usr/share/parslinux/parslinux-nvidia-installer/src/package.py install-nouveau
   ```
4. Sistemi yeniden başlatın:
   ```bash
   sudo reboot
   ```
5. Bu işlem, NVIDIA tescilli modüllerini kara listeden çıkarır ve temiz masaüstü açılışı sağlar.
