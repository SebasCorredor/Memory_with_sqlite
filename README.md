# LangGraph Weather Agent

Este proyecto implementa un agente conversacional simple utilizando LangGraph y Vertex AI que puede responder preguntas sobre el clima en ciudades específicas (actualmente New York y San Francisco).

## Descripción

El proyecto utiliza:
- **LangGraph**: Framework para construir aplicaciones con flujos de trabajo basados en grafos para sistemas de IA
- **Vertex AI (Gemini)**: Modelo de lenguaje de Google utilizado como base del agente
- **SQLite**: Para persistencia de estado y checkpoints

El agente está diseñado con una arquitectura ReAct (Reasoning and Acting) que le permite razonar sobre consultas del usuario y utilizar herramientas externas para obtener información del clima.

## Estructura del Proyecto

```
.
├── README.md
├── main.py             # Definición del grafo y lógica principal
├── tools.py            # Herramientas disponibles para el agente
├── langgraph.json      # Configuración de LangGraph
├── requirements.txt    # Dependencias del proyecto
└── checkpoint.db       # Base de datos SQLite para checkpoints (se genera automáticamente)
```

## Requisitos

- Python 3.11
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-directorio>
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tus credenciales de Google Cloud (necesario para Vertex AI):
   ```bash
   # Configura las variables de entorno necesarias
   export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/tu/archivo-credenciales.json"
   ```

### Ejemplos de consultas

- "¿Cuál es el clima en Nueva York?"
- "¿Cómo está el tiempo en San Francisco?"

## Nota importante sobre debugging

**⚠️ Advertencia**: El uso del sistema de memoria (SQLite checkpoint) es incompatible con el entorno de depuración de LangGraph. 

Si necesitas depurar el proyecto:

1. Comenta temporalmente la configuración del checkpointer en `main.py`:
   ```python
   # Cambiar esta línea:
   graph = builder.compile(checkpointer=memory)
   
   # Por esta durante la depuración:
   graph = builder.compile()
   ```

2. Una vez finalizada la depuración, restaura la configuración original para mantener la persistencia.

## Herramientas disponibles

Actualmente, el agente cuenta con las siguientes herramientas:

- `get_weather`: Proporciona información del clima para NYC y SF (datos simulados)

## Ampliación

Para añadir soporte para más ciudades:
1. Modifica la función `get_weather` en `tools.py` para incluir más ciudades
2. Actualiza el tipo `Literal` en la anotación de tipo para incluir las nuevas ciudades
