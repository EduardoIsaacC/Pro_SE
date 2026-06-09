import discord 
import os
import asyncio
from dotenv import load_dotenv

#Importamos a los 3 agentes
from agente_nlp import procesar_texto_cliente
from motor_inferencia import evaluar_pedido
from agente_explicador import generar_explicacion

#Cargamos llaves secretas
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
# Esto nos dirá en la terminal si la llave se cargó o no
if DISCORD_TOKEN is None:
    print(" ERROR: No se encontró la llave 'DISCORD_TOKEN' en el archivo .env")
    print("Asegúrate de que el archivo .env existe y está guardado.")
    exit() # Detiene el programa antes de que explote con el error largo
else:
    print(" Llave de Discord detectada correctamente.")

class ClienteDiscord(discord.Client):
    async def on_ready(self):
        print("SISTEMA EXPERTO ADEREZOS EDU EN LINEA EN DISCORD")
        print(f"Conectado como: {self.user}")

    async def on_message(self, message):
        #Evitar que el bot se responda a si mismo
        if message.author == self.user:
            return

        #Si el usuario menciona "aderezo", "hola", o "quiero", el bot despierta
        texto = message.content.lower()
        if 'hola' in texto or 'aderezo' in texto or 'quiero' in texto:

            #Interfaz de espera (solucion al semaforo de Google)
            mensaje_espera = await message.channel.send(" *PROCESANDO TU PEDIDO CON INTELIGENCIA ARTIFICIAL, DAME UNOS SEGUNDOS....*")
            await asyncio.sleep(3) #Primera pausa

            try:

                #AGENTE 1: NLP
                pedido_estructurado = procesar_texto_cliente(message.content)

                if not pedido_estructurado:
                    await mensaje_espera.edit(content=" ** Error:** No pude identificar los sabores o tamaños. Por favor intenta especificando mejor (ej. Chipotle 725g o Habanero 7oz).")
                    return

                #Agente 2: Motor de Inferencia (SQLITE)
                reporte_sistema = evaluar_pedido(pedido_estructurado)

                await mensaje_espera.edit(content=" *Consultando inventario y aplicando reglas de negocio...*")
                await asyncio.sleep(5) #Segunda pausa tactica para dejar respirar a la API

                #Agente 3: Explicador
                respuesta_final = generar_explicacion(reporte_sistema)

                #SALIDA FINAL EN DISCORD
                await message.channel.send(f"** TICKET DEL SISTEMA EXPERTO:**\n\n{respuesta_final}")
                await mensaje_espera.delete() # Borramos el mensaje de "Cargando" para que se vea limpio

            except Exception as e:
                # Si por alguna razón Google nos bloquea, no se cae el programa, avisa en el chat
                await message.channel.send(f" **Aviso de Sistema:** El servidor de IA detectó tráfico inusual. Por favor, espera 1 minuto y vuelve a escribir tu pedido.")
                print(f"Error interno: {e}")

#Configuramos los permisos para leer los mensajes
intents = discord.Intents.default()
intents.message_content = True

#Encendemos el bot
cliente = ClienteDiscord(intents=intents)
cliente.run(DISCORD_TOKEN)