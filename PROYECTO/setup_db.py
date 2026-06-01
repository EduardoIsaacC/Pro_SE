import sqlite3

def incializar_base_datos():
    conexion = sqlite3.connect('aderezos_edu.db')
    cursor = conexion.cursor()

    #Eliminacion de tavla anterior (en caso de haber futuras modificaciones)
    cursor.execute("DROP TABLE IF EXISTS productos")
    cursor.execute("DROP TABLE IF EXISTS pedidos")

    #Creamos la nueva tabla con columnas para sabor y tamaño
    cursor.execute('''
        CREATE TABLE productos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               sabor TEXT NOT NULL,
               tamano TEXT NOT NULL,
               precio REAL NOT NULL,
               stock INTEGER NOT NULL,
               UNIQUE(sabor, tamano)
            )               
    ''')

    #Insertamos las 6 variantes de Aderezos Edu con sus precios especificados
    inventario_inicial = [
        ('Chipotle', '725g', 90.00, 20),
        ('Chipotle', '7oz', 25.00, 50),
        ('Chipotle', '10oz', 40.00, 40),
        ('Habanero', '725g', 90.00, 15),
        ('Habanero', '7oz', 25.00, 45),
        ('Habanero', '10oz', 40.00, 35),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO productos (sabor, tamano, precio, stock)
        VALUES (?, ?, ?, ?)
    ''', inventario_inicial)

    #Recreamos la tabla de pedidos
    cursor.execute('''
        CREATE TABLE pedidos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            total REAL NOT NULL,
            estado TEXT DEFAULT 'Pendiente'
                   
            )
    ''')

    conexion.commit()
    conexion.close()
    print("¡Base de datos actualizada con exito con los nuevos tamaños y precios!")

if __name__ == "__main__":
    incializar_base_datos()
