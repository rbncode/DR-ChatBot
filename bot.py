from fastapi import FastAPI, HTTPException
from serpapi.google_search import GoogleSearch
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Crear una instancia de FastAPI
app = FastAPI()

# Función para consultar Gemini AI
def consultar_gemini(pregunta):
    try:
        load_dotenv("key.env") 
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise HTTPException(status_code=500, detail="Error: No se encontró la clave API de Gemini.")
        
        # Configurar la API de Gemini
        genai.configure(api_key=api_key)
        
        # Seleccion de modelos disponibles en tu lista
        modelo = genai.GenerativeModel('gemma-3-27b-it')
        
        # Enviar la consulta y obtener respuesta
        respuesta = modelo.generate_content(pregunta)
        
        return respuesta.text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Gemini AI: {str(e)}")

# Función para realizar búsqueda en Google
def busqueda_google_chatbot(pregunta):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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

        return respuesta.text  # Devolver solo el texto de la respuesta

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la búsqueda en Google: {str(e)}")

# Endpoint principal
@app.post("/chatbot/")
async def chatbot_endpoint(pregunta_usuario: dict):
    try:
        # Cargar variables de entorno
        load_dotenv("key.env") 

    
        system_prompt = "En base a la pregunta del usuario se debe identificar una busqueda en google a realizar clave, que puede ser solo una de la siguiente lista " \
        "1) El clima del dia en la zona que se pregunta el dia de hoy(esta debe ser respondida con respecto a como se pregunte) " \
        "2) El valor de la UF hoy" \
        "3) El valor del dolar hoy" \
        "4) Noticias del dia" \
        "5) La hora actual en la zona que se pregunta" \
        "Si el usuario pregunta algo fuera de esto devuelve -NEGATIVO- " \
        "Si puedes identificar la pregunta en una de las catergoria responde como si fueras a realizar una busqueda en google del tema poniendo lo que buscaras " \
        "entre 2 #." \
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
            return {"respuesta": respuesta_gemini}  # Si no hay búsqueda, devolver la respuesta directamente

        # Realizar búsqueda en Google
        respuesta_busqueda = busqueda_google_chatbot(busqueda[0])

        return {"respuesta": respuesta_busqueda}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error general: {str(e)}")

