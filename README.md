# Obsidian to BookStack Transfer Tool

Esta herramienta te permite transferir el contenido de tu bóveda de Obsidian a una instancia de BookStack a través de su API, organizando el contenido en estantes.

## Características

- ✅ Transfiere archivos Markdown de Obsidian a páginas de BookStack
- ✅ Mantiene el formato Markdown original (no convierte a HTML)
- ✅ Organiza carpetas de primer nivel como libros separados
- ✅ Convierte carpetas de segundo nivel en capítulos dentro de los libros
- ✅ Maneja enlaces internos de Obsidian `[[enlace]]`
- ✅ Procesa frontmatter YAML
- ✅ Configuración mediante archivo JSON
- ✅ Modo de simulación (dry-run)
- ✅ **NUEVO**: Transferencia automática de imágenes embebidas
- ✅ **NUEVO**: Transferencia automática de adjuntos (PDF, DOCX, etc.)
- ✅ **NUEVO**: Soporte para sintaxis de imágenes de Obsidian `![[imagen.png]]` y Markdown `![alt](imagen.png)`
- ✅ **NUEVO**: Soporte para enlaces de adjuntos de Obsidian `[[documento.pdf]]` y Markdown `[texto](archivo.docx)`
- ✅ **NUEVO**: Resolución automática de rutas de imágenes y adjuntos relativas y absolutas
- ✅ **NUEVO**: Salida con colores y estadísticas detalladas de transferencia
- ✅ **NUEVO**: Reporte de errores detallado en el resumen final
- ✅ **NUEVO**: Prueba de conexión integrada con diagnósticos detallados (`--test-connection`)
- ✅ **NUEVO**: Validación inteligente de configuración con mensajes de error claros
- ✅ **NUEVO**: Detección automática de tokens de ejemplo y configuraciones incorrectas

## Requisitos

- Python 3.7+
- Una instancia de BookStack con API habilitada
- Tokens de API de BookStack
- Una bóveda de Obsidian local

## Instalación

### Opción 1: Configuración automática (Recomendado)

1. Clona o descarga este repositorio
2. Ejecuta el script de configuración:

**En macOS/Linux:**
```bash
source setup_env.sh
```

**En Windows:**
```cmd
setup_env.bat
```

Esto creará automáticamente el entorno virtual e instalará las dependencias.

### Opción 2: Configuración manual

1. Clona o descarga este repositorio
2. Crea un entorno virtual:

```bash
python3 -m venv obsidian_env
```

3. Activa el entorno virtual:

**En macOS/Linux:**
```bash
source obsidian_env/bin/activate
```

