import os
import json
from google import genai
from dotenv import load_dotenv

# 1. Ruta absoluta de la llave
ruta_absoluta = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(ruta_absoluta)

# 2. Conexión usando el SDK moderno de Google
api_key = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=api_key)

def procesar_texto_cliente(mensaje_cliente):
    """
    Agente 1: Interpreta el lenguaje natural del cliente y extrae las entidades.
    """
    instrucciones = f"""
    Eres el Agente 1 de ventas del negocio "Aderezos Edu".
    Tu trabajo es leer el mensaje del cliente y extraer qué aderezos quiere comprar.
    
    Catálogo válido:
    Sabores: Chipotle, Habanero.
    Tamaños oficiales: 725g, 10oz, 7oz.
    
    Base de conocimiento para sinónimos:
    - Si el cliente dice "chico" o "pequeño", el tamaño es "7oz".
    - Si el cliente dice "mediano", el tamaño es "10oz".
    - Si el cliente dice "grande" o "grandote", el tamaño es "725g".
    
    Mensaje del cliente: "{mensaje_cliente}"
    
    REGLA ESTRICTA: Responde ÚNICAMENTE con un arreglo en formato JSON puro. No agregues texto antes ni después.
    El JSON debe tener esta estructura exacta para cada artículo:
    [
        {{"sabor": "Chipotle o Habanero", "tamano": "725g o 10oz o 7oz", "cantidad": numero_entero}}
    ]
    Si no entiendes el pedido, devuelve un arreglo vacío: []
    """

    try:
        # Llamada al modelo 
        respuesta = cliente.models.generate_content(
            model='gemini-2.0-flash'
            contents=instrucciones
        )
        
        # --- LIMPIEZA DE JSON A PRUEBA DE BALAS ---
        texto_limpio = respuesta.text.strip()
        # En lugar de rebanar, simplemente reemplazamos cualquier rastro de markdown por "nada"
        texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
        
        lista_articulos = json.loads(texto_limpio)
        return lista_articulos
        
    except Exception as e:
        print(f"Error al interpretar la respuesta de la IA: {e}")
        return []

# PRUEBA LOCAL
if __name__ == "__main__":
    texto_prueba = "Hola, me mandas porfa dos aderezos chicos de habanero y un chipotle grandote de 725g. Gracias."
    
    print(f"Mensaje original: {texto_prueba}\n")
    print("El Agente 1 está pensando...\n")
    
    resultado_agente = procesar_texto_cliente(texto_prueba)
    
    print("  DATO ESTRUCTURADO PARA EL MOTOR DE INFERENCIA  ")
    print(resultado_agente)