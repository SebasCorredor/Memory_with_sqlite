
from langchain_google_vertexai import ChatVertexAI
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from tools import get_weather
from typing import Literal


#Crear la conexion a la base de datos SQLite
conn = sqlite3.connect(
                       'checkpoint.db', 
                       check_same_thread=False
                       )
cursor = conn.cursor()

#Configuramos para que el checkpoint se guarde en la base de datos SQLite
memory = SqliteSaver(conn)


#Herramienta de recuperacion de datos
tools = [
        get_weather
        ]

#Definimos el modelo de lenguaje a utilizar
llm = ChatVertexAI(
                   model="gemini-2.0-flash",
                   temperature=0,
                   )


#Definimos el estado inicial
class State(MessagesState):
    next: str

#Creamos el agente
agent = create_react_agent(
    llm, tools=tools, prompt=f'''
    You are a helpful assistant that can answer questions about the weather.
    '''
)

#Funcion de operacion del agente
def weather_function(state: State) -> Command[Literal["__end__"]]:
    
    result = agent.invoke(state)
    return Command(
    update={
            "messages": AIMessage(    
        content=result["messages"][-1].content, name="agent"
    )
        },
        goto=END,
    )


#Compilamos el grafo
builder = StateGraph(State)
builder.add_edge(START, "agent")
builder.add_node("agent", weather_function)
builder.add_edge("agent", END)
graph = builder.compile(checkpointer=memory) 