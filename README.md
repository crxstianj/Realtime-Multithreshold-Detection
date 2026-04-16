# Realtime Multithreshold Detection

Detección de objetos en tiempo real mediante segmentación por múltiples umbrales en el espacio de color **HSV** usando Python y OpenCV.

---

## ¿Qué hace?

Captura video en vivo desde la cámara y aplica **múltiples rangos de umbral HSV** simultáneamente para detectar y segmentar objetos por color en tiempo real. Cada umbral puede representar un color o categoría distinta, permitiendo identificar varios objetos al mismo tiempo en un solo frame.

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| OpenCV | Captura de video y procesamiento de imagen |
| HSV Color Space | Base para la segmentación por umbral |
| NumPy | Operaciones con matrices y máscaras |

---

## Instalación y uso

```bash
# Clonar el repositorio
git clone https://github.com/crxstianj/Realtime-Multithreshold-Detection.git
cd Realtime-Multithreshold-Detection

# Instalar dependencias
pip install opencv-python numpy

# Ejecutar
python hsv.py
```

> Asegúrate de tener una cámara conectada o usar una fuente de video alternativa.

---

## ¿Por qué HSV?

El espacio de color HSV (Hue, Saturation, Value) es mucho más robusto que RGB para segmentación por color, ya que **separa el tono del brillo**, haciendo la detección resistente a cambios de iluminación.
