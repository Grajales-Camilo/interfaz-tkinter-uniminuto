# Interfaz Tkinter — Taller Comparativo UNIMINUTO

App de escritorio en Python + Tkinter que replica la funcionalidad de un e-commerce conectado a Firebase, construida como **Stack B** de un taller comparativo de interfaces.

## Stack A vs Stack B

| | Stack A | Stack B |
|---|---|---|
| Tecnología | React (web) | Python + Tkinter (escritorio) |
| Despliegue | GitHub Pages | Ejecutable `.exe` (PyInstaller) |
| Datos | Firestore REST API | Firestore REST API |

## Funcionalidades

- Carga de productos desde Firestore al arrancar
- Búsqueda por nombre con filtrado local
- Vista de detalle con imagen, precio USD y precio COP
- Precios COP calculados desde tasa de cambio en `settings/exchange_rate`
- Instrumentación de métricas M2, M3 y M4 con `time.perf_counter()`

## Requisitos

```
Python 3.13+
requests
Pillow
```

```bash
pip install requests Pillow
```

## Uso

```bash
python app.py
```

## Empaquetar como .exe

```bash
pip install pyinstaller
pyinstaller --onefile app.py
```

El ejecutable queda en `dist/app.exe`.

## Métricas medidas

| Métrica | Qué mide |
|---|---|
| M2 | Tiempo de carga inicial de productos desde Firestore |
| M3 | Tiempo de descarga de imagen desde Firebase Storage |
| M4 | Tiempo de filtrado local al presionar Buscar |

Al cerrar la ventana se imprime un resumen de promedios en consola.
