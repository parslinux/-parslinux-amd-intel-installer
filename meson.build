project('parslinux-nvidia-installer', version: '1.0.0')

# Configuration
gnome = import('gnome')

prefix = get_option('prefix')
sysconfdir = get_option('sysconfdir')
var_dir = get_option('var_dir')
data_dir = join_paths(prefix, get_option('datadir'))
icon_dir = join_paths(prefix, 'share', 'icons', 'hicolor', 'scalable', 'apps')
policy_dir = join_paths(prefix, 'share', 'polkit-1', 'actions')

desktop_file = 'org.parslinux.nvidia-installer.desktop'
polkit_file = 'org.parslinux.pkexec.parslinux-nvidia-installer.policy'
desktop_file_dir = join_paths(prefix, 'share', 'applications')
service_file = 'pni-disable-gpu.service'
service_runner = 'pni-disable-gpu.sh'
update_translation_file = 'update_translations.sh'
nvidia_pub = 'nvidia.pub'

# Target installation directory
source_dir = join_paths(prefix, 'share', 'parslinux', 'parslinux-nvidia-installer')

install_data([desktop_file], install_dir : desktop_file_dir)
install_data(['images/parslinux-nvidia-installer.svg'], install_dir : icon_dir)
install_data(['parslinux-nvidia-installer', 'images/parslinux-nvidia-installer.svg'], install_dir : source_dir)
install_data([polkit_file], install_dir : policy_dir)
install_data([service_runner, update_translation_file], install_dir : source_dir, install_mode : 'rwxr-xr-x')
install_data([service_file], install_dir : '/lib/systemd/system/', install_mode : 'rw-r--r--')

install_subdir('data', install_dir : source_dir)
install_subdir('src', install_dir : source_dir)
install_subdir('ui', install_dir : source_dir)
install_subdir('images', install_dir : source_dir)

install_data(['parslinux-nvidia-installer'], install_dir : prefix / 'bin')
install_data([nvidia_pub], install_dir : source_dir)

# locale settings
subdir('data/po')
