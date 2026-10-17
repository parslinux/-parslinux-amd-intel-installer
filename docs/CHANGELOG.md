# 📝 Değişiklik Günlüğü (`CHANGELOG.md`)

Tüm önemli değişiklikler bu dosyada belgelenecektir. Format [Keep a Changelog](https://keepachangelog.com/) standardına uygundur.

---

## [1.0.0] - 2026-10-17

### 🎉 İlk Sürüm (ParsLinux Çatallaması)
- `pardus-nvidia-installer` temel alınarak ParsLinux ekosistemi için sıfırdan çatallandı ve modernize edildi.
- Tüm eski marka, TÜBİTAK/BİLGEM ve Pardus kalıntıları temizlendi.

### ✨ Yenilikler ve Geliştirmeler
- **Vektörel Grafik Dönüşümü**:
  - 128x128 piksel modern ParsLinux koyu yeşil/mor yüksek çözünürlüklü uygulama ikonu (`images/parslinux-nvidia-installer.svg`) oluşturuldu.
  - Eski 765 KB'lık piksel bazlı raster görseller silindi; yerine hafif ve net SVG vektörler (`video_card.svg`, `video_card_disabled.svg`, `parslinux-logo.svg`) entegre edildi.
- **Dinamik Logo ve Stil Yükleyici**:
  - `GtkAboutDialog` logosu sistem yolu veya yerel yoldan dinamik olarak yüklenecek şekilde `GdkPixbuf.Pixbuf.new_from_file_at_scale` mekanizmasına kavuşturuldu.
  - Modern koyu tema kartları ve yuvarlatılmış köşeler için `data/style.css` eklendi.
- **Gelişmiş Donanım Tespiti ve Simülasyon**:
  - `src/nvidia.py` içerisine çoklu `pci.ids` arama yolu (`/usr/share/hwdata/pci.ids` ve `/usr/share/misc/pci.ids`) eklendi.
  - Fiziksel NVIDIA kartı bulunmayan geliştirici makinelerinde GUI'nin test edilebilmesi için `--debug` bayrağı ve `PARSLINUX_NVI_DEBUG=1` ortam değişkeniyle çalışan simülasyon motoru (`RTX 4070 Ti`) eklendi.
  - `MockAptCache` katmanı eklenerek Arch Linux ve Debian harici ortamlarda uygulamanın çökmesi engellendi.
- **Sistem Entegrasyonu ve Paketleme**:
  - Standartlaştırılmış yönetim araçları: `run.sh`, `stop.sh`, `install.sh`, `uninstall.sh`, `package.sh`, `manage.sh`.
  - Debian (`parslinux-nvidia-installer_1.0.0-1_all.deb`) ve Arch Linux (`parslinux-nvidia-installer-1.0.0-1-any.pkg.tar.zst`) paketleme altyapısı tamamlandı.
  - PolicyKit kuralı `org.parslinux.pkexec.parslinux-nvidia-installer.policy` olarak güncellendi.
  - Systemd güç tasarruf servisi `pni-disable-gpu.service` ve kabuk betiği `pni-disable-gpu.sh` güncellendi.
- **Test ve Kalite Güvencesi**:
  - `tests/test_nvidia_installer.py` birim test takımı yazıldı (12/12 test geçmektedir).
  - Standart ParsLinux dokümantasyon seti (`docs/`) eklendi.
