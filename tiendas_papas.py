import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Tu contraseña aquí
    database="tienda_papas"
)

cursor = db.cursor(dictionary=True)

# Funciones para manejar la lógica


def verificar_usuario(usuario, contrasena):
    query = "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s"
    cursor.execute(query, (usuario, contrasena))
    return cursor.fetchone()


def obtener_productos():
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()


def agregar_al_carrito(usuario_id, producto_id, cantidad):
    query = "INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)"
    cursor.execute(query, (usuario_id, producto_id, cantidad))
    db.commit()
    messagebox.showinfo("Éxito", "Producto agregado al carrito")


def obtener_historial_carrito(usuario_id, meses=6):
    fecha_inicio = datetime.now() - timedelta(days=meses*30)
    query = """
        SELECT p.nombre, p.sabor, p.tamano, p.precio, c.cantidad, c.fecha
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s AND c.fecha >= %s
    """
    cursor.execute(query, (usuario_id, fecha_inicio))
    return cursor.fetchall()

# Interfaz gráfica


def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    usuario_data = verificar_usuario(usuario, contrasena)

    if usuario_data:
        ventana_inicio.destroy()
        mostrar_menu_principal(usuario_data)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def mostrar_menu_principal(usuario):
    def ver_productos():
        productos = obtener_productos()
        ventana_productos = tk.Toplevel()
        ventana_productos.title("Productos disponibles")

        for producto in productos:
            tk.Label(ventana_productos,
                     text=f"{producto['nombre']} - {producto['sabor']} - {producto['tamano']} - ${producto['precio']}").pack()

    def ver_carrito():
        carrito = obtener_historial_carrito(usuario['id'])
        ventana_carrito = tk.Toplevel()
        ventana_carrito.title("Historial del carrito")

        for item in carrito:
            tk.Label(
                ventana_carrito, text=f"{item['nombre']} ({item['sabor']} - {item['tamano']}): {item['cantidad']} unidades").pack()

    ventana_menu = tk.Tk()
    ventana_menu.title(f"Menú principal - {usuario['nombre']}")

    tk.Button(ventana_menu, text="Ver productos", command=ver_productos).pack()
    tk.Button(ventana_menu, text="Ver historial del carrito",
              command=ver_carrito).pack()


# Ventana inicial
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de sesión")

tk.Label(ventana_inicio, text="Usuario:").pack()
entry_usuario = tk.Entry(ventana_inicio)
entry_usuario.pack()

tk.Label(ventana_inicio, text="Contraseña:").pack()
entry_contrasena = tk.Entry(ventana_inicio, show="*")
entry_contrasena.pack()

tk.Button(ventana_inicio, text="Iniciar sesión", command=iniciar_sesion).pack()

ventana_inicio.mainloop()
