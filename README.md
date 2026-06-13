# Sistema Experto Multi-Agente: Aderezos Edu 

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Discord](https://img.shields.io/badge/Discord.py-2.3+-7289DA.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)

## Descripción del Proyecto
Este proyecto implementa un **Sistema Experto moderno** basado en Inteligencia Artificial Generativa y un Motor de Inferencia clásico para la automatización de ventas y atención al cliente. El sistema opera a través de una arquitectura cliente-servidor utilizando Discord como interfaz de usuario para el negocio "Aderezos Edu".

A diferencia de los bots tradicionales de opciones rígidas, este sistema comprende el lenguaje humano coloquial y aplica reglas matemáticas exactas para la gestión de inventario y cobros.

## Arquitectura del Sistema
El núcleo del proyecto funciona mediante la orquestación de 3 agentes inteligentes:

1. **Agente NLP (Extractor Cognitivo):** Utiliza Google Gemini 2.5 Flash para procesar lenguaje natural, interpretar intenciones y traducir lenguaje coloquial (ej. "chicos", "grandote") a entidades estructuradas matemáticas (JSON).
2. **Motor de Inferencia (Lógica de Negocio):** Evalúa el diccionario de datos contra reglas lógicas. Interactúa de forma invisible con una base de datos SQLite para validar existencias, restar inventario en tiempo real y aplicar promociones por volumen.
3. **Agente Explicador (Servicio al Cliente):** Traduce el dictamen lógico del motor de inferencia a lenguaje natural, justificando las decisiones del sistema de forma transparente, empática y detallada para el usuario final.

## Tolerancia a Fallos y Degradación Elegante
El sistema está diseñado para entornos de producción reales. Cuenta con:
* **Lógica de Reintentos (Retry Logic):** Ciclos automatizados que protegen al bot de colapsar ante errores HTTP `503 UNAVAILABLE` o picos de tráfico en la API de Google.
* **Sistema de Respaldo Local (Plan B):** Si el proveedor en la nube falla por completo, el sistema cuenta con degradación elegante para emitir el ticket de compra directamente desde el motor local, garantizando que nunca se pierda una venta.

## Estructura del Repositorio
* `bot_discord.py` - Orquestador principal y conexión con la API de Discord.
* `agente_nlp.py` - Procesamiento de lenguaje natural y base de conocimiento.
* `motor_inferencia.py` - Evaluación matemática y conexión transaccional.
* `agente_explicador.py` - Generación de explicabilidad y respuesta final.
* `inventario.db` - Base de datos relacional local (SQLite).
* `.env.example` - Plantilla de variables de entorno requeridas.

## Guía de Instalación y Despliegue

### 1. Preparación del Entorno
Clona este repositorio y abre una terminal en la carpeta raíz. Crea y activa un entorno virtual:
```bash
python -m venv .venv
# En Windows:
.\.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate

#### 2. Instalación de Dependencias
pip install discord.py google-genai python-dotenv

#####3. Configuración de Credenciales
GEMINI_API_KEY=tu_llave_de_google_ai_studio_aqui
DISCORD_TOKEN=tu_llave_del_bot_de_discord_aqui

##### 4. Inicialización
python bot_discord.py