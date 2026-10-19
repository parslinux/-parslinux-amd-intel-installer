# 🤖 Claude & Yapay Zeka Asistan Yönergeleri (`CLAUDE.md`)

Bu belge, Claude ve diğer yapay zeka kodlama asistanlarının **parslinux-amd-intel-installer** projesinde çalışırken uyması gereken temel kuralları tanımlar.

---

## 1. Proje Özeti
- **Ad:** `parslinux-amd-intel-installer`
- **Hedef:** ParsLinux için AMD Radeon ve Intel grafik donanımları, Vulkan katmanları, VA-API hızlandırma ve melez GPU yönetim merkezi
- **Teknoloji:** Python 3, PyGObject (GTK 4.0), VTE (Virtual Terminal Emulator), PolicyKit
- **Lisans:** GNU General Public License v3.0 (GPL-3.0)

---

## 2. Temel Kurallar ve Kısıtlamalar

1. **Marka Standardizasyonu**: Kod, metin, yorum satırları, UI etiketleri veya dosya adlarında eski marka referansları bırakılmamalıdır.
2. **Donanım Bağımsızlığı ve Mock Mekanizması**: Geliştirme ortamında veya CI sunucularında fiziksel bir AMD/Intel kartı bulunmayabilir. Simülasyon ve mock mantığı (`--debug`) kesinlikle bozulmamalıdır.
3. **Güvenlik ve Yetkilendirme**: GUI asla doğrudan `root` olarak çalıştırılmamalıdır. Sistem işlemlerini tetiklerken daima PolicyKit (`pkexec`) ve `src/package.py` kullanılmalıdır.
4. **GTK4 Standartları**: Arayüz bileşenlerinde GTK4 API'lerine uyulmalıdır.
5. **Vektörel Grafik Standartları**: Arayüze eklenecek tüm yeni görseller SVG formatında, optimize edilmiş ve ParsLinux tasarım çizgisine uygun olmalıdır.
6. **Birim Testleri**: Yapılan her mantıksal değişiklikten sonra testler çalıştırılmalı ve doğrulanmalıdır.
