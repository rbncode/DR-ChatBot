from fastapi.testclient import TestClient
from bot import app  # Importa tu aplicación FastAPI

client = TestClient(app)

def test_cp1_consulta_clima_ciudad():
    # Entrada simulada
    payload = {"pregunta": "¿Cuál es el clima en Temuco?"}

    # Realizar la petición POST al endpoint
    response = client.post("/chatbot/", json=payload)

    # Verificar que la respuesta sea exitosa
    assert response.status_code == 200

    # Verificar que la respuesta contenga algo relacionado al clima
    respuesta_texto = response.json().get("respuesta", "").lower()

    # Puedes ajustar esta parte si quieres ser más estricto con palabras clave
    assert any(
        palabra in respuesta_texto for palabra in ["temperatura", "clima", "grados", "cielo", "pronóstico"]
    ), "La respuesta no contiene información meteorológica esperada."

def test_cp2_consulta_informal_clima_ciudad():
    payload = {"pregunta": "tiempo en temuco"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["temperatura", "clima", "temuco"]
    )

def test_cp3_consulta_clima_ciudad_error_ortografico():
    payload = {"pregunta": "clima temuko"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["temperatura", "clima", "temuco"]
    )

def test_cp4_consulta_ambigua_clima_1():
    payload = {"pregunta": "¿Cómo está allá?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp5_consulta_valor_dolar_1():
    payload = {"pregunta": "¿Cuánto vale el dólar hoy?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["valor", "dolar", "chile"]
    )

def test_cp6_consulta_valor_dolar_2():
    payload = {"pregunta": "¿A cuánto está el dólar?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["valor", "dolar", "chile"]
    )

def test_cp7_consulta_informal_valor_dolar():
    payload = {"pregunta": "dólar hoy"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["valor", "dolar", "chile"]
    )

def test_cp8_consulta_erronea_valor_dolar():
    payload = {"pregunta": "dolaro"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp9_consulta_noticias_actualizadas():
    payload = {"pregunta": "Noticias importantes del día"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["noticias", "hoy", "actualizadas"]
    )

def test_cp10_consulta_noticias_ciudad():
    payload = {"pregunta": "Noticias en Temuco hoy"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["noticias", "hoy", "temuco"]
    )

def test_cp11_consulta_informal_noticias_actualizadas():
    payload = {"pregunta": "¿Qué pasó últimamente?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["noticias", "hoy", "general"]
    )

def test_cp12_consulta_ambigua_noticias():
    payload = {"pregunta": "Dame noticias"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp13_consulta_valor_uf_1():
    payload = {"pregunta": "Precio de la UF hoy"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["uf", "valor", "pesos"]
    )

def test_cp14_consulta_valor_uf_2():
    payload = {"pregunta": "¿A cuánto está la UF?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["uf", "valor", "pesos"]
    )

def test_cp15_consulta_valor_uf_3():
    payload = {"pregunta": "¿Cuál es el valor de la UF?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["uf", "valor", "pesos"]
    )

def test_cp16_consulta_contenido_invalido():
    payload = {"pregunta": "😊🌧️"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp17_consulta_vacia():
    payload = {"pregunta": ""}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 500
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp18_consulta_ambigua_clima_2():
    payload = {"pregunta": "¿Qué tiempo hace?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp19_consulta_información_pandemia():
    payload = {"pregunta": "Cuando fue la pandemia"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp20_consulta_informacion_partido_Chile():
    payload = {"pregunta": "Cuando juega Chile"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp21_consulta_informacion_sismos_recientes():
    payload = {"pregunta": "Últimos terremotos en Chile"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp22_consulta_informacion_sismos_actualizado():
    payload = {"pregunta": "¿Hubo un sismo hoy?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp23_consulta_informacion_sismos_tiempo_real():
    payload = {"pregunta": "¿Tiembla ahora?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto
    
def test_cp24_consulta_noticias_locales():
    payload = {"pregunta": "¿Qué pasó en Temuco hoy?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["noticias", "hoy", "temuco"]
    )

def test_cp25_consulta_informacion_estado_transito():
    payload = {"pregunta": "¿Cómo están las carreteras?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp26_consulta_informacion_estado_metro():
    payload = {"pregunta": "Estado del metro en Santiago"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp27_consulta_informacion_estado_linea_metro():
    payload = {"pregunta": "¿Funciona la línea 1 del metro?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp28_consulta_informacion_resultado_equipo_local():
    payload = {"pregunta": "Resultado del partido de Colo Colo"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto
    
def test_cp29_consulta_informacion_torneo_internacional():
    payload = {"pregunta": "Resultado Champions League"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp30_consulta_valor_euro():
    payload = {"pregunta": "¿A cuánto está el euro hoy?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp31_consulta_informacion_precio_petroleo():
    payload = {"pregunta": "Precio del petróleo"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp32_consulta_informacion_humedad_ciudad():
    payload = {"pregunta": "¿Cuál es la humedad en Valparaíso?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["clima", "humedad", "valparaiso"]
    )

def test_cp33_consulta_temperatura_actual_ciudad():
    payload = {"pregunta": "¿Cuántos grados hay en Iquique?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert any(
        palabra in respuesta_texto for palabra in ["clima", "temperatura", "iquique"]
    )
    
def test_cp34_consulta_informacion_alerta_incendios():
    payload = {"pregunta": "¿Hay alerta de incendios en la Araucanía?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto

def test_cp35_consulta_informacion_alreta_sanitaria():
    payload = {"pregunta": "¿Hay alerta sanitaria en Chile?"}
    response = client.post("/chatbot/", json=payload)
    assert response.status_code == 200
    respuesta_texto = response.json().get("respuesta", "").lower()
    assert "lo siento, no puedo ayudar con esa pregunta" in respuesta_texto