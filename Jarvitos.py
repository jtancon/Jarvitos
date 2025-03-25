import openai
import speech_recognition as sr
import pyttsx3
import time
import requests

# Inicializa o reconhecedor e o motor de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configuração do microfone (substitua o índice pelo do seu microfone desejado)
MICROFONE_INDEX = 1  
openai.api_key = "" #sua chave gpt
# API do Open-Meteo
class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude, longitude, lang="pt", units="metric"):
        """
        Consulta a previsão do tempo com base em coordenadas de latitude e longitude.

        Args:
            latitude (float): Latitude do local.
            longitude (float): Longitude do local.
            lang (str): Idioma da resposta (default: "pt").
            units (str): Unidade métrica ("metric" para °C).

        Returns:
            dict: Informações sobre o clima (temperatura e descrição).
        """
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
    """
    Usa o microfone configurado para ouvir um comando de voz.
    """
    try:
        with sr.Microphone(device_index=MICROFONE_INDEX) as source:
            print("Aguardando comando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            texto = recognizer.recognize_google(audio, language="pt-BR")
            return texto.lower()
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return None
    except sr.RequestError:
        print("Erro ao acessar o serviço de reconhecimento de fala.")
        return None
    except sr.WaitTimeoutError:
        print("Tempo de espera excedido. Nenhum som detectado.")
        return None
    except Exception as e:
        print(f"Erro ao usar o microfone: {e}")
        return None

def falar(mensagem):
    print(mensagem)
    engine.say(mensagem)
    engine.runAndWait()

def analisar_com_gpt(prompt):
    """
    Usa o GPT para responder a perguntas genéricas.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda o usuário em perguntas gerais."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao consultar o GPT: {e}")
        return "Não consegui processar sua solicitação no momento."

def obter_coordenadas_com_gpt(cidade):
    """
    Usa o GPT para obter a latitude e longitude de uma cidade.

    Args:
        cidade (str): Nome da cidade.

    Returns:
        tuple: Latitude e longitude da cidade.
    """
    prompt = f"Qual é a latitude e longitude da cidade {cidade}? Responda no formato: latitude=-X, longitude=-Y"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente que fornece informações geográficas."},
                {"role": "user", "content": prompt}
            ]
        )
        resposta = response.choices[0].message.content
        print(f"Resposta do GPT: {resposta}")

        # Usa regex para extrair os valores de latitude e longitude
        import re
        match = re.search(r"latitude=([-+]?[0-9]*\.?[0-9]+), longitude=([-+]?[0-9]*\.?[0-9]+)", resposta)
        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude
        else:
            print("Formato de resposta inesperado do GPT.")
            return None, None
    except Exception as e:
        print(f"Erro ao consultar o GPT: {e}")
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
                # Verifica se a pergunta é sobre o clima
                if "temperatura" in pergunta or "vai chover" in pergunta:
                    falar("Diga o nome da cidade.")
                    cidade = ouvir()
                    if cidade:
                        # Obtém as coordenadas da cidade usando o GPT
                        latitude, longitude = obter_coordenadas_com_gpt(cidade)
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
                    # Usa o GPT para outras perguntas
                    resposta = analisar_com_gpt(pergunta)
                    falar("Resposta tirada do GPT: " + resposta)
                    break
