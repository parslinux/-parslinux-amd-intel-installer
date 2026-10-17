#!/bin/bash
set -e

langs=("tr" "pt")

if ! command -v xgettext &> /dev/null; then
    echo "xgettext could not be found. Please install 'gettext'."
    exit 1
fi

echo "Updating POT template: data/po/parslinux-nvidia-installer.pot"
xgettext -o data/po/parslinux-nvidia-installer.pot \
    --default-domain=parslinux-nvidia-installer \
    --from-code=UTF-8 \
    --files-from=data/po/files

for lang in "${langs[@]}"; do
    if [[ -f "data/po/$lang.po" ]]; then
        echo "Updating data/po/$lang.po"
        msgmerge -o "data/po/$lang.po" "data/po/$lang.po" data/po/parslinux-nvidia-installer.pot
    else
        echo "Creating data/po/$lang.po"
        cp data/po/parslinux-nvidia-installer.pot "data/po/$lang.po"
    fi
done

echo "Compiling MO files..."
mkdir -p mo
for lang in "${langs[@]}"; do
    mkdir -p "mo/$lang/LC_MESSAGES"
    msgfmt "data/po/$lang.po" -o "mo/$lang/LC_MESSAGES/parslinux-nvidia-installer.mo"
done

echo "Translations updated successfully."
