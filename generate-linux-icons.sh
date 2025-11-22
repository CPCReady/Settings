#!/bin/bash
# Script para generar iconos en múltiples tamaños para Linux

echo "Generando iconos para Linux desde icon.svg..."

# Verificar que existe ImageMagick
if ! command -v magick &> /dev/null; then
    echo "Error: ImageMagick no está instalado"
    echo "Instala con: brew install imagemagick"
    exit 1
fi

# Verificar que existe el archivo SVG
if [ ! -f "src/cpcreadyconfig/resources/icon.svg" ]; then
    echo "Error: No se encuentra src/cpcreadyconfig/resources/icon.svg"
    exit 1
fi

# Generar iconos en múltiples tamaños
for size in 16 32 64 128 256 512; do
    echo "Generando icon-${size}.png..."
    magick src/cpcreadyconfig/resources/icon.svg \
        -background none \
        -resize ${size}x${size}! \
        src/cpcreadyconfig/resources/icon-${size}.png
done

echo "✅ Iconos generados exitosamente:"
ls -lh src/cpcreadyconfig/resources/icon-*.png

echo ""
echo "Ahora puedes ejecutar:"
echo "  briefcase create linux"
echo "  briefcase build linux"
echo "  briefcase package linux --no-sign"
