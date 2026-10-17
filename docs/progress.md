# 📊 İlerleme ve Yol Haritası (`progress.md`)

## 📌 Tamamlanan Görevler (v1.0.0, v1.1.0 & v1.2.0)
- [x] Kaynak kodun `pardus-nvidia-installer` deposundan incelenmesi ve çatallanması.
- [x] Tüm marka ve meta verilerin `parslinux-nvidia-installer` olarak dönüştürülmesi.
- [x] TÜBİTAK/BİLGEM ve Pardus kalıntılarının kaynak koddan temizlenmesi.
- [x] Yüksek çözünürlüklü ParsLinux kurumsal vektörel SVG ikonlarının üretilmesi (`images/` ve `data/assets/`).
- [x] Eski 765 KB'lık raster kart görselinin modern hafif vektörle değiştirilmesi.
- [x] Gtk.Application mimarisinin `NON_UNIQUE` bayrağı ve çoklu argüman desteğiyle modernize edilmesi.
- [x] Donanım olmayan makinelerde sorunsuz test için donanım simülatörü (`--debug` / RTX 4070 Ti) eklenmesi.
- [x] Çoklu PCI ID veritabanı tarayıcısı (`/usr/share/hwdata/pci.ids` & `/usr/share/misc/pci.ids`) eklenmesi.
- [x] Debian harici ortamlarda çökmeleri önleyen `MockAptCache` katmanı eklenmesi.
- [x] `run.sh`, `stop.sh`, `install.sh`, `uninstall.sh`, `package.sh` ve `manage.sh` yönetim araçlarının yazılması.
- [x] Debian `.deb` ve Arch Linux `.pkg.tar.zst` paketlerinin başarıyla inşa edilmesi (`dist/`).
- [x] Birim test takımının oluşturulması (`tests/test_nvidia_installer.py`, 20/20 başarılı).
- [x] Tam standartlaştırılmış dokümantasyon seti (`docs/`) ve `.claudeignore` oluşturulması.
- [x] Gelişmiş Wayland / PRIME profil seçici arayüzü (🍃 Tasarruf / ⚡ Hibrit / 🚀 Performans).
- [x] Canlı telemetri, GPU sıcaklığı, fan hızı ve VRAM kullanım göstergeleri (`src/monitor.py`).
- [x] CUDA Toolkit, cuDNN ve TensorRT geliştirici kütüphaneleri için tek tıkla kurulum sihirbazı.
- [x] Özel GPU fan hızı (%20-%100) ve güç limiti (Power Limit TDP) ayarlayıcısı.
- [x] Oyun bazlı profil yönetimi (Steam, Lutris, Heroic oyunlarında otomatik NVIDIA PRIME offload).
- [x] Sistem tepsisi (AppIndicator / Tray) mini sıcaklık ve mod göstergesi (`src/tray.py`).
- [x] Modern 4 sekmeli (`Gtk.StackSwitcher`) kullanıcı arayüzü tasarımı.

---

## 🎯 Gelecek Hedefler (v1.3.0+)
- [ ] Gelişmiş GPU hız aşırtma (overclock) çekirdek ve bellek frekans kaydırıcıları.
- [ ] Oyun esnasında ekran üzeri canlı FPS ve telemetri göstergesi (MangoHud entegrasyonu).
- [ ] Çoklu monitör G-Sync / VRR (Değişken Yenileme Hızı) yapılandırma asistanı.