**En Windows:**
```cmd
obsidian_env\Scripts\activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de BookStack

### 1. Habilitar la API

En tu instancia de BookStack:
1. Ve a **Configuración** → **Características**
2. Habilita **API REST**

### 2. Crear tokens de API

1. Ve a tu **Perfil de usuario**
2. En la sección **Tokens de API**, crea un nuevo token
3. Guarda el **Token ID** y **Token Secret**

## Configuración del programa

### 1. Crear archivo de configuración

Copia el archivo de ejemplo y personalízalo:

```bash
cp config.json.example config.json
```

Edita `config.json` con tus datos:

```json
{
  "bookstack": {
    "url": "https://tu-bookstack.com",
    "token_id": "tu_token_id_aqui",
    "token_secret": "tu_token_secret_aqui"
  },
  "obsidian": {
    "vault_path": "/ruta/a/tu/boveda/obsidian"
  },
  "transfer": {
    "book_name": "Contenido de Obsidian",
    "shelf_name": "Contenido de Obsidian"
  }
}
```

### 2. Configurar parámetros

- **bookstack.url**: URL completa de tu instancia BookStack
- **bookstack.token_id**: Tu Token ID de la API
- **bookstack.token_secret**: Tu Token Secret de la API
- **obsidian.vault_path**: Ruta completa a tu bóveda de Obsidian
- **transfer.book_name**: Nombre del libro por defecto (usado como fallback)
- **transfer.shelf_name**: Nombre del estante principal que contendrá todos los libros (por defecto: "Contenido de Obsidian")

## Uso

### Prueba de conexión

Antes de realizar cualquier transferencia, es recomendable probar la conexión con BookStack:

```bash
python obsidian_to_bookstack.py config.json --test-connection
```

Esta opción realiza una verificación completa:
- ✅ Conectividad básica con BookStack
- 🔑 Validación de tokens de API
- 📚 Verificación de permisos para crear/eliminar libros
- 📄 Acceso a APIs de páginas y capítulos
- 🎯 Diagnósticos detallados en caso de errores

### Modo Dry-Run

Puedes simular la transferencia sin crear contenido real para ver qué se transferiría:

```bash
python obsidian_to_bookstack.py config.json --dry-run
```

### Transferencia

Una vez verificada la conexión y revisado el dry-run:

```bash
python obsidian_to_bookstack.py config.json
```

El modo dry-run mostrará:
- ✅ Verificación de conexión con BookStack
- 📁 Estructura de libros y capítulos que se crearían
- 📄 Lista de páginas que se transferirían
- 📊 Resumen con conteo de libros, capítulos y páginas
- ⚠️ Detección de errores sin realizar cambios reales

### Verificación de la transferencia

El modo dry-run te permite verificar qué contenido se transferirá antes de realizar cambios reales:

- 🏗️ Muestra la estructura de libros y capítulos que se crearían
- 📝 Lista todas las páginas que se transferirían
- 🖼️ Identifica qué imágenes se subirán correctamente
- 📎 Detecta qué adjuntos se procesarán
- ⚠️ Reporta archivos no encontrados o errores potenciales
- 📊 Proporciona un resumen completo con estadísticas
 
## Estructura de transferencia

La herramienta organiza automáticamente el contenido siguiendo esta lógica jerárquica:
- **Estante principal** → Contiene todos los libros transferidos
- **Carpetas de primer nivel** → **Libros** en BookStack
- **Carpetas de segundo nivel** → **Capítulos** dentro de los libros
- **Archivos .md** → **Páginas** en libros o capítulos

### Ejemplo de estructura jerárquica

```
Obsidian Vault/
├── Proyectos/
│   ├── Web/
│   │   ├── frontend.md
│   │   └── backend.md
│   ├── Mobile/
│   │   └── app.md
│   └── proyecto_general.md
├── Notas/
│   ├── Reuniones/
│   │   └── reunion1.md
│   └── nota_suelta.md
└── archivo_raiz.md
```

Se convierte en:

```
BookStack:
└── Shelf: "Contenido de Obsidian" (estante principal)
    ├── Book: "Proyectos"
    │   ├── Chapter: "Web"
    │   │   ├── Page: "Frontend"
    │   │   └── Page: "Backend"
    │   ├── Chapter: "Mobile"
    │   │   └── Page: "App"
    │   └── Page: "Proyecto General" (página directa del libro)
    ├── Book: "Notas"
    │   ├── Chapter: "Reuniones"
    │   │   └── Page: "Reunion1"
    │   └── Page: "Nota Suelta" (página directa del libro)
    └── Book: "Archivos Raíz"
        └── Page: "Archivo Raiz"
```

### Reglas de organización

1. **Estante principal** → Se crea automáticamente con el nombre configurado (por defecto "Contenido de Obsidian")
2. **Archivos en la raíz** → Se agrupan en un libro llamado "Archivos Raíz"
3. **Archivos en carpetas de primer nivel** → Se convierten en páginas directas del libro
4. **Archivos en carpetas de segundo nivel o más profundas** → Se convierten en páginas del capítulo correspondiente
5. **Carpetas vacías** → Se ignoran automáticamente
6. **Todos los libros** → Se organizan automáticamente dentro del estante principal

## Formato de contenido

La herramienta transfiere el contenido en **formato Markdown original**, preservando:

- **Encabezados**: `# H1`, `## H2`, etc.
- **Énfasis**: `**negrita**`, `*cursiva*`
- **Enlaces Obsidian**: `[[enlace]]`, `[[enlace|alias]]`
- **Enlaces normales**: `[texto](url)`
- **Código inline**: `` `código` ``
- **Bloques de código**: ` ```código``` `
- **Listas**: `- item`, `1. item`
- **Tablas**: Sintaxis de tablas Markdown
- **Citas**: `> cita`

BookStack se encarga de renderizar el Markdown automáticamente en su interfaz.

## Frontmatter

Si tus archivos de Obsidian tienen frontmatter YAML:

```yaml
---
title: "Mi Título Personalizado"
tags: [tag1, tag2]
---

Contenido del archivo...
```

La herramienta usará el título del frontmatter como nombre de la página en BookStack.

