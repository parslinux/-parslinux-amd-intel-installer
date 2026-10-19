# 🔒 Güvenlik Politikası (Security Policy)

## 🛡️ Desteklenen Sürümler

| Sürüm | Destek Durumu |
|---|---|
| `1.0.x` | ✅ Aktif Güvenlik Desteği |

---

## 🔐 Güvenlik Mimarisi

`parslinux-amd-intel-installer` ayrıcalıklı sistem yetkileriyle donanım ve sürücü yönetimi yapmaktadır. Güvenlik ilkeleri:

1. **En Az Yetki İlkesi (Least Privilege):** Grafik arayüzü (`src/Main.py`, `src/MainWindow.py`) sıradan kullanıcı haklarıyla çalışır.
2. **PolicyKit Doğrulaması:** Paket ve çekirdek seviyesindeki tüm kritik işlemler PolicyKit (`pkexec`) üzerinden `src/package.py` aracılığıyla yürütülür.
3. **Katı Paket Beyaz Listesi (Whitelist Validation):**
   - Yalnızca grafik, Vulkan, VA-API ve compute kütüphaneleri şablonlarına uyan doğrulanmış parametrelerin işlenmesine izin verilir.
   - Komut veya parametre enjeksiyonu (`;`, `&&`, yol geçişi vb.) kesin olarak reddedilir.
4. **Donanım Koruması:** Birincil ekran bağdaştırıcısı (`boot_vga=1`) hiçbir koşulda sistemden kaldırılmaz veya karartılmaz.

---

## 🚨 Güvenlik Açığı Bildirimi

Bir güvenlik açığı tespit ettiğinizde lütfen bunu herkese açık issue sayfalarında paylaşmak yerine şu adrese iletiniz:
- **E-posta:** `security@parslinux.org`
