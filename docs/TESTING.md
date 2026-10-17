# 🧪 Test ve Kalite Doğrulama Kılavuzu (`TESTING.md`)

Bu belge, **ParsLinux Nvidia Installer** üzerindeki birim testleri, donanım simülatörü ve arayüz doğrulama yöntemlerini açıklamaktadır.

---

## 1. Otomatik Birim Testleri (Unit Tests)

Proje, fiziksel bir NVIDIA kartı gerektirmeyen kapsamlı bir test takımına sahiptir:

```bash
# Tüm birim testlerini çalıştırın:
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Test Edilen Kritik Alanlar:
- **Güvenlik Doğrulaması (`test_package_name_validation`):** Komut enjeksiyonu ve geçersiz paket adlarının engellenmesi.
- **Yeniden Başlatma Bayrağı (`test_reboot_required_detection`):** Çekirdek güncelleme durumunun tespiti.
- **Dağıtım Sürüm Ayrıştırma (`test_debian_major_parsing`):** ParsLinux ve Debian sürümlerinin doğru eşlenmesi.
- **Simülatör Donanım Verisi (`test_debug_simulation_mode`):** Debug modunda mock GPU ve sürücü listesinin doğru üretilmesi.
- **Varlık ve XML Doğrulaması (`test_assets_and_metadata_exist`):** Glade, CSS, SVG ve AppStream dosyalarının sağlamlığı.

---

## 2. Masaüstünde Canlı Arayüz Testi (Simülasyon Modu)

Mevcut makinenizde fiziksel NVIDIA kartı yoksa bile arayüzü tam işlevsel olarak test edebilirsiniz:

```bash
# Simülasyon modunda başlatma:
./run.sh --debug
```

Bu modda:
- Simüle edilmiş bir NVIDIA GeForce RTX 4070 Ti kartı ekrana gelir.
- Donanım detay sayfası, sürücü versiyonları ve simülasyon terminali etkileşimli olarak test edilebilir.

---

## 3. Paket Derleme Testi

Dağıtım paketlerinin sorunsuz üretildiğini doğrulamak için:

```bash
./package.sh
```

`dist/` dizini altında hem Debian (`.deb`) hem de Arch Linux (`.pkg.tar.zst`) paketlerinin üretildiğini teyit edin.
