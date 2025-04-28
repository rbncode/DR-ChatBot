from fastapi import FastAPI, HTTPException
from serpapi.google_search import GoogleSearch
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Crear una instancia de FastAPI
app = FastAPI()

def consultar_gemini(pregunta):
    try:
        load_dotenv("key.env") 
        api_key = os.getenv("GEMMA_API_KEY")
        
        if not api_key:
            raise HTTPException(status_code=500, detail="Error: No se encontró la clave API de gemma.")
        
        # Configurar la API de Gemini
        genai.configure(api_key=api_key)
        
        # Seleccion del modelo
        modelo = genai.GenerativeModel('gemma-3-27b-it')
        
        # Enviar la consulta y obtener respuesta
        respuesta = modelo.generate_content(pregunta)
        
        return respuesta.text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar gemma: {str(e)}")

def busqueda_google_chatbot(pregunta):
    try:
        genai.configure(api_key=os.getenv("GEMMA_API_KEY"))
        model = genai.GenerativeModel('gemma-3-27b-it')
        
        params = {
            "q": pregunta,
            "api_key": os.getenv("SERPAPI_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()["organic_results"]

        # Obtener los primeros 3 resultados
        contexto = "\n".join(f"{r['title']}: {r['snippet']}" for r in results[:3])

        # Consulta con contexto
        respuesta = model.generate_content(f"Con base en esta información:\n{contexto}\n\n {pregunta}")

        return respuesta.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la búsqueda en Google: {str(e)}")

# endpoint
@app.post("/chatbot/")
async def chatbot_endpoint(pregunta_usuario: dict):
    try:
        # Cargar variables de entorno
        load_dotenv("key.env") 
    
        system_prompt = "En base a la pregunta del usuario se debe identificar una busqueda en google a realizar clave, que puede ser solo una de la siguiente lista " \
        "1) El clima del dia en la zona que se pregunta el dia de hoy(esta debe ser respondida con respecto a como se pregunte) si no se identifica la zona en la pregunta devolver: Lo siento, falta información para poder contestar a su consulta" \
        "2) El valor de la UF a CLP hoy se entiende uf o UF" \
        "3) Valor del dolar a CLP hoy y solo puede ser en estas monedas, si se pregunta de otra moneda no corresponde se entiende dolar o usd" \
        "4) Noticias del dia en la zona que se pregunta y si no se especifica entonces de manera global" \
        "Si el usuario pregunta algo fuera de esto devuelve un: Lo siento, no puedo ayudar con esa pregunta" \
        "Si puedes identificar la pregunta en una de las catergoria responde como si fueras a realizar una busqueda en google del tema poniendo lo que buscaras " \
        "entre 2 #." \
        "Si se identifica un saludo o despedida de parte del usuario responde como si fueras un asistente virtual y no como un buscador de google correspondiendo al saludo" \
        "La pregunta del usuario es : "

        # Obtener la pregunta del usuario desde el JSON enviado
        pregunta = pregunta_usuario.get("pregunta", "")
        if not pregunta:
            raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

        consulta = f"{system_prompt} {pregunta}"

        # Consultar Gemini AI
        respuesta_gemini = consultar_gemini(consulta)

        # Extraer la pregunta para la búsqueda en Google
        busqueda = re.findall(r"\#(.*?)\#", respuesta_gemini)
        if not busqueda:
            return respuesta_gemini
        # Realizar búsqueda en Google
        respuesta_busqueda = busqueda_google_chatbot(busqueda[0])
       
        return {"respuesta": respuesta_busqueda}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error general: {str(e)}")

