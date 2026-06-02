import sqlite3
import os

#Forzar la creacion de la Base de Datos en el lugar
ruta_bd = os.path.join(os.path.dirname(__file__), 'aderezos_edu.db')

conexion = sqlite3.connect(ruta_bd)
cursor = conexion.cursor()

#Creamos tabla de productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sabor TEXT NOT NULL,
        tamano TEXT NOT NULL,
        stock INTEGER NOT NULL,
        precio REAL NOT NULL
    )
''')

#Limpiar en caso de datos basura
cursor.execute('DELETE FROM productos')

#Insertamos el catalogo
catalogo = [
    ('Habanero', '7oz', 15, 25.0),
    ('Habanero', '10oz', 10, 45.0),
    ('Habanero', '725g', 4, 90.0),
    ('Chipotle', '7oz', 20, 25.0),
    ('Chipotle', '10oz', 12, 45.0),
    ('Chipotle', '725g', 8, 90.0)
]

cursor.executemany('''
    INSERT INTO productos (sabor, tamano, stock, precio)
    VALUES (?, ?, ?, ?)
''', catalogo)

conexion.commit()
conexion.close()

print(f"¡ÉXITO! Base de datos creada en: {ruta_bd}")
print("Catálogo de Aderezos Edu guardado correctamente.")