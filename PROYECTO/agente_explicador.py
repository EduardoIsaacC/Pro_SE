import os
from google import genai
from dotenv import load_dotenv

# 1. Ruta absoluta de la llave
ruta_absoluta = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(ruta_absoluta)

# 2. Conexión usando el SDK moderno
api_key = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=api_key)

def generar_explicacion(datos_del_pedido):
    """
    Agente 3: Toma los datos matemáticos del motor de inferencia 
    y redacta una explicación clara y amable para el cliente.
    """
    instrucciones = f"""
    Eres el Agente 3 de servicio al cliente de "Aderezos Edu". 
    Tu objetivo es explicarle al cliente de forma amable, clara y transparente el resultado de su pedido, justificando las decisiones del sistema experto.
    
    Aquí están los datos matemáticos y lógicos del pedido procesado por el Motor de Inferencia:
    {datos_del_pedido}
    
    Redacta un mensaje para el cliente que incluya:
    1. Un saludo amable.
    2. El resumen de lo que se le va a vender (cantidades, sabores y tamaños).
    3. El total a pagar final.
    4. EXPLICABILIDAD: Si se aplicó un descuento, explícale por qué se aplicó. Si se modificó su pedido porque no había stock suficiente, explícale el motivo y ofrécele una disculpa.
    
    REGLA: NO menciones las alertas internas de reabastecimiento, esa información es confidencial para el dueño.
    """

    try:
        respuesta = cliente.models.generate_content(
            model='gemini-1.5-flash-8b',  # <--- Agrega el "-8b" al final
            contents=instrucciones
        )
        return respuesta.text
    except Exception as e:
        return f"Error al generar la explicación: {e}"

# PRUEBA LOCAL
if __name__ == "__main__":
    reporte_simulado = {
        'estado': 'Aprobado', 
        'productos': [
            {'sabor': 'Habanero', 'tamano': '7oz', 'cantidad': 4, 'precio_unitario': 25.0}, 
            {'sabor': 'Chipotle', 'tamano': '725g', 'cantidad': 1, 'precio_unitario': 90.0}
        ], 
        'subtotal': 190.0, 
        'descuento': 19.0, 
        'total': 171.0, 
        'alertas': ['Inferencia comercial: Se aplicó un 10% de descuento por llevar 5 o más artículos.']
    }
    
    print("El Agente 3 está redactando la explicación...\n")
    explicacion_final = generar_explicacion(reporte_simulado)
    
    print(" RESPUESTA FINAL PARA EL CLIENTE ")
    print(explicacion_final)