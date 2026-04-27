import tkinter as tk
import requests
import time

PROJECT_ID = "reto-fullstack-upb-af0d2"
FIRESTORE_URL = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
    "/databases/(default)/documents/products"
)


def cargar_productos():
    t0 = time.perf_counter()
    respuesta = requests.get(FIRESTORE_URL)
    t1 = time.perf_counter()
    print(f"[M2] Tiempo carga Firestore: {t1 - t0:.3f}s")
    respuesta.raise_for_status()
    documentos = respuesta.json().get("documents", [])
    lista = []
    for doc in documentos:
        fields = doc.get("fields", {})
        lista.append({
            "id": doc["name"].split("/")[-1],
            "nombre": fields.get("name", {}).get("stringValue", ""),
            "precio_usd": fields.get("price", {}).get("doubleValue")
                          or fields.get("price", {}).get("integerValue", 0),
            "precio_cop": fields.get("priceCOP", {}).get("doubleValue")
                          or fields.get("priceCOP", {}).get("integerValue", 0),
            "imagen_url": fields.get("imageUrl", {}).get("stringValue", ""),
        })
    print(f"[INFO] Productos cargados: {len(lista)}")
    return lista


productos = cargar_productos()

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
    listbox.delete(0, tk.END)
    for p in lista:
        listbox.insert(tk.END, p["nombre"])


def on_buscar():
    termino = entry_busqueda.get().strip().lower()
    t0 = time.perf_counter()
    if termino:
        filtrados = [p for p in productos if termino in p["nombre"].lower()]
    else:
        filtrados = productos
    t1 = time.perf_counter()
    print(f"[M4] Tiempo filtrado: {t1 - t0:.6f}s — {len(filtrados)} resultado(s)")
    poblar_listbox(filtrados)

# Widgets de búsqueda
tk.Label(frame_busqueda, text="🔍").pack(side=tk.LEFT)
entry_busqueda = tk.Entry(frame_busqueda, width=40)
entry_busqueda.pack(side=tk.LEFT, padx=(4, 8))
tk.Button(frame_busqueda, text="Buscar", command=on_buscar).pack(side=tk.LEFT)

# Listbox con scrollbar vertical
scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL)
listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, activestyle="arrow")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

poblar_listbox(productos)

# Etiqueta temporal del panel derecho
tk.Label(frame_detalle, text="[Detalle]", fg="gray").pack(expand=True)

root.mainloop()
