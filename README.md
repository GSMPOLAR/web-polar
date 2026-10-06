# GSM-POLAR • Suite de Escritorio y Web

> **trabajando en nuevos procesos lo mejor en garantias polar**

---

## 🖥️ ¿Cómo iniciar la aplicación de escritorio?

Tienes 3 formas sencillas de abrir la ventana de escritorio:

1. **Doble clic (Recomendado):**
   Haz doble clic sobre el archivo [iniciar_escritorio.bat](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/iniciar_escritorio.bat). Se abrirá la ventana directamente sin consola negra de fondo.

2. **Desde la terminal con Python:**
   ```powershell
   python imei_desktop.py
   ```
   O sin consola:
   ```powershell
   pythonw imei_desktop.pyw
   ```

3. **Herramienta en consola clásica (CLI):**
   ```powershell
   python imei_generator.py
   ```

---

## 🌟 Características de la Aplicación de Escritorio

### 1. 🔍 Pestaña: Verificador (14 / 15 Dígitos)
- Escribe **14 dígitos**: la aplicación calcula al instante el 15º dígito verificador utilizando el **Algoritmo de Luhn (Mod 10)** y destaca el resultado en color.
- Escribe **15 dígitos**: la aplicación comprueba en tiempo real si el IMEI es **VÁLIDO** o **INVÁLIDO**.
- **Desglose completo en tarjetas:**
  - TAC Oficial (8 dígitos GSMA).
  - TAC clásico (6 dígitos) + FAC (2 dígitos).
  - SNR (Número de serie de 6 dígitos).
  - Dígito de control (Check Digit).
- Botón **"Copiar"** para transferir el número completo al portapapeles.

### 2. ⚙️ Pestaña: Generador por Modelos
- Selector de **Marcas** (Samsung, Xiaomi, Apple, Motorola, etc.).
- Selector de **Modelos** que carga automáticamente su código TAC.
- Selector de cantidad (1, 3, 5, 10).
- Tabla interactiva con desglose de campos y botones para:
  - **Copiar Seleccionado**
  - **Copiar Todos**
  - **Limpiar Lista**

### 3. 📱 Pestaña: Modelos y TACs (Sin Programar)
- Visualiza todos los modelos registrados.
- Botón **"➕ Agregar Modelo"**: abre un formulario donde puedes añadir cualquier marca, modelo y TAC de 8 dígitos (o TAC 6d + FAC 2d).
- Botón **"🗑️ Eliminar Seleccionado"**: remueve modelos de la base de datos.
- Botón **"📂 Abrir en Bloc de Notas"**: abre directamente el archivo [tac_database.json](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/tac_database.json) en tu Bloc de Notas de Windows para modificarlo como prefieras.

---

## 🎬 Fondo de Video y Multimedia (`C:\Users\Jhose\Documents\videos`)

La aplicación web y de escritorio integran automáticamente el archivo encontrado en tu carpeta de videos:
- **Archivo activo:** `videoframe_9214.png` (frame de alta resolución con estética de ojos carmesí/anime).
- **Efecto cinemático:** Gradación de color ultra-vívida (`saturate 1.95`), pulso sutil y filtros Liquid Glass no transparentes para máxima legibilidad.
- **Reproductor de Video Integrado:**
  - En la barra superior de la Web ([index.html](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/index.html)), pulsa el botón **🎬** para cargar al instante cualquier video (`.mp4`, `.webm`, etc.) o imagen desde tu carpeta `C:\Users\Jhose\Documents\videos`. El video se reproducirá en bucle continuo de fondo.
  - Si colocas un archivo llamado `video.mp4` o `background.mp4` en esta carpeta, la web lo reproducirá automáticamente al iniciar.

---

## 📁 Archivos principales en esta carpeta

- [index.html](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/index.html): Aplicación Web completa con Liquid Glass, reproductor de video de fondo y cinta interactiva de 15 dígitos.
- [videoframe_9214.png](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/videoframe_9214.png): Frame/fondo copiado desde `C:\Users\Jhose\Documents\videos`.
- [imei_desktop.pyw](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/imei_desktop.pyw) / [imei_desktop.py](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/imei_desktop.py): Aplicación gráfica de escritorio con avatar/logo de la imagen.
- [iniciar_escritorio.bat](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/iniciar_escritorio.bat): Lanzador directo para Windows.
- [tac_database.json](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/tac_database.json): Archivo de configuración de TACs editable.
- [imei_generator.py](file:///C:/Users/Jhose/.gemini/antigravity-ide/scratch/imei_generator.py): Versión para terminal/consola.

