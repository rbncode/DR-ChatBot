import google.generativeai as genai
import os
from dotenv import load_dotenv

def consultar_gemini(pregunta):
    try:
        load_dotenv("key.env") 
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "Error: No se encontró la clave API de Gemini. Asegúrate de configurar GEMINI_API_KEY en tus variables de entorno."
        
        # Configurar la API de Gemini
        genai.configure(api_key=api_key)
        
        # Seleccion de modelos disponibles en tu lista
        modelo = genai.GenerativeModel('gemma-3-27b-it')
        
        # Enviar la consulta y obtener respuesta
        respuesta = modelo.generate_content(pregunta)
        
        return respuesta.text
        
    except Exception as e:
        return f"Error al consultar Gemini AI: {str(e)}"

# Función para listar modelos disponibles
def listar_modelos_disponibles(api_key):
    genai.configure(api_key=api_key)
    for m in genai.list_models():
        print(f"Nombre: {m.name}")
        print(f"Métodos disponibles: {m.supported_generation_methods}")
        print("---")

if __name__ == "__main__":
    pregunta_usuario = input("Ingresa tu pregunta para Gemini AI: ")
    respuesta = consultar_gemini(pregunta_usuario)
    print("\nRespuesta de Gemini AI:")
    print(respuesta)