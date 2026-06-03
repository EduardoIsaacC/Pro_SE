import time
from agente_nlp import  procesar_texto_cliente
from motor_inferencia import evaluar_pedido
from agente_explicador import generar_explicacion

def ejecutar_sistema_experto():
    """
    Funcion principal que orquesta la comunicacion entre los 3 agentes.
    """
    print( " SISTEMA EXPERTO DE ADEREZOS EDU INICIADO ")

    #Simulamos la entrada del usuario por consola
    mensaje_cliente = input(" Cliente ")
    print("\n Procesando pedido...... \n")

    #Agente NLP (Traduccion de Lenguaje Natural a JSON)
    print(" [Agente 1] Analizando texto..... ")
    pedido_estructurado = procesar_texto_cliente(mensaje_cliente)

    #Validacion por si el cliente escribe algo no tiene sentido
    if not pedido_estructurado:
        print("\n  Error: El sistema no pudo identificar los sabores o tamaños en tu mensaje.")
        print(" Por favor intenta de nuevo especificando (ej. Chipotle 725g o Habanero 7oz.)")
        return
    
    print(f"Datos extraídos con éxito: {pedido_estructurado}\n")
    time.sleep(1) #Pausa para que se visualice el proceso

    #MOTOR DE INFERENCIA (Base de datos y Matematicas)
    print(" [Agente 2] Consultando inventario y aplicando reglas de negocio....")
    reporte_sistema = evaluar_pedido(pedido_estructurado)

    print(f" Calculo finalizado. Estado del ticket: {reporte_sistema['estado']}\n")
    time.sleep(1)

    #AGENTE EXPLICADOR (Redaccion justificada)
    print(" [Agente 3] Redactando la explicacion transparante para el cliente.....")
    respuesta_final = generar_explicacion(reporte_sistema)

    #SALIDA FINAL
    print("\n" + "="*50)
    print(" RESPUESTA FINAL DEL ASISTENTE VIRTUAL")
    print("="*50)
    print(respuesta_final)
    print("="*50 + "\n")

    #BUCLE DE EJECUCION
if __name__ == "__main__":
    while True:
        ejecutar_sistema_experto()

        #Pregnutar si el usuario desea realizar otra prueba
        continuar = input("¿Desea procesar otro pedido? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nApagando Sistema Experto..... ¡HASTA PRONTO!")
            break