# 🧪 Test ve Kalite Güvencesi (`TESTING.md`)

Bu belge, **ParsLinux AMD & Intel Installer** üzerindeki birim testleri, donanım simülatörü ve arayüz doğrulama yöntemlerini açıklamaktadır.

---

## 1. Birim Testlerini Çalıştırma

Proje, fiziksel bir grafik kartı gerektirmeyen kapsamlı bir test takımına sahiptir:

```bash
# Standart unittest koşucusu:
python3 -m unittest discover -s tests -p "test_*.py" -v

# veya yönetim konsolundan:
./manage.sh test
```

---

## 2. Geliştirici Simülatörü ve Donanım Olmayan Ortamlar

Mevcut makinenizde fiziksel AMD/Intel kartı yoksa veya sanal makinede test ediyorsanız:

```bash
# Simülasyon modunda başlatma:
./run.sh --debug
```

Bu modda:
- Simüle edilmiş AMD Radeon ve Intel Iris Xe donanımları arayüze yüklenir.
- Canlı telemetri, Vulkan durumu ve güç profili bileşenleri GUI üzerinde görselleştirilebilir.
