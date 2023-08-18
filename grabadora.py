import sounddevice as sd
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import scipy.io.wavfile as wavfile
import time
import os

# ----------- FUNCIONES -----------

def callback(indata, frames, time, status):
    global audio_blocks
    if status:
        print(status)
    audio_blocks.append(indata.copy())

def actualizar_contador():
    global contador_segundos, contador_minutos, contador_id
    if contador_segundos >= 59:
        contador_minutos += 1
        contador_segundos = 0
    else:
        contador_segundos += 1
    contador.set(f"{contador_minutos:02d}:{contador_segundos:02d}")
    contador_id = raiz.after(1000, actualizar_contador)
    
def guardar_en():
    global ruta_musica
    ruta_musica = filedialog.askdirectory(title="Seleccionar carpeta")
    
def grabar():
    global contador_segundos, contador_minutos, recording, audio_blocks
    boton_stop.config(state="normal")
    boton_play.config(state="disabled")
    boton_abrir.config(state="disabled")
    contador_segundos = 0
    contador_minutos = 0
    audio_blocks = []
    actualizar_contador()
    recording = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback)
    recording.start()
    
def detener():
    global recording, SAMPLE_RATE, ruta_musica, primer_audio, archivo
    boton_stop.config(state="disabled")
    raiz.after_cancel(contador_id)
    recording.stop()
    recording.close()
    audio_data = np.concatenate(audio_blocks, axis=0)
    timestamp = time.strftime("%Y%m%d%H%M%S")
    if primer_audio:
        primer_audio = False
        guardar_en() 
    archivo = ruta_musica + f"/grabacion_{timestamp}.wav"
    wavfile.write(archivo, SAMPLE_RATE, audio_data)
    raiz.after(500)
    boton_play.config(state="normal")
    boton_abrir.config(state="normal")

def abrir():
    global archivo
    try:
        if os.name == "nt":  # Windows
            os.system(f'start "" "{archivo}"')
        elif os.name == "posix":  # macOS y Linux
            os.system(f'open "{archivo}"')
    except Exception as e:
        print(f"No se pudo reproducir el archivo: {e}")

# ----------- VARIABLES -----------
SAMPLE_RATE = 44100 # Frecuencia de muestreo
CHANNELS = 2 # Número de canales (2 para estéreo)

audio_blocks = []
primer_audio = True
ruta_musica = ""
archivo = ""

# ----------- TKINTER -----------
raiz = tk.Tk()
raiz.title("Grabadora")
raiz.resizable(0,0)
raiz.iconbitmap("logo.ico")

frame = tk.Frame(raiz, bg="black")
frame.grid()

# ----------- AJUSTAR IMAGENES -----------
image_play = Image.open("microphone.png")
image_play = image_play.resize((100,100))
img_play = ImageTk.PhotoImage(image_play)

image_stop = Image.open("stop.png")
image_stop = image_stop.resize((100,100))
img_stop = ImageTk.PhotoImage(image_stop)

# ----------- CONTADOR -----------
contador = tk.StringVar()
contador.set("00:00")
contador_segundos = 0
contador_minutos = 0
contador_id = ""

# ----------- WIDGETS -----------
boton_play = tk.Button(frame, image=img_play, bg="black", activebackground="black", borderwidth=0, command=grabar)
boton_play.grid(row=1, column=1, padx=10, pady=10)

boton_stop = tk.Button(frame, image=img_stop, bg="black", activebackground="black", borderwidth=0, command=detener, state="disabled")
boton_stop.grid(row=1, column=3, padx=10, pady=10)

boton_abrir = tk.Button(frame, text="Abrir", font=("Helvetica"), bg="black", fg="white", relief="groove", activebackground="black", activeforeground="white", command=abrir, state="disabled")
boton_abrir.grid(row=2, column=1, padx=10, pady=10)

label_contador = tk.Label(frame, textvariable=contador, font=("Helvetica", 20), bg="black", fg="white")
label_contador.grid(row=1, column=2, padx=10, pady=10)

boton_guardar_en = tk.Button(frame, text="Ubicación...", font=("Helvetica"), bg="black", fg="white", relief="groove", activebackground="black", activeforeground="white", command=guardar_en)
boton_guardar_en.grid(row=2, column=3, padx=10, pady=10)

raiz.mainloop()

