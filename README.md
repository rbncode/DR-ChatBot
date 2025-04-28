# Aplicación ChatBot

Asistente virtual de ChatBot que se encarga de entregar respuestas del usuario respecto a UF, dólar, clima y noticias.

### Integrantes del Proyecto
- Francisca Neira
- Benjamín Urrea
- Robin Vásquez
- Sebastián Yáñez
- Sebastián Vidal

## Requisitos de execución

1. Instalación de dependencias Front-End

   ```bash
   npm install expo
   npm install react-native-markdown-display
   ```

> [!IMPORTANT]
> Además de estas dependencias, en caso de realizar pruebas desde el celular, se requiere de la aplicación Expo Go. Si se realizan desde un computador, ingresar desde el puerto en localhost asignado una vez iniciado.

2. Instalación de dependencias del Back-End

   ```bash
    pip install -r requirements.txt
    pip install fastapi
    pip install google-search-results
    pip install google-generativeai python-dotenv
    pip install transformers torch sentencepiece --user
    pip install requests
   ```

3. Para realizar pruebas

   ```bash
    pip install pytest
    cd backend
    python -m pytest test_chatbot.py
   ```

## Ejecución del proyecto

Para ejecutar el proyecto se puede realizar por dos métodos distintos:

1. Único terminal

   ```bash
   npm run start
   ```

> [!NOTE]
> Esto ejecutará tanto el front-end como back-end para el projecto. Asegurarse que el IP de conexión de de REST esté acordé a la conexión Wi-Fi utilizada.
   
3. Ejecución por separado

- Para ejecutar Front-End:
   ```bash
   npx expo start
   ```

- Para ejecutar Back-End:
   ```bash
   npm run start-back
   ```

> [!NOTE]
> Se deben utilizar dos terminales diferentes con este método. Asegurarse que el IP de conexión de de REST esté acordé a la conexión Wi-Fi utilizada.
