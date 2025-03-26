
import speech_recognition as sr
import pyttsx3
import time
import requests
import google.generativeai as genai
import re

# Configuração da chave da API Gemini
genai.configure(api_key="coloque_sua_chave_aqui")

# Inicializa o reconhecedor e o motor de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configuração do microfone
MICROFONE_INDEX = 1

# API do Open-Meteo
class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude, longitude, lang="pt", units="metric"):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "timezone": "auto",
            "language": lang,
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            current_weather = data.get("current_weather", {})
            return {
                "temperatura": current_weather.get("temperature"),
                "descricao": current_weather.get("weathercode"),
                "vento": current_weather.get("windspeed"),
            }
        else:
            return {"erro": f"Não foi possível obter os dados. Código HTTP: {response.status_code}"}

# Funções auxiliares
def ouvir():
    try:
        with sr.Microphone(device_index=MICROFONE_INDEX) as source:
            print("Aguardando comando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            texto = recognizer.recognize_google(audio, language="pt-BR")
            return texto.lower()
    except:
        return None

def falar(mensagem):
    print(mensagem)
    engine.say(mensagem)
    engine.runAndWait()

def analisar_com_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao consultar o Gemini: {e}")
        return "Não consegui processar sua solicitação no momento."

def obter_coordenadas_com_gemini(cidade):
    prompt = f"Qual é a latitude e longitude da cidade {cidade}? Responda no formato: latitude=-X, longitude=-Y"
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        resposta = response.text
        match = re.search(r"latitude=([-+]?[0-9]*\.?[0-9]+), longitude=([-+]?[0-9]*\.?[0-9]+)", resposta)
        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude
        else:
            return None, None
    except:
        return None, None

# Configuração da API do Open-Meteo
weather_api = WeatherAPI()

# Loop principal
while True:
    texto = ouvir()
    if texto and "jarvis" in texto:
        falar("Estou ouvindo, mestre.")
        tempo_inicio = time.time()
        while time.time() - tempo_inicio < 10:
            pergunta = ouvir()
            if pergunta:
                if "temperatura" in pergunta or "vai chover" in pergunta:
                    falar("Diga o nome da cidade.")
                    cidade = ouvir()
                    if cidade:
                        latitude, longitude = obter_coordenadas_com_gemini(cidade)
                        if latitude is not None and longitude is not None:
                            clima = weather_api.get_weather(latitude, longitude)
                            if "erro" in clima:
                                falar(clima["erro"])
                            else:
                                falar(f"A temperatura em {cidade} é de {clima['temperatura']} graus.")
                        else:
                            falar("Não consegui obter as coordenadas da cidade.")
                    break
                else:
                    resposta = analisar_com_gemini(pergunta)
                    falar("Resposta tirada do Gemini: " + resposta)
                    break