## Manejo de imágenes y adjuntos

La herramienta incluye **transferencia automática de imágenes y adjuntos** con las siguientes características:

### Formatos soportados

**Imágenes:**
- **Sintaxis Obsidian**: `![[imagen.png]]`, `![[carpeta/imagen.jpg]]`
- **Sintaxis Markdown**: `![alt text](imagen.png)`, `![](../assets/imagen.gif)`

**Adjuntos:**
- **Sintaxis Obsidian**: `[[documento.pdf]]`, `[[carpeta/archivo.docx]]`
- **Sintaxis Markdown**: `[Descargar PDF](documento.pdf)`, `[Ver archivo](../docs/archivo.xlsx)`

### Resolución de rutas

La herramienta busca imágenes y adjuntos en el siguiente orden:

1. **Ruta relativa al archivo**: `./images/foto.png`, `./docs/documento.pdf`
2. **Ruta relativa a la raíz del vault**: `assets/imagen.jpg`, `attachments/archivo.docx`
3. **Búsqueda por nombre**: Si no encuentra el archivo en las rutas anteriores, busca cualquier archivo con ese nombre en todo el vault

### Proceso de transferencia

1. **Detección**: Escanea el contenido Markdown buscando referencias de imágenes y adjuntos
2. **Resolución**: Encuentra la ubicación real de cada archivo en el sistema de archivos
3. **Subida**: Sube cada archivo a BookStack como adjunto de la página
4. **Actualización**: Reemplaza las referencias originales con las URLs de BookStack
5. **Estadísticas**: Muestra un resumen detallado con contadores de éxito y errores

### Verificación en dry-run

En modo dry-run, la herramienta:

- ✅ Muestra qué imágenes y adjuntos se encontraron y subirán
- ❌ Reporta archivos no encontrados
- 📍 Indica la ruta exacta donde se encontró cada archivo
- 🔗 Muestra cómo se actualizarán las referencias
- 📊 Proporciona estadísticas detalladas de archivos procesados

Cuando ejecutes el modo de simulación, verás:

```
📄 Mi Documento → Mi Libro (2 imágenes)
  🖼️  foto1.png ✓
  🖼️  diagrama.jpg ✗ (no encontrada)
```

Esto te permite verificar qué imágenes se transferirán correctamente antes de ejecutar la transferencia real.

### Formatos soportados

**Imágenes:**
- **PNG**: `.png`
- **JPEG**: `.jpg`, `.jpeg`
- **GIF**: `.gif`
- **WebP**: `.webp`
- **SVG**: `.svg`
- **BMP**: `.bmp`

**Adjuntos:**
- **Documentos**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`
- **Hojas de cálculo**: `.xls`, `.xlsx`, `.csv`
- **Presentaciones**: `.ppt`, `.pptx`
- **Archivos comprimidos**: `.zip`, `.rar`, `.7z`
- **Otros**: Cualquier tipo de archivo que BookStack permita

## Validación de Configuración

La herramienta incluye validación inteligente que detecta automáticamente errores comunes de configuración:

### Errores Detectados Automáticamente

- ✅ **Archivos de configuración faltantes o corruptos**
- ✅ **Secciones y campos requeridos faltantes**
- ✅ **Tokens de API vacíos o con valores de ejemplo**
- ✅ **URLs mal formateadas** (sin http:// o https://)
- ✅ **Rutas de vault de Obsidian inexistentes**
- ✅ **Tokens que parecen ser valores de ejemplo**

### Mensajes de Error Mejorados

Cuando hay problemas de configuración, recibirás mensajes claros con soluciones específicas:

```bash
❌ Errores en la configuración:
   1. Campo 'bookstack.token_id' está vacío - necesitas configurar tus tokens de API
   2. La ruta del vault de Obsidian no existe: /ruta/incorrecta

💡 Soluciones:
   • Copia config.json.example a config.json
   • Edita config.json con tus datos reales
   • Para obtener tokens de API, ve a BookStack > Configuración > Tokens de API
   • Asegúrate de que la ruta del vault de Obsidian sea correcta
```

### Comandos de Diagnóstico

```bash
# Validar configuración sin hacer cambios
python obsidian_to_bookstack.py config.json --dry-run

