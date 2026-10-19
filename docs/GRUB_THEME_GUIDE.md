# 🖥️ GRUB ve Çekirdek Grafik Parametreleri (`GRUB_THEME_GUIDE.md`)

Bu belge, AMD ve Intel grafik sürücülerinin ParsLinux GRUB önyükleyicisi ve çekirdek açılış parametreleri ile uyumluluğunu açıklamaktadır.

---

## 1. AMD & Intel Çekirdek Modülleri

- **AMD:** Çekirdek `amdgpu` modülünü otomatik yükler. Modern kartlar (GCN 3 ve sonrası) varsayılan olarak bu modülü kullanır.
- **Intel:** Çekirdek `i915` veya yeni nesil kartlar için `xe` modülünü kullanır.

---

## 2. Sorun Giderme Açılış Parametreleri

Eski donanımlar veya özel GPU yapılandırmalarında `/etc/default/grub` dosyasına eklenebilecek parametreler:
- AMD eski kartları `amdgpu` modülüne zorlama:
  ```bash
  radeon.si_support=0 amdgpu.si_support=1 radeon.cik_support=0 amdgpu.cik_support=1
  ```
- Intel Xe sürücüsünü deneme (12. nesil ve üzeri):
  ```bash
  i915.force_probe=!device_id xe.force_probe=device_id
  ```

Parametreleri uyguladıktan sonra:
```bash
sudo update-grub
```
