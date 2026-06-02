import time
from agente_nlp import  procesar_texto_cliente
from motor_inferencia import evaluar_pedido
from agente_explicador import generar_explicacion

def ejecutar_sistema_experto():
    """
    Funcion principal que orquesta la comunicacion entre los 3 agentes.
    """
    print("\n" + "="*50)
    print( " SISTEMA EXPERTO DE ADEREZOS EDU INICIADO ")
    print("="*50 + "\n")

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
    
    print(f"")