# Probar conexión con diagnósticos detallados
python obsidian_to_bookstack.py config.json --test-connection
```

## Control de Rate Limiting

Para evitar errores de "Demasiadas solicitudes (429)" al subir imágenes y adjuntos, puedes configurar un retardo entre peticiones:

```json
{
  "transfer": {
    "request_delay_seconds": 1.0
  }
}
```

### Valores Recomendados

- **0.0**: Sin delay (por defecto) - Máxima velocidad
- **0.5**: Balance entre velocidad y estabilidad
- **1.0**: Recomendado para la mayoría de servidores
- **2.0**: Para servidores muy restrictivos

### Mecanismo de Retry Automático

Si aún ocurren errores 429, el sistema implementa un mecanismo de retry automático con backoff exponencial:

- **Primer intento**: Espera 2 segundos
- **Segundo intento**: Espera 4 segundos  
- **Tercer intento**: Espera 8 segundos
- **Después de 3 intentos**: Reporta el error

Esto se aplica automáticamente a todas las operaciones de subida de imágenes y adjuntos.

## Solución de problemas

### Diagnóstico inicial

**Siempre ejecuta primero la prueba de conexión:**

```bash
python obsidian_to_bookstack.py config.json --test-connection
```

Esta herramienta te ayudará a identificar rápidamente:
- Problemas de conectividad
- Errores de autenticación
- Problemas de permisos
- Configuración incorrecta

### Error de conexión

- Verifica que la URL de BookStack sea correcta
- Asegúrate de que la API esté habilitada
- Comprueba que los tokens sean válidos
- Usa `--test-connection` para diagnóstico detallado

### Error de permisos

- Verifica que tu usuario tenga permisos para crear libros y páginas
- Comprueba que los tokens no hayan expirado
- El flag `--test-connection` probará automáticamente los permisos necesarios

### Archivos no encontrados

- Verifica que la ruta de la bóveda de Obsidian sea correcta
- Asegúrate de que existan archivos `.md` en la bóveda

### Caracteres especiales

- La herramienta maneja UTF-8, pero algunos caracteres especiales pueden necesitar ajustes
- Revisa la configuración de encoding si tienes problemas

### Problemas con imágenes y adjuntos

**Archivos no encontrados:**
- Ejecuta primero el dry-run para ver qué archivos no se encuentran
- Verifica que las rutas en tus archivos Markdown sean correctas
- Asegúrate de que las imágenes y adjuntos existan en tu vault de Obsidian
- Revisa que no haya caracteres especiales en los nombres de archivo

**Error al subir archivos:**
- Verifica que tu usuario tenga permisos para subir archivos en BookStack
- Comprueba que el tamaño de los archivos no exceda los límites de BookStack
- Revisa la configuración de almacenamiento de archivos en BookStack
- Verifica que el formato del archivo sea soportado por BookStack

**Archivos muy grandes:**
- BookStack puede tener límites de tamaño de archivo
- Considera comprimir archivos grandes antes de la transferencia
- Verifica la configuración `upload_max_filesize` en tu servidor

**Problemas específicos con adjuntos:**
- Comprueba la configuración de adjuntos en BookStack
- Verifica que tu usuario tenga permisos para subir diferentes tipos de archivo
- Revisa los límites de tipos de archivo permitidos en BookStack

## Limitaciones actuales

- Los enlaces internos `[[enlace]]` se mantienen como texto (no se convierten a enlaces de BookStack)
- No se preservan las etiquetas de Obsidian
- No procesa plugins específicos de Obsidian
- No transfiere metadatos de archivos (fechas de creación, modificación)
- No maneja enlaces bidireccionales automáticamente
- No procesa bloques de código embebidos de otros archivos
- No transfiere configuraciones específicas de Obsidian (temas, plugins, etc.)

## Contribuir

Si encuentras bugs o quieres agregar características:

1. Reporta issues con detalles específicos
2. Propón mejoras
3. Envía pull requests

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

**Autor**: Miguel Navarro  
**Año**: 2025  
**Versión**: 1.1

### Changelog v1.1
- ✅ Agregado flag `--test-connection` para diagnósticos detallados
- ✅ Integrada funcionalidad de prueba de conexión en el script principal
- ✅ Mejorada la experiencia de usuario con verificaciones previas
- ✅ Eliminados archivos de prueba redundantes (`test_connection.py`, `test_images.py`)
- ✅ Actualizada documentación y ejemplos de uso

**¡Importante!** Siempre haz una copia de seguridad de tu contenido antes de ejecutar transferencias masivas.