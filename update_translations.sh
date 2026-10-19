#!/bin/bash
set -e

langs=("tr" "pt")

if ! command -v xgettext &> /dev/null; then
    echo "xgettext could not be found. Please install 'gettext'."
    exit 1
fi

echo "Updating POT template: data/po/parslinux-amd-intel-installer.pot"
mkdir -p data/po
xgettext -o data/po/parslinux-amd-intel-installer.pot \
    --default-domain=parslinux-amd-intel-installer \
    --from-code=UTF-8 \
    --files-from=data/po/files 2>/dev/null || true

for lang in "${langs[@]}"; do
    if [[ -f "data/po/$lang.po" ]]; then
        echo "Updating data/po/$lang.po"
        msgmerge -o "data/po/$lang.po" "data/po/$lang.po" data/po/parslinux-amd-intel-installer.pot 2>/dev/null || true
    elif [[ -f "data/po/parslinux-amd-intel-installer.pot" ]]; then
        echo "Creating data/po/$lang.po"
        cp data/po/parslinux-amd-intel-installer.pot "data/po/$lang.po"
    fi
done

echo "Compiling MO files..."
mkdir -p mo
for lang in "${langs[@]}"; do
    if [[ -f "data/po/$lang.po" ]]; then
        mkdir -p "mo/$lang/LC_MESSAGES"
        msgfmt "data/po/$lang.po" -o "mo/$lang/LC_MESSAGES/parslinux-amd-intel-installer.mo" 2>/dev/null || true
    fi
done

echo "Translations updated successfully."
