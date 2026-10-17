# ⌨️ ParsLinux Nvidia Installer — CLI ve Yardımcı Başvuru Kılavuzu

## 🚀 Komut Satırı Seçenekleri

```bash
parslinux-nvidia-installer [SEÇENEKLER]
```

| Seçenek | Kısa Kod | Açıklama |
|---|---|---|
| `--help` | `-h` | Komut satırı seçeneklerini ve kullanım kılavuzunu görüntüler. |
| `--debug` | `-g` | Simüle edilmiş NVIDIA GPU donanım ve sürücü görünümünü açar. |
| `--version` | `-v` | Uygulama sürüm bilgisini görüntüler ve çıkar. |
| `--details` | `-d` | Donanım ve sürücü detay sayfasını doğrudan açar. |
| `--remove` | `-r` | Sürücü kaldırma / açık kaynak sürücüye dönme sayfasını açar. |
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
pkexec /usr/share/parslinux/parslinux-nvidia-installer/src/package.py <ALT_KOMUT> [PARAMETRELER]
```

### Desteklenen Alt Komutlar:
1. `install-nvidia <PAKETLER...>`: Seçilen resmi NVIDIA sürücüsünü ve çekirdek başlıklarını kurar.
2. `install-nouveau`: Kapalı kaynak sürücüleri temizler ve açık kaynak nouveau sürücüsünü yapılandırır.
3. `update`: Resmi NVIDIA CUDA / sürücü deposu yapılandırmasını (`dest`) açar/kapatır ve apt listelerini günceller.
4. `disable-sec-gpu`: Melez dizüstü sistemlerde ikincil NVIDIA GPU'yu devre dışı bırakır.
5. `enable-sec-gpu`: Devre dışı bırakılmış NVIDIA GPU'yu yeniden etkinleştirir ve PCI veriyolunu tarar.
6. `prime-mode <intel|on-demand|nvidia>`: Dizüstü bilgisayarlar için PRIME GPU güç ve çalışma profilini değiştirir.
7. `set-fan-speed <YÜZDE_20_100>`: GPU fan dönüş hızını özel yüzdeye ayarlar (`nvidia-settings`).
8. `set-power-limit <WATT_100_350>`: GPU maksimum güç tüketim sınırını (TDP) ayarlar (`nvidia-smi -pl`).
9. `set-game-offload <1|0>`: Tüm oyun ve uygulamalar için global NVIDIA PRIME offload ortam değişkenlerini (`/etc/environment.d`) açar/kapatır.
10. `install-ai-tools`: CUDA Toolkit, cuDNN ve TensorRT kütüphanelerini sisteme kurar.
