import tkinter as tk

PROJECT_ID = "reto-fullstack-basico"

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

def on_buscar():
    print("Buscar presionado")

# Widgets de búsqueda
tk.Label(frame_busqueda, text="🔍").pack(side=tk.LEFT)
entry_busqueda = tk.Entry(frame_busqueda, width=40)
entry_busqueda.pack(side=tk.LEFT, padx=(4, 8))
tk.Button(frame_busqueda, text="Buscar", command=on_buscar).pack(side=tk.LEFT)

# Etiquetas temporales para identificar cada frame visualmente
tk.Label(frame_lista, text="[Lista de productos]", fg="gray").pack(expand=True)
tk.Label(frame_detalle, text="[Detalle]", fg="gray").pack(expand=True)

root.mainloop()
