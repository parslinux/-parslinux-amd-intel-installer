# 🤖 Claude & Yapay Zeka Asistan Yönergeleri (`CLAUDE.md`)

Bu belge, Claude ve diğer yapay zeka kodlama asistanlarının **parslinux-nvidia-installer** projesinde çalışırken uyması gereken temel kuralları tanımlar.

---

## 1. Proje Özeti
- **Ad:** `parslinux-nvidia-installer`
- **Hedef:** ParsLinux için tek tıkla resmi NVIDIA sürücü kurulum ve yönetim aracı
- **Teknoloji:** Python 3, PyGObject (GTK+ 3.0), VTE (Virtual Terminal Emulator), PolicyKit
- **Lisans:** GNU General Public License v3.0 (GPL-3.0)

---

## 2. Temel Kurallar ve Kısıtlamalar

1. **Pardus ve TÜBİTAK Referansı Bırakmama**: Kod, metin, yorum satırları, UI etiketleri veya dosya adlarında eski "pardus" veya "tubitak/bilgem" referansı bırakılmamalıdır (yalnızca geriye dönük uyumluluk symlink'leri hariç).
2. **Donanım Bağımsızlığı ve Mock Mekanizması**: Geliştirme ortamında veya CI sunucularında fiziksel bir NVIDIA kartı bulunmayabilir. `src/nvidia.py` ve `src/MainWindow.py` içerisindeki simülasyon ve mock mantığı kesinlikle bozulmamalıdır.
3. **Güvenlik ve Yetkilendirme**: GUI asla doğrudan `root` olarak çalıştırılmamalıdır. Sistem işlemlerini tetiklerken daima PolicyKit (`pkexec`) ve `src/package.py` kullanılmalıdır.
4. **Pango Biçimlendirme Kuralları**: GTK etiketlerinde pango markup kullanılırken `<br/>` kullanılmamalı, standart satır sonu (`\n`) kullanılmalıdır.
5. **Vektörel Grafik Standartları**: Arayüze eklenecek tüm yeni görseller SVG formatında, optimize edilmiş ve ParsLinux tasarım çizgisine uygun olmalıdır.
6. **Birim Testleri**: Yapılan her mantıksal değişiklikten sonra `python3 -m unittest discover -s tests -p "test_*.py" -v` komutu çalıştırılmalı ve testlerin tamamının geçtiği teyit edilmelidir.
