# Prompt para Agente — Taller Comparativo Tkinter (UNIMINUTO)

## 1. Contexto del proyecto

Este es un proyecto académico independiente del Reto React UPB. Pertenece a otra asignatura de UNIMINUTO cuyo taller pide construir la **misma interfaz mínima en dos stacks distintos** y elaborar un informe técnico comparativo.

- **Stack A (ya construido):** App React e-commerce — `https://grajales-camilo.github.io/reto_fullstack_basico/`
- **Stack B (este proyecto):** App de escritorio con Python + Tkinter

El objetivo de este proyecto es construir el Stack B: una pantalla de búsqueda con lista de resultados y detalle de producto, conectada al mismo Firebase del Stack A, para medir métricas comparables entre ambos entornos.

---

## 2. Entorno local

- **SO:** Windows 11
- **Python:** 3.13 (ya instalado)
- **IDE:** VS Code con extensión Python de Microsoft (ms-python.python)
- **Empaquetado final:** PyInstaller → genera `.exe` autónomo para Windows

---

## 3. Stack y dependencias

### Dependencias Python (instalar con pip)

```
requests    ← REST API de Firestore + descarga de imágenes desde Storage
Pillow      ← mostrar imágenes JPEG/PNG en Tkinter
PyInstaller ← empaquetar como .exe (solo para entrega final)
```

Tkinter viene incluido con Python 3.13. No requiere instalación.

### Lo que NO se usa

- `firebase-admin` — no se necesita. Las reglas de Firestore son abiertas hasta mayo 2026. Se usan requests HTTP directos a la REST API pública.
- Threading — se omite intencionalmente. El congelamiento de la ventana durante descarga de imágenes se mide como métrica y se documenta como limitación técnica.

---

## 4. Conexión a Firebase

### Firestore — REST API sin credenciales

```
GET https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/products
```

Reemplazar `{PROJECT_ID}` con el ID del proyecto Firebase del Stack A. Devuelve JSON con los 10 productos de la colección `products`. No requiere token mientras las reglas sean abiertas.

### Firebase Storage — descarga directa

Las imágenes están almacenadas en Firebase Storage bajo `products/{productId}/{fileName}`. La URL pública de cada imagen está en el campo `imageUrl` de cada documento de Firestore. Se descarga con `requests.get(url)` y se muestra con Pillow.

---

## 5. Layout de la ventana

```
┌─────────────────────────────────────────────┐
│  🔍 [campo de texto        ] [Buscar]        │  ← Frame superior
├─────────────────────────────┬───────────────┤
│                             │               │
│  Listado de productos       │    Detalle    │
│  ─────────────────          │    ───────    │
│  > Producto 1               │  [imagen]     │
│    Producto 2               │               │
│    Producto 3               │  Nombre       │
│    Producto 4               │  Precio USD   │
│    ...                      │  Precio COP   │
│                             │               │
└─────────────────────────────┴───────────────┘
```

### Widgets Tkinter utilizados

| Widget | Rol |
|---|---|
| `Entry` | Campo de texto para búsqueda |
| `Button` | Ejecutar búsqueda |
| `Listbox` | Lista de resultados filtrados |
| `Label` | Imagen del producto en detalle |
| `Label` | Nombre, precio USD y precio COP |
| `Frame` | Contenedor del panel izquierdo y derecho |

---

## 6. Flujo de datos

```
Arranque
   │
   ▼
Request GET a Firestore REST API ──→ [M2: tiempo medido con time.perf_counter()]
   │
   ▼
Carga lista completa de productos en memoria (lista Python)
   │
   ├── Usuario escribe término + presiona [Buscar]
   │        │
   │        ▼
   │   Filtrado local sobre lista en memoria ──→ [M4: tiempo medido]
   │        │
   │        ▼
   │   Actualiza Listbox con resultados filtrados
   │
   └── Usuario selecciona producto en Listbox
            │
            ▼
       Request GET a URL de Firebase Storage ──→ [M3: tiempo medido]
       (ventana se congela durante descarga — comportamiento esperado y documentado)
            │
            ▼
       Muestra imagen con Pillow + nombre + precios en panel derecho
```

---

## 7. Orden de construcción (commits atómicos)

