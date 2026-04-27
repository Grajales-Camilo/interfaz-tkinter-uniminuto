import tkinter as tk
import requests
import time
from io import BytesIO
from PIL import Image, ImageTk

PROJECT_ID = "reto-fullstack-upb-af0d2"
FIRESTORE_URL = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
    "/databases/(default)/documents/products"
)
EXCHANGE_RATE_URL = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
    "/databases/(default)/documents/settings/exchange_rate"
)


def parse_numero(field):
    if "doubleValue" in field:
        return float(field["doubleValue"])
    if "integerValue" in field:
        return int(field["integerValue"])
    return 0


def cargar_tasa_cambio():
    try:
        respuesta = requests.get(EXCHANGE_RATE_URL, timeout=10)
        respuesta.raise_for_status()
        fields = respuesta.json().get("fields", {})
        tasa = parse_numero(fields.get("usdToCop", {}))
        print(f"[INFO] Tasa USD→COP: {tasa}")
        return tasa
    except Exception as e:
        print(f"[WARN] No se pudo obtener tasa de cambio: {e}")
        return 0


def cargar_productos():
    global tiempo_m2
    t0 = time.perf_counter()
    respuesta = requests.get(FIRESTORE_URL)
    t1 = time.perf_counter()
    tiempo_m2 = t1 - t0
    print(f"[M2] Tiempo carga Firestore: {tiempo_m2:.3f}s")
    respuesta.raise_for_status()
    documentos = respuesta.json().get("documents", [])
    lista = []
    for doc in documentos:
        fields = doc.get("fields", {})
        precio_usd = parse_numero(fields.get("price", {}))
        lista.append({
            "id": doc["name"].split("/")[-1],
            "nombre": fields.get("name", {}).get("stringValue", ""),
            "precio_usd": precio_usd,
            "precio_cop": round(precio_usd * tasa_usd_cop),
            "imagen_url": fields.get("imageUrl", {}).get("stringValue", ""),
        })
    print(f"[INFO] Productos cargados: {len(lista)}")
    return lista


# Acumuladores de métricas
tiempo_m2 = 0.0
tiempos_m3 = []
tiempos_m4 = []

tasa_usd_cop = cargar_tasa_cambio()
productos = cargar_productos()
productos_visibles = list(productos)  # subconjunto actualmente en el Listbox

root = tk.Tk()
root.title("Tienda — Tkinter")
root.geometry("800x520")
root.resizable(False, False)

# Frame superior: búsqueda
frame_busqueda = tk.Frame(root, bd=1, relief=tk.SOLID, pady=6, padx=8)
frame_busqueda.pack(fill=tk.X, padx=10, pady=(10, 0))

# Frame central: divide lista y detalle
frame_central = tk.Frame(root)
frame_central.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame izquierdo: listado de productos
frame_lista = tk.Frame(frame_central, bd=1, relief=tk.SOLID)
frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame derecho: detalle del producto
frame_detalle = tk.Frame(frame_central, bd=1, relief=tk.SOLID, width=260)
frame_detalle.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
frame_detalle.pack_propagate(False)

def poblar_listbox(lista):
    global productos_visibles
    productos_visibles = list(lista)
    listbox.delete(0, tk.END)
    for p in productos_visibles:
        listbox.insert(tk.END, p["nombre"])


def on_buscar():
    termino = entry_busqueda.get().strip().lower()
    t0 = time.perf_counter()
    filtrados = [p for p in productos if termino in p["nombre"].lower()] if termino else productos
    t1 = time.perf_counter()
    duracion_m4 = t1 - t0
    tiempos_m4.append(duracion_m4)
    print(f"[M4] Tiempo filtrado: {duracion_m4:.6f}s — {len(filtrados)} resultado(s)")
    poblar_listbox(filtrados)


def descargar_imagen(url):
    t0 = time.perf_counter()
    respuesta = requests.get(url, timeout=10)
    t1 = time.perf_counter()
    duracion_m3 = t1 - t0
    tiempos_m3.append(duracion_m3)
    print(f"[M3] Tiempo descarga imagen: {duracion_m3:.3f}s")
    respuesta.raise_for_status()
    img = Image.open(BytesIO(respuesta.content))
    img.thumbnail((200, 200))
    return ImageTk.PhotoImage(img)


def on_seleccionar(event):
    seleccion = listbox.curselection()
    if not seleccion:
        return
    producto = productos_visibles[seleccion[0]]

    # Imagen
    url = producto.get("imagen_url", "")
    if url:
        try:
            foto = descargar_imagen(url)
            lbl_imagen.config(image=foto, text="")
            lbl_imagen.image = foto  # evita que el GC elimine la referencia
        except Exception as e:
            print(f"[WARN] No se pudo cargar imagen: {e}")
            lbl_imagen.config(image="", text="Sin imagen")
            lbl_imagen.image = None
    else:
        lbl_imagen.config(image="", text="Sin imagen")
        lbl_imagen.image = None

    lbl_nombre.config(text=producto["nombre"])
    lbl_precio_usd.config(text=f"USD  ${float(producto['precio_usd']):.2f}")
    lbl_precio_cop.config(text=f"COP  ${int(producto['precio_cop']):,}".replace(",", "."))

# Widgets de búsqueda
tk.Label(frame_busqueda, text="🔍").pack(side=tk.LEFT)
entry_busqueda = tk.Entry(frame_busqueda, width=40)
entry_busqueda.pack(side=tk.LEFT, padx=(4, 8))
tk.Button(frame_busqueda, text="Buscar", command=on_buscar).pack(side=tk.LEFT)

# Listbox con scrollbar vertical
scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL)
listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, activestyle="dotbox")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

poblar_listbox(productos)
listbox.bind("<<ListboxSelect>>", on_seleccionar)

# Panel detalle: imagen, nombre y precios
tk.Label(frame_detalle, text="Detalle del producto", font=("Arial", 10, "bold"),
         pady=8).pack()
lbl_imagen = tk.Label(frame_detalle, text="Sin imagen", fg="gray")
lbl_imagen.pack(pady=(0, 8))
lbl_nombre = tk.Label(frame_detalle, text="", wraplength=240, justify=tk.LEFT,
                      font=("Arial", 10))
lbl_nombre.pack(padx=10, pady=(4, 12))
lbl_precio_usd = tk.Label(frame_detalle, text="", font=("Arial", 10))
lbl_precio_usd.pack(padx=10, anchor=tk.W)
lbl_precio_cop = tk.Label(frame_detalle, text="", font=("Arial", 10))
lbl_precio_cop.pack(padx=10, anchor=tk.W)

def on_closing():
    prom_m3 = sum(tiempos_m3) / len(tiempos_m3) if tiempos_m3 else 0.0
    prom_m4 = sum(tiempos_m4) / len(tiempos_m4) if tiempos_m4 else 0.0
    print("\n─── Resumen de métricas de la sesión ───")
    print(f"  M2  Carga inicial Firestore : {tiempo_m2:.3f}s")
    print(f"  M3  Descarga imagen (prom.) : {prom_m3:.3f}s  (n={len(tiempos_m3)})")
    print(f"  M4  Filtrado búsqueda (prom): {prom_m4:.6f}s  (n={len(tiempos_m4)})")
    print("────────────────────────────────────────\n")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
