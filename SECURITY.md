# 🔒 Güvenlik Politikası (Security Policy)

## 🛡️ Desteklenen Sürümler

| Sürüm | Destek Durumu |
|---|---|
| `1.0.x` | ✅ Aktif Güvenlik Desteği |
| `< 1.0.0` | ❌ Desteklenmiyor |

---

## 🔐 Güvenlik Mimarisi

`parslinux-nvidia-installer` ayrıcalıklı sistem yetkileriyle donanım ve sürücü yönetimi yapmaktadır. Güvenlik ilkeleri:

1. **En Az Yetki İlkesi (Least Privilege):** Grafik arayüzü (`src/Main.py`, `src/MainWindow.py`) sıradan kullanıcı haklarıyla çalışır.
2. **PolicyKit Doğrulaması:** Paket ve çekirdek seviyesindeki tüm kritik işlemler PolicyKit (`pkexec`) üzerinden `src/package.py` aracılığıyla yürütülür.
3. **Katı Paket Beyaz Listesi (Whitelist Validation):**
   - Yalnızca `^nvidia-[a-zA-Z0-9\-_]+$`, `xserver-xorg-video-nouveau` ve `^linux-headers-[a-zA-Z0-9\.\-_+]+$` şablonlarına uyan paketlerin kurulumuna izin verilir.
   - Komut veya parametre enjeksiyonu (`--reinstall`, `;`, `&&`, yol geçişi vb.) kesin olarak reddedilir.
4. **Donanım Koruması:** Birincil ekran bağdaştırıcısı (`boot_vga=1`) hiçbir koşulda sistemden kaldırılmaz.

---

## 🚨 Güvenlik Açığı Bildirimi

Bir güvenlik açığı tespit ettiğinizde lütfen bunu herkese açık issue sayfalarında paylaşmak yerine şu adrese iletiniz:
- **E-posta:** `security@parslinux.org`
- Bildiriminiz 48 saat içerisinde değerlendirilecek ve en geç 7 iş günü içinde düzeltme yayınlanacaktır.
