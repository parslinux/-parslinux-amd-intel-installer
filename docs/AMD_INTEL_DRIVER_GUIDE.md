# 🎮 AMD & Intel Sürücü ve Donanım Rehberi (`AMD_INTEL_DRIVER_GUIDE.md`)

Bu kılavuz, ParsLinux üzerinde AMD Radeon ve Intel grafik işlemcileri, çekirdek sürücü modülleri (`amdgpu`, `i915`, `xe`), Vulkan katmanları, donanım video çözme (VA-API / QuickSync) ve melez grafik yapılandırmalarını detaylandırır.

---

## 1. Donanım Mimarileri ve Çekirdek Sürücüleri

### AMD Radeon
| Mimari Ailesi | Örnek GPU Modelleri | Çekirdek Modülü | Vulkan Sürücüsü | Durum |
|---|---|---|---|---|
| **RDNA 3 / 3.5** | RX 7900 XTX, RX 7800 XT, Radeon 780M/890M | `amdgpu` | `vulkan-radeon` (RADV) | Mükemmel / Ray Tracing |
| **RDNA 2** | RX 6900 XT, RX 6700 XT, RX 6600 | `amdgpu` | `vulkan-radeon` (RADV) | Tam Kararlı / FSR 3 |
| **RDNA 1** | RX 5700 XT, RX 5600 XT, RX 5500 | `amdgpu` | `vulkan-radeon` (RADV) | Tam Kararlı |
| **GCN 4 / 5 (Polaris/Vega)** | RX 580, RX 570, Vega 56/64, Radeon VII | `amdgpu` | `vulkan-radeon` (RADV) | Tam Kararlı |
| **GCN 1-3 (Eski)** | HD 7000, R9 200/300 serisi | `radeon` / `amdgpu` | `vulkan-radeon` | Eski Mimari |

### Intel Graphics & Arc
| Mimari Ailesi | Örnek GPU Modelleri | Çekirdek Modülü | Vulkan Sürücüsü | Durum |
|---|---|---|---|---|
| **Intel Arc (Battlemage)** | B580, B570 | `xe` | `vulkan-intel` (ANV) | Yeni Nesil Destek |
| **Intel Arc (Alchemist)** | A770, A750, A580, A380 | `i915` / `xe` | `vulkan-intel` (ANV) | Tam Kararlı / XeSS |
| **Intel Xe (Core Ultra / 11-14. Nesil)** | Iris Xe, Meteor Lake, Lunar Lake | `i915` / `xe` | `vulkan-intel` (ANV) | Tam Kararlı |
| **Intel UHD / HD (6-10. Nesil)** | Skylake, Kaby Lake, Comet Lake UHD 630 | `i915` | `vulkan-intel` (ANV) | Kararlı |
| **Eski Intel HD** | Broadwell, Haswell ve öncesi | `i915` | Eski Mesa | Temel 2D/3D |

---

## 2. Vulkan Sürücü Seçenekleri ve Karşılaştırma

### AMD: RADV vs AMDVLK
- **RADV (`vulkan-radeon` / Mesa):** ParsLinux ve topluluk tarafından **varsayılan ve önerilen** sürücüdür. Valve'ın katkılarıyla geliştirilmiş ACO shader derleyicisini kullanır, oyunlarda en yüksek FPS ve en düşük stuttering (takılma) oranını sağlar.
- **AMDVLK (`amdvlk`):** AMD'nin kendi açık kaynaklı Vulkan sürücüsüdür. LLVM shader derleyicisi kullanır. Özel geliştirme ve doğrulama ortamlarında tercih edilir.

### Intel: ANV (Mesa Vulkan Intel)
- Intel Arc ve Iris Xe grafik yongaları için en gelişmiş açık kaynak Vulkan sürücüsüdür. Modern oyunlarda DXVK ve VKD3D-Proton ile mükemmel uyumluluk gösterir.

---

## 3. Donanım Video Hızlandırma (VA-API & QuickSync)

Web tarayıcılarında (YouTube 4K/60fps) ve medya oynatıcılarda (VLC, MPV) CPU kullanımını sıfıra indirmek ve batarya ömrünü artırmak için gerekli paketler:

- **AMD Donanımları:**
  - `mesa-va-drivers` (VA-API)
  - `mesa-vdpau-drivers` (VDPAU)
- **Intel Donanımları:**
  - `intel-media-driver` (iHD - Broadwell ve sonrası için modern sürücü)
  - `libva-intel-driver` (i965 - Eski Intel GPU'lar için)

Sistemdeki VA-API durumunu test etmek için:
```bash
vainfo
```

---

## 4. Melez (Hybrid / PRIME) Çift GPU Yönetimi

Intel iGPU + AMD dGPU veya AMD APU + AMD dGPU yapılandırmalarında:

- Masaüstü ve basit pencereler varsayılan olarak entegre kartta (düşük güç tüketimi) çalışır.
- Bir uygulamayı veya oyunu güçlü harici kartta başlatmak için:
  ```bash
  DRI_PRIME=1 steam
  # veya
  DRI_PRIME=1 %command%
  ```
- ParsLinux AMD & Intel Installer, oyun başlatıcılarını (Steam, Lutris, Heroic) tek tıkla `DRI_PRIME=1` ortam değişkeniyle yapılandırabilir.

---

## 5. Hesaplama ve Yapay Zeka (Compute & AI)

- **AMD ROCm:** Radeon GPU'lar üzerinde PyTorch, TensorFlow ve Blender OpenCL/HIP hızlandırması için `rocm-hip-runtime`, `rocm-opencl-runtime` kütüphanelerini sunar.
- **Intel oneAPI & Compute Runtime:** Intel Arc ve Xe GPU'lar üzerinde OpenCL, Level Zero ve Intel OpenVINO hızlandırması sağlar.
