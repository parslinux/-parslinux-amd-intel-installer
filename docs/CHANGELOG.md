# 📝 Değişiklik Günlüğü (`CHANGELOG.md`)

Tüm önemli değişiklikler bu dosyada belgelenecektir. Format [Keep a Changelog](https://keepachangelog.com/) standardına uygundur.

---

## [1.2.0] - 2026-10-17

### 🚀 Gelişmiş Donanım Monitörü, Sistem Tepsisi ve Güç Yönetimi
- **Modern 4 Sekmeli Arayüz**:
  - `Gtk.StackSwitcher` ile sekmeli mimariye geçildi: **🎮 Sürücüler**, **📊 Donanım & Güç**, **🕹️ Oyun**, **🧠 Yapay Zeka**.
- **Canlı Telemetri ve Sensörler (`src/monitor.py`)**:
  - `nvidia-smi` üzerinden gerçek zamanlı GPU çekirdek sıcaklığı, fan hızı, VRAM bellek kullanımı ve güç çekimi (Watt) takibi.
  - Donanım bulunmayan geliştirici ortamlarında otomatik simülatör telemetrisi.
- **Donanım Fan ve Güç Limiti Kontrolü**:
  - Kullanıcı tanımlı fan hızı kaydırıcısı (%20 - %100) ve manuel fan kontrolü (`nvidia-settings`).
  - Ayarlanabilir GPU maksimum güç tüketim limiti (TDP 100W - 350W) (`nvidia-smi -pl`).
- **PRIME GPU Güç Profili Seçici**:
  - Melez dizüstü bilgisayarlar için dinamik profil yönetimi:
    - 🍃 **Tasarruf (Intel/iGPU)**: NVIDIA GPU tamamen uykuya alınır.
    - ⚡ **Hibrit (On-Demand)**: Yalnızca talep eden uygulamalarda NVIDIA kullanılır.
    - 🚀 **Performans (NVIDIA)**: Tüm ekran sunumu ve grafikler harici GPU'da çalışır.
- **Sistem Tepsisi (AppIndicator / Tray) Arka Plan Göstergesi (`src/tray.py`)**:
  - `--tray` / `-t` seçeneğiyle arka planda sistem tepsisinde çalışabilme.
  - Canlı sıcaklık ve profil etiket göstergesi (`45°C • Hibrit`).
  - Hızlı profil değiştirme menüsü ve ana kontrol paneli kısayolu.
- **Oyun ve Başlatıcı Merkezi (Gaming Hub)**:
  - Sistemde yüklü oyun platformlarının (Steam, Lutris, Heroic, Bottles) otomatik tespiti ve durumu.
  - Global otomatik NVIDIA PRIME Offload anahtarı (`/etc/environment.d/10-nvidia-gaming.conf`).
- **Yapay Zeka ve CUDA Geliştirici Kiti**:
  - Tek tıkla CUDA Toolkit (`nvidia-cuda-toolkit`), cuDNN (`libcudnn8`) ve TensorRT kütüphanelerinin kurulum sihirbazı.
- **Genişletilmiş Birim Testleri**:
  - Birim test kapsamı 20/20'ye yükseltildi (`tests/test_nvidia_installer.py`).

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
