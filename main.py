import webbrowser
import gradio 
import openai
from config import key

openai.api_key = key

def chat_bot(accion, contenido):
    solicitud = openai.Chatcomplemetion.create(
        model = "gpt-3.5-turbo",
        message=[
            {"role":"system","content":contenido},
            {"role":"user","content": accion},
        ]
    )
    respuesta = solicitud.choise[0].message.content
    return respuesta 

def solicitud_audio(audio):
    
    archivo_audio = open(audio, "rb")
    transcipcion_audio =  openai.Audio.transcribe("whisper-1",archivo_audio)

    palabras_transcribidas = transcipcion_audio["text"].split(maxsplit = 1)
    
    if "decime" in palabras_transcribidas[0].lower():
        return chat_bot(palabras_transcribidas[0],"sos un chatbot")
    elif "dibujame" in palabras_transcribidas[0].lower():
        solicitud = openai.Image.create(
            prompt = palabras_transcribidas[1],
            n = 1,
            size = "1024x1024",
        )
        url_imagen = solicitud['data'][0]['url']
        webbrowser.open(url_imagen)
        return 'Abriendo imagen'
    
interfaz = gradio.Interface(fn = solicitud_audio,inputs= gradio.Audio(source="microphone",type="filepath"),outputs=gradio.outputs.Textbox())
interfaz.launch(inbrowser=True)