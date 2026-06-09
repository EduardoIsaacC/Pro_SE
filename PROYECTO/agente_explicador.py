import os
import time
from google import genai
from dotenv import load_dotenv

# 1. Ruta absoluta de la llave
ruta_absoluta = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(ruta_absoluta)

# 2. Conexión usando el SDK moderno
api_key = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=api_key)

def generar_explicacion(datos_del_pedido):
    instrucciones = f"""
    Eres el Agente 3 de servicio al cliente de "Aderezos Edu". 
    Tu objetivo es explicarle al cliente de forma amable, clara y transparente el resultado de su pedido.
    
    Aquí están los datos matemáticos y lógicos del pedido:
    {datos_del_pedido}
    
    Redacta un mensaje para el cliente que incluya:
    1. Un saludo amable.
    2. El resumen de lo que se le va a vender (cantidades, sabores y tamaños).
    3. El total a pagar final.
    4. EXPLICABILIDAD: Si se aplicó un descuento o hubo falta de stock, explícale el motivo.
    
    REGLA: NO menciones las alertas internas de reabastecimiento.
    """

    intentos_maximos = 3
    
    for intento in range(intentos_maximos):
        try:
            # Llamada al modelo
            respuesta = cliente.models.generate_content(
                model='gemini-2.5-flash',
                contents=instrucciones
            )
            return respuesta.text
            
        except Exception as e:
            error_mensaje = str(e)
            if "503" in error_mensaje or "429" in error_mensaje:
                if intento < intentos_maximos - 1:
                    print(f" Servidor ocupado (Intento {intento + 1}/{intentos_maximos}). Esperando 3 segundos...")
                    time.sleep(3)
                    continue
            
    # PLAN B: DEGRADACIÓN ELEGANTE (SISTEMA DE RESPALDO LOCAL)
    # Si llegamos a esta línea, es porque Google se cayó por completo.
    # El sistema emite el ticket directamente para no perder la venta.
    print(" Google no respondió. Activando sistema de respaldo local...")
    
    ticket_respaldo = f"""
    **¡Hola! Gracias por tu preferencia en Aderezos Edu.** 
    *(Aviso: Nuestro Agente de Lenguaje se encuentra temporalmente saturado en la nube. Generando ticket mediante sistema de respaldo local).*
    
    **Resumen de la Operación en Base de Datos:**
    ```json
    {datos_del_pedido}
    ```
    
     *Tu pedido ha sido procesado y descontado del inventario exitosamente.*
    """
    return ticket_respaldo

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
    print(generar_explicacion(reporte_simulado))