| Paso | Qué construir | Mensaje de commit sugerido |
|---|---|---|
| 1 | Ventana base con tres frames vacíos (búsqueda, lista, detalle) | `feat: estructura base ventana Tkinter` |
| 2 | Campo de texto Entry + botón Buscar funcionales (sin datos) | `feat: agrega campo búsqueda y botón` |
| 3 | Request a Firestore REST API y carga de productos en memoria | `feat: conecta Firestore REST API y carga productos` |
| 4 | Listbox poblado con nombres de productos cargados | `feat: renderiza lista de productos en Listbox` |
| 5 | Filtrado local al presionar Buscar — actualiza Listbox | `feat: implementa filtrado local de búsqueda` |
| 6 | Panel detalle muestra nombre y precios al seleccionar item | `feat: muestra detalle textual del producto seleccionado` |
| 7 | Descarga imagen desde Firebase Storage y la muestra con Pillow | `feat: carga imagen del producto desde Firebase Storage` |
| 8 | Instrumentación de métricas con time.perf_counter() en M2, M3, M4 | `chore: agrega medición de tiempos para métricas comparativas` |

**Reglas de commits:**
- Conventional Commits en español
- Un commit por paso atómico
- Sin `git push --force` jamás
- Push manual al final, no automático

---

## 8. Métricas a medir (Fase 3 del taller)

### M1 — Tiempo de arranque
- **Tkinter:** desde ejecutar el script hasta que la ventana responde (cronómetro manual)
- **React:** desde abrir la URL hasta que la galería es interactiva (cronómetro + DevTools DOMContentLoaded)

### M2 — Tiempo de carga inicial de productos desde Firestore
- **Tkinter:** `time.perf_counter()` antes y después del `requests.get()` a la REST API
- **React:** Network tab de Chrome → filtrar `firestore.googleapis.com` → columna Time

### M3 — Tiempo de carga de imagen desde Firebase Storage
- **Tkinter:** `time.perf_counter()` antes y después del `requests.get(imageUrl)`
- **React:** Network tab → filtrar `firebasestorage.googleapis.com` → columna Time
- Medir las mismas 3 URLs en ambos entornos y promediar

### M4 — Tiempo de respuesta de búsqueda
- **Tkinter:** `time.perf_counter()` antes y después del filtrado local al presionar botón
- **React:** búsqueda en tiempo real — verificar en Network tab si hay requests nuevos (si no los hay, es filtrado local)

### M5 — Errores detectados
- **Tkinter:** consola/terminal durante uso normal
- **React:** consola del navegador durante uso normal
- Registro cualitativo: tipo de error, frecuencia, si bloquea o es silencioso

### M6 — Accesibilidad básica
- **Tkinter:** navegación con Tab entre widgets, accesibilidad nativa de Windows
- **React:** navegación con Tab, contraste (Lighthouse en DevTools), ARIA roles en HTML

---

## 9. Limitaciones documentadas (para el informe)

- **Congelamiento de ventana en Tkinter:** la descarga de imágenes bloquea el hilo principal. La solución correcta es threading, omitida intencionalmente para reducir complejidad. El tiempo de congelamiento se mide como parte de M3 y se menciona como trade-off en el informe.
- **Tamaño del .exe:** PyInstaller genera un ejecutable de ~30–80 MB porque incluye el intérprete Python. Es autónomo pero pesado.
- **Reglas de Firebase abiertas:** válidas hasta mayo 2026. Después de esa fecha se requiere autenticación para leer Firestore y Storage desde Python.

---

## 10. Reglas operativas para el agente

- No tocar el proyecto React ni su repositorio — son proyectos independientes
- No hardcodear el PROJECT_ID de Firebase — leerlo desde una variable o constante al inicio del archivo
- No instalar dependencias sin confirmar nombre, versión y razón
- Flagear incertidumbre antes de ejecutar cualquier acción destructiva
- Idioma de respuestas: siempre español
- Este proyecto NO se despliega en GitHub Pages — el entregable es el `.py` funcional y el `.exe` empaquetado

---

## 11. Primera acción al iniciar sesión con este archivo

1. Leer este archivo completo
2. Verificar que `pip install requests Pillow` funciona en el entorno
3. Verificar que la URL de Firestore REST API responde con los productos (hacer un `requests.get()` de prueba)
4. Reportar estado antes de tocar cualquier archivo
5. Esperar instrucción explícita para arrancar el paso 1
