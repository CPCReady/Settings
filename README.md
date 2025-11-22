# CPCReady Config - Desktop Application

Aplicación de escritorio multiplataforma para configurar CPCReady, construida con PySide6 y empaquetada con Briefcase.

## Características

- 🖥️ **Multiplataforma**: Funciona en Windows, macOS y Linux
- 🎨 **Interfaz moderna**: Construida con PySide6 (Qt6)
- ⚙️ **Configuración TOML**: Gestión de configuración basada en archivos TOML
- 💾 **Gestión de drives**: Configura archivos DSK para Drive A y B
- 🎮 **Emuladores**: Soporte para RetroVirtualMachine, M4Board y CPCEmu
- 🖥️ **Configuración CPC**: Configura modelo, modo de video y número de usuario

## Requisitos

- Python 3.8 o superior
- pip

## Instalación de Briefcase

```bash
pip install briefcase
```

## Desarrollo

### Ejecutar en modo desarrollo

```bash
briefcase dev
```

Este comando ejecuta la aplicación directamente desde el código fuente sin necesidad de empaquetar.

### Crear la aplicación

```bash
briefcase create
```

Este comando crea la estructura de la aplicación para tu plataforma.

### Construir la aplicación

```bash
briefcase build
```

Este comando compila la aplicación.

### Ejecutar la aplicación construida

```bash
briefcase run
```

### Empaquetar para distribución

```bash
briefcase package
```

Este comando crea un paquete distribuible:
- **Windows**: Instalador MSI
- **macOS**: Archivo DMG
- **Linux**: AppImage o paquete del sistema

## Construcción para múltiples plataformas

Para construir para diferentes plataformas, necesitas ejecutar Briefcase en cada sistema operativo:

### Windows
```bash
briefcase create windows
briefcase build windows
briefcase package windows
```

### macOS
```bash
briefcase create macOS
briefcase build macOS
briefcase package macOS
```

### Linux
```bash
briefcase create linux
briefcase build linux
briefcase package linux
```

## Estructura del Proyecto

```
CPCReadyConfig/
├── pyproject.toml              # Configuración de Briefcase
├── src/
│   └── cpcreadyconfig/
│       ├── __init__.py         # Inicialización del paquete
│       ├── __main__.py         # Punto de entrada
│       ├── app.py              # Código principal de la aplicación
│       └── resources/
│           └── icon.png        # Icono de la aplicación
├── app.py                      # Código original (mantener para referencia)
└── icon.png                    # Icono original (mantener para referencia)
```

## Configuración

La aplicación guarda su configuración en:
- **Linux/macOS**: `~/.config/cpcready/cpcready.toml`
- **Windows**: `%USERPROFILE%\.config\cpcready\cpcready.toml`

## Personalización

### Cambiar el icono

Reemplaza `src/cpcreadyconfig/resources/icon.png` con tu propio icono. Briefcase convertirá automáticamente el PNG a los formatos necesarios para cada plataforma.

### Modificar metadatos

Edita `pyproject.toml` para cambiar:
- Nombre de la aplicación
- Versión
- Autor
- Descripción
- URL del proyecto

## Solución de Problemas

### Error: "No module named 'PySide6'"

Asegúrate de que Briefcase esté instalado correctamente:
```bash
pip install --upgrade briefcase
```

### La aplicación no encuentra el icono

Verifica que `src/cpcreadyconfig/resources/icon.png` existe y es un archivo PNG válido.

### Problemas en Linux con Qt

Instala las dependencias del sistema necesarias:
```bash
sudo apt-get install libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
```

## Licencia

MIT

## Soporte

Para reportar problemas o solicitar características, por favor abre un issue en el repositorio del proyecto.
