# 🛡️ Yapılandırma ve Durum Yönetimi Kılavuzu (`DATA_SAVING_GUIDE.md`)

## 1. Sistem Durum Dosyaları

ParsLinux AMD & Intel Installer, sistem genelindeki donanım tercihlerini durum dosyaları ile takip eder:

- `/etc/parslinux-amd-intel-installer.conf`: Genel kullanıcı tercihleri ve varsayılan ayarlar.
- `/etc/environment.d/10-parslinux-gaming.conf`: Global `DRI_PRIME=1` veya MangoHud ortam değişkenleri.

---

## 2. Sorun Giderme ve Sıfırlama

Grafik ayarlarını varsayılana sıfırlamak için:

```bash
sudo rm -f /etc/environment.d/10-parslinux-gaming.conf
```
