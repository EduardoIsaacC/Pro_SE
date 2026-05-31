import sqlite3

def evaluar_pedido(articulos_solicitados):
    """
    Recibe una lista de diccionarios con lo que el cliente pidio
    """

    #Conexion a la Base de datos
    conexion = sqlite3.connect('aderezos_edu.db')
    cursor = conexion.cursor()

    estado_pedido = "Aprobado"
    alertas = []
    subtotal = 0
    cantidad_total_botellas = 0
    items_procesados = []

    #Procesar cada articulo solicitado por el cliente
    for item in articulos_solicitados:
        sabor = item['sabor']
        tamano = item['tamano']
        cantidad_pedida = item['cantidad']

        #Consultar la BD usando el sabor y tamaño especificos
        cursor.execute(
            "SELECT id, stock, precio FROM productos WHERE sabor = ? AND tamano = ?",
            (sabor, tamano)
        )
        resultado = cursor.fetchone()

        if resultado:
            id_prod, stock_actual, precio = resultado
            cantidad_final = cantidad_pedida

            #Validacion de stock
            if cantidad_pedida > stock_actual:
                estado_pedido = "Modificado"
                alertas.append(
                    f"Stock insuficiente de {sabor} ({tamano})."
                    f"Pedido: {cantidad_pedida}, Disponible: {stock_actual}."
                )
                cantidad_final = stock_actual
            
            #Alerta de Reabastecimiento Critico
            stock_restante = stock_actual - cantidad_final
            if stock_restante < 5:
                alertas.append(
                    f"ALERTA INTERNA: El stock de {sabor} ({tamano})"
                    f"quedara en {stock_restante} unidades. Requiere reabastecimiento urgente."
                )

            #Acumular valores para el calculo final
            subtotal += cantidad_final * precio
            cantidad_total_botellas += cantidad_final

            #Guardamos el estado de este item para el reporte
            items_procesados.append({
                "sabor": sabor,
                "tamano": tamano,
                "cantidad": cantidad_final,
                "precio_unitario": precio
            })
        else:
            alertas.append(f"Error: El producto {sabor} de {tamano} no existe en el catalogo")

    #Promocion por volumen
    descuento = 0
    if cantidad_total_botellas >= 5:
        descuento = subtotal * 0.10
        alertas.append("Inferencia comercial: Se aplico un 10% de descuento por llevar 5 unidades")

    total = subtotal - descuento
    conexion.close()

    return {
        "estado": estado_pedido,
        "productos": items_procesados,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
        "alertas": alertas
    }

#Prueba local

if __name__ == "__main__":
    #Simulamos un pedido mixto:
    # 1 bote de chipotle grande (725g) a $90
    # 4 botes de habanero chicos (7oz) 
    # Total de botellas: 5 (Aplica descuento del 10%)
    carrito_prueba = [
        {"sabor": "Chipotle", "tamano": "725g", "cantidad": 1},
        {"sabor": "Habanero", "tamano": "7oz", "cantidad": 4},
    ]

    resultado = evaluar_pedido(carrito_prueba)

    print("REPORTE GENERADO POR EL SISTEMA EXPERTO")
    print(f"Estado general: {resultado['estado']} MXN")
    print(f"Subtotal: ${resultado['subtotal']} MXN")
    print(f"Descuento: ${resultado['descuento']} MXN")
    print(f"Total Neto: ${resultado['total']} MXN")
    print("\n EXPLICABILIDAD Y RAZONAMIENTO")
    for alerta in resultado['alertas']:
        print(f"- {alerta}")
