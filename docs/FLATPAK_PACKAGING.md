# 📦 Flatpak ve Sandbox Kapsamı Değerlendirmesi (`FLATPAK_PACKAGING.md`)

Bu belge, **ParsLinux Nvidia Installer** aracının neden doğrudan bir Flatpak sandbox paketi olamayacağını ve Flatpak oyun/grafik ekosistemiyle nasıl entegre çalıştığını açıklar.

---

## 1. Mimari Sınırlar ve Sandbox Engelleri

Grafik sürücüsü yükleyicileri, doğası gereği işletim sistemi çekirdeği ve donanım denetimiyle en alt düzeyde etkileşime girer:

- **DKMS ve Çekirdek Modülleri**: Sürücü kurulumu, ana bilgisayardaki Linux çekirdeği için `nvidia.ko`, `nvidia-modeset.ko` ve `nvidia-uvm.ko` modüllerinin derlenmesini ve `/lib/modules/` altına yerleştirilmesini gerektirir.
- **Donanım ve PCI Erişimi**: `/sys/bus/pci/devices` üzerinden aygıtların güç durumunu yönetmek (`power/control`, `remove`) çekirdek düzeyinde yetki gerektirir.
- **APT / Paket Yönetimi**: Sistem paket yöneticisi (`apt-get`) kilit mekanizmalarına ve `/var/lib/dpkg/` veritabanına erişmek Flatpak kısıtlamaları dahilinde mümkün değildir.

Bu nedenlerle `parslinux-nvidia-installer` ana sistem paketi (`.deb` / Arch PKGBUILD) olarak çalışmalıdır.

---

## 2. Flatpak Uygulamalarıyla Entegrasyon (Steam, Lutris, Blender)

ParsLinux üzerinde Flatpak ile çalışan grafik uygulamaları, ana sisteme kurulan NVIDIA sürücüsünü otomatik olarak tanır:

1. `parslinux-nvidia-installer` ana sisteme NVIDIA tescilli sürücüsünü (örn. `550.xx`) kurar.
2. Flatpak, sistemdeki sürücü sürümünü tespit ederek uyumlu grafik katmanını indirir:
   ```bash
   org.freedesktop.Platform.GL.nvidia-550-xx
   ```
3. Kullanıcı Flatpak üzerinden Steam veya Lutris başlattığında tam 3D hızlandırma ve DLSS/Ray Tracing desteği kesintisiz çalışır.
