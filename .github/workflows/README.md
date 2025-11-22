# GitHub Actions - Build and Release

Este workflow compila automáticamente CPCReady Config para Windows, macOS y Linux.

## Cómo usar

### Opción 1: Crear un release con tag (recomendado)

```bash
# Crear y push un tag de versión
git tag v1.0.0
git push origin v1.0.0
```

El workflow se ejecutará automáticamente y creará un release con los paquetes para las tres plataformas.

### Opción 2: Ejecutar manualmente

1. Ve a la pestaña "Actions" en GitHub
2. Selecciona "Build and Release" en la lista de workflows
3. Haz clic en "Run workflow"
4. Selecciona la rama y haz clic en "Run workflow"

**Nota**: Si ejecutas manualmente, los artefactos se generarán pero NO se creará un release automáticamente. Deberás descargarlos desde la página del workflow.

## Artefactos generados

- **macOS**: `CPCReady Config-X.X.X.dmg`
- **Windows**: `CPCReady Config-X.X.X.msi`
- **Linux**: `CPCReady Config-X.X.X.AppImage`

## Requisitos

- El repositorio debe tener permisos de escritura para crear releases
- Los tags deben seguir el formato `vX.X.X` (ejemplo: `v1.0.0`)

## Notas

- La compilación para macOS usa firma ad-hoc (solo para testing)
- Para distribución pública en macOS, necesitas un certificado de desarrollador de Apple
- Los paquetes de Windows y Linux no están firmados
