# 🤖 Jarvitos: Assistente Pessoal por Voz com GPT ou Gemini + Previsão do Tempo

Este projeto é um assistente pessoal ativado por voz chamado **Jarvis**, que pode ser usado com **OpenAI GPT** ou com o **Gemini da Google**. Ele reconhece comandos de voz, responde com voz sintética e pode consultar a previsão do tempo para qualquer cidade informada.

## 🧠 Funcionalidades

- Reconhecimento de voz com `speech_recognition`
- Síntese de voz com `pyttsx3`
- Respostas inteligentes com:
  - **OpenAI GPT (gpt-3.5-turbo ou gpt-4o-mini)**
  - **Google Gemini (gemini-pro ou gemini-2.0-flash)**
- Previsão do tempo com base na localização (via [Open-Meteo](https://open-meteo.com/))
- Busca automática de latitude/longitude com IA
- Ativação por voz com a palavra-chave **"jarvis"**

## 📁 Estrutura dos Arquivos

- `Jarvitos.py`: versão do assistente usando **OpenAI GPT**
- `jarvitos_com_gemini.py`: versão do assistente usando **Google Gemini**

## 🛠️ Tecnologias Utilizadas

- Python 3
- [OpenAI API](https://platform.openai.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Requests](https://pypi.org/project/requests/)
- Open-Meteo API (gratuita)

## ⚙️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/jarvis-assistente-voz.git
cd jarvis-assistente-voz
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> **Nota:** Para sistemas Windows, use:
> pip install pipwin
> pipwin install pyaudio

## 🔑 Configuração das Chaves de API

- No `Jarvitos.py`:
```python
openai.api_key = "SUA_CHAVE_OPENAI"
```

- No `jarvitos_com_gemini.py`:
```python
genai.configure(api_key="SUA_CHAVE_GEMINI")
```

## 🎙️ Como Usar

1. Execute uma das versões do script:

**Usando OpenAI GPT:**
```bash
python Jarvitos.py
```

**Usando Gemini:**
```bash
python jarvitos_com_gemini.py
```

2. Diga: `jarvis` para ativar o assistente.

3. Faça perguntas como:
   - “Qual é a temperatura em Recife?”
   - “Vai chover em São Paulo?”
   - “Quem descobriu o Brasil?”

## 🎧 Configuração do Microfone

Altere o índice do microfone, se necessário:
```python
MICROFONE_INDEX = 1
```

Para listar os dispositivos disponíveis:
```python
import speech_recognition as sr
print(sr.Microphone.list_microphone_names())
```

## 🧪 Exemplo de Uso

```
Aguardando comando...
Você: jarvis
Jarvis: Estou ouvindo, mestre.
Você: Qual é a temperatura em Fortaleza?
Jarvis: A temperatura em Fortaleza é de 29 graus.
```

## 🧑‍💻 Autor

- [João Victor Monteiro Tancon](https://github.com/jtancon)
