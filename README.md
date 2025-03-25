# 🤖 Jarvis: Assistente Pessoal por Voz com GPT e Previsão do Tempo

Este projeto é um assistente pessoal ativado por voz chamado **Jarvis**, que utiliza o **OpenAI GPT** para responder perguntas e a **API Open-Meteo** para informar a previsão do tempo. O sistema reconhece comandos por voz, responde utilizando síntese de voz, e pode ser expandido para outras funcionalidades.

## 🧠 Funcionalidades

- Reconhecimento de voz com `speech_recognition`
- Síntese de voz com `pyttsx3`
- Respostas inteligentes com **ChatGPT (OpenAI GPT)**
- Previsão do tempo por cidade com a API do [Open-Meteo](https://open-meteo.com/)
- Busca automática de coordenadas geográficas via GPT
- Ativação por comando de voz com a palavra-chave "jarvis"

## 🛠️ Tecnologias Utilizadas

- Python 3
- [OpenAI API](https://platform.openai.com/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Requests](https://pypi.org/project/requests/)
- Open-Meteo API (gratuita e sem necessidade de chave)

## ⚙️ Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/jarvis-assistente-voz.git
cd jarvis-assistente-voz
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> **Nota:** O `PyAudio` pode precisar de dependências extras no sistema. No Windows, recomenda-se usar:  
> `pip install pipwin` seguido de `pipwin install pyaudio`

4. Adicione sua chave da API OpenAI no código:

No trecho:
```python
openai.api_key = ""
```
Insira sua chave entre as aspas.

## 🎙️ Como Usar

1. Execute o script:

```bash
python jarvis.py
```

2. Diga a palavra-chave **"jarvis"** para ativar o assistente.

3. Faça uma pergunta, como:
   - “Qual é a temperatura em São Paulo?”
   - “Vai chover hoje em Recife?”
   - “Quem descobriu o Brasil?”

4. O assistente responderá por voz.

## 🎧 Configuração do Microfone

Altere o índice do microfone se necessário:
```python
MICROFONE_INDEX = 1
```
Você pode descobrir os dispositivos disponíveis com:

```python
import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, name)
```

## 📌 Exemplo de Uso

```bash
Aguardando comando...
Você: jarvis
Jarvis: Estou ouvindo, mestre.
Você: Qual é a temperatura em Fortaleza?
Jarvis: Diga o nome da cidade.
Você: Fortaleza
Jarvis: A temperatura em Fortaleza é de 29 graus.
```

## 🧑‍💻 Autor

- [João Victor Monteiro Tancon](https://github.com/jtancon)

