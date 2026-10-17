# 📊 İlerleme ve Yol Haritası (`progress.md`)

## 📌 Tamamlanan Görevler (v1.0.0)
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
- [x] Birim test takımının oluşturulması (`tests/test_nvidia_installer.py`, 12/12 başarılı).
- [x] Tam standartlaştırılmış dokümantasyon seti (`docs/`) ve `.claudeignore` oluşturulması.

---

## 🎯 Gelecek Hedefler (v1.1.0+)
- [ ] Gelişmiş Wayland / PRIME profil seçici arayüzü (Entegre / NVIDIA / Hibrit).
- [ ] Fan kontrolü, sıcaklık izleme ve VRAM kullanım göstergeleri.
- [ ] CUDA, cuDNN ve TensorRT geliştirici kütüphaneleri için tek tıkla kurulum sihirbazı.
