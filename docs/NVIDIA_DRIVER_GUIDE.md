# 🎮 NVIDIA Sürücü ve Donanım Rehberi (`NVIDIA_DRIVER_GUIDE.md`)

Bu kılavuz, ParsLinux üzerinde NVIDIA ekran kartı aileleri, sürücü sürümleri, Wayland uyumluluğu ve Optimus melez grafik yapılandırmalarını detaylandırır.

---

## 1. NVIDIA Donanım Mimarileri ve Sürücü Eşleşmeleri

| Mimari Ailesi | Örnek GPU Modelleri | Önerilen Sürücü Dalı | Durum |
|---|---|---|---|
| **Blackwell & Ada Lovelace** | RTX 5090, RTX 4090, 4080, 4070, 4060 | `nvidia-driver` (550+ / 560+) | Tam Kararlı / DLSS 3.5 |
| **Ampere** | RTX 3090, 3080, 3070, 3060 | `nvidia-driver` (550+) | Tam Kararlı / DLSS 2/3 |
| **Turing** | RTX 2080, 2070, 2060, GTX 1660 | `nvidia-driver` (550+) | Tam Kararlı |
| **Pascal** | GTX 1080, 1070, 1060, 1050 | `nvidia-driver` (470.xx / 550) | Kararlı Destek |
| **Maxwell & Kepler** | GTX 980, 970, 780, 680 | `nvidia-legacy-470xx-driver` | Eski Sürücü Desteği |
| **Fermi ve Öncesi** | GTX 580, 480, 9800 GT | `xserver-xorg-video-nouveau` | Açık Kaynak Sürücü |

---

## 2. NVIDIA Optimus & Melez Dizüstü Sistemleri

İki GPU'ya (Intel/AMD entegre + NVIDIA harici) sahip dizüstü bilgisayarlarda:
- **Güç Tasarrufu Modu**: ParsLinux Nvidia Installer içerisindeki "İkincil Kartı Kapat" özelliği ile NVIDIA GPU PCI veriyolundan uyutularak batarya ömrü 2-3 katına çıkarılır.
- **Yüksek Performans Modu**: Kart etkinleştirildiğinde `prime-run` veya Vulkan katmanları aracılığıyla oyunlar harici kartta başlatılır:
  ```bash
  prime-run steam
  # veya
  __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia oyun-adi
  ```

---

## 3. Wayland ve Modern Ekran Sunucusu Desteği

ParsLinux GNOME ve Wayland masaüstü ortamlarında modern NVIDIA sürücüleri (`>= 550`):
- `nvidia-drm.modeset=1` çekirdek parametresi ile doğrudan çalışır.
- XWayland üzerinden tüm oyunlarda tam ekran ve VRR (G-Sync) desteği sunar.
