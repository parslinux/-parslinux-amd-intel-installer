# ⌨️ ParsLinux AMD & Intel Installer — CLI ve Yardımcı Başvuru Kılavuzu

## 🚀 Komut Satırı Seçenekleri

```bash
parslinux-amd-intel-installer [SEÇENEKLER]
```

| Seçenek | Kısa Kod | Açıklama |
|---|---|---|
| `--help` | `-h` | Komut satırı seçeneklerini ve kullanım kılavuzunu görüntüler. |
| `--debug` | `-g` | Simüle edilmiş AMD & Intel GPU donanım ve sürücü görünümünü açar. |
| `--version` | `-v` | Uygulama sürüm bilgisini görüntüler ve çıkar. |
| `--detect` | `-d` | Sistemdeki AMD & Intel donanımlarını terminalde listeler. |
| `--json` | `-j` | Donanım tespit sonucunu JSON formatında yazdırır. |
| `--details` | | Donanım ve grafik katmanları detay sayfasını doğrudan açar. |
| `--tray` | `-t` | Arka planda sistem tepsisinde (AppIndicator / Tray) çalışır. |

---

## 🛠️ Yönetim ve Geliştirici Betikleri

| Betik | Kullanım Örneği | Açıklama |
|---|---|---|
| `run.sh` | `./run.sh [--debug]` | Geliştirme ortamında uygulamayı çalıştırır. Kart yoksa otomatik simülasyona geçer. |
| `stop.sh` | `./stop.sh` | Arka planda çalışan tüm uygulayıcı süreçleri güvenle sonlandırır. |
| `install.sh` | `./install.sh [--no-deps]` | Sistem geneline kurulum yapar ve önbellekleri yeniler. |
| `uninstall.sh` | `./uninstall.sh` | Sistemden tüm bileşenleri temiz bir şekilde kaldırır. |
| `package.sh` | `./package.sh [--deb\|--arch]` | Dağıtıma uygun `.deb` veya `.pkg.tar.zst` paketlerini derler. |
| `manage.sh` | `./manage.sh [komut]` | Master kontrol paneli (interaktif terminal menüsü). |

---

## 🔐 Ayrıcalıklı Yardımcı (src/package.py)

`package.py`, PolicyKit (`pkexec`) yetkilendirmesi altında çağrılan arka plan yürütücüsüdür:

```bash
pkexec /usr/share/parslinux/parslinux-amd-intel-installer/src/package.py <ALT_KOMUT> [PARAMETRELER]
```

### Desteklenen Alt Komutlar:
1. `install-vulkan <amd|intel|both>`: Seçilen donanım için resmi açık kaynak Vulkan sürücülerini kurar.
2. `install-vaapi <amd|intel|both>`: Donanım video hızlandırma kütüphanelerini (VA-API / QuickSync) yapılandırır.
3. `install-compute <amd|intel>`: ROCm veya oneAPI / OpenCL kütüphanelerini sisteme kurar.
4. `prime-mode <integrated|hybrid|performance>`: Melez dizüstü sistemler için GPU güç profilini değiştirir.
5. `set-game-offload <1|0>`: Tüm oyun ve başlatıcılar için global `DRI_PRIME=1` yapılandırmasını açar/kapatır.
