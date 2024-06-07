import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from Filtro_de_Robinson2 import FiltroRobinson
from Filtro_Umbralado2 import FiltroUmbralado
from filtromin2 import FiltroMin
from Gamma2 import Gama

def cargar_imagen():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.bmp")])
    if ruta_archivo:
        img = cv2.imread(ruta_archivo)
        return img, ruta_archivo
    return None, None

def mostrar_imagen(img, etiqueta, tamaño_max=(400, 300)):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail(tamaño_max, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)
    etiqueta.config(image=img_tk)
    etiqueta.image = img_tk

def mostrar_histograma(img, etiqueta, tamaño_max=(400, 300)):
    for widget in etiqueta.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 3))
    if len(img.shape) == 2:
        ax.hist(img.ravel(), bins=256, color='black', alpha=0.7)
    else:
        colores = ('r', 'g', 'b')
        for i, color in enumerate(colores):
            ax.hist(img[:, :, i].ravel(), bins=256, color=color, alpha=0.7)
    ax.set_xlim([0, 256])
    ax.set_ylim([0, None])
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=etiqueta)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    etiqueta.config(width=tamaño_max[0], height=tamaño_max[1])

    return fig

def mostrar_histograma_gris(img, etiqueta, tamaño_max=(400, 300)):
    for widget in etiqueta.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(img.ravel(), bins=256, color='black', alpha=0.7)
    ax.set_xlim([0, 256])
    ax.set_ylim([0, None])
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=etiqueta)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    etiqueta.config(width=tamaño_max[0], height=tamaño_max[1])

    return fig

def cerrar_plots(figuras):
    for fig in figuras:
        plt.close(fig)

raiz = tk.Tk()
raiz.title("Procesamiento Digital de Imágenes")
raiz.geometry("1050x700")

control_pestañas = ttk.Notebook(raiz)

pestaña_portada = ttk.Frame(control_pestañas)
control_pestañas.add(pestaña_portada, text="Portada")

pestaña_robinson = ttk.Frame(control_pestañas)
control_pestañas.add(pestaña_robinson, text="Filtro de Robinson")

pestaña_umbralado = ttk.Frame(control_pestañas)
control_pestañas.add(pestaña_umbralado, text="Filtro Umbralado")

pestaña_min = ttk.Frame(control_pestañas)
control_pestañas.add(pestaña_min, text="Filtro Mínimo")

pestaña_gama = ttk.Frame(control_pestañas)
control_pestañas.add(pestaña_gama, text="Gama")

control_pestañas.pack(expand=1, fill="both")

imagen_fondo = Image.open("fondo.jpg")
imagen_fondo = ImageOps.fit(imagen_fondo, (1050, 700), Image.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
etiqueta_fondo = tk.Label(pestaña_portada, image=imagen_fondo)
etiqueta_fondo.place(relwidth=1, relheight=1)

titulo = tk.Label(pestaña_portada, text="Segmentación de Zonas con presencia\nde incendios forestales en tomas satelitales",
                 font=("Helvetica", 18, "bold"), bg=None)
titulo.pack(pady=20)

info = tk.Label(pestaña_portada, text="Comunidad 7:\n• Díaz Martínez Aldo\n• Lagunes Vázquez Mildred Valeria\n• Lezama Tapia Brisa María.\n• Meléndez Medina Jimena\n• Pérez Aguirre Ian Miztli.", 
                justify="left", font=("Helvetica", 14), bg=None)
info.pack(pady=10)

texto_seleccionar = tk.Label(pestaña_portada, text="Seleccione una imagen para modificar", font=("Helvetica", 12), bg=None)
texto_seleccionar.pack(pady=10)

ruta_archivo = None
img_seleccionada = None

def seleccionar_archivo():
    global ruta_archivo, img_seleccionada
    img_seleccionada, ruta_archivo = cargar_imagen()
    if img_seleccionada is not None:
        texto_leyenda.set(f"Imagen ({os.path.basename(ruta_archivo)}) cargada correctamente")
        aplicar_algoritmos()

selector_archivo = tk.Button(pestaña_portada, text="Seleccionar Imagen", command=seleccionar_archivo)
selector_archivo.pack(pady=10)

texto_leyenda = tk.StringVar()
etiqueta_leyenda = tk.Label(pestaña_portada, textvariable=texto_leyenda, font=("Helvetica", 12), bg=None)
etiqueta_leyenda.pack(pady=10)

filtro_robinson = FiltroRobinson()
filtro_umbralado = FiltroUmbralado()
filtro_min = FiltroMin()
gama = Gama()

def aplicar_algoritmos():
    if img_seleccionada is not None:
        for figuras in figuras_pestañas.values():
            cerrar_plots(figuras)

        figuras_robinson = mostrar_resultados_algoritmo(filtro_robinson, etiqueta_robinson_original, histograma_robinson_original, etiqueta_robinson_procesada, histograma_robinson_procesada)
        figuras_umbralado = mostrar_resultados_umbralado(filtro_umbralado, etiqueta_umbralado_original, histograma_umbralado_original, etiqueta_umbralado_procesada, histograma_umbralado_procesada)
        figuras_min = mostrar_resultados_algoritmo(filtro_min, etiqueta_min_original, histograma_min_original, etiqueta_min_procesada, histograma_min_procesada)
        figuras_gama = mostrar_resultados_algoritmo(gama, etiqueta_gama_original, histograma_gama_original, etiqueta_gama_procesada, histograma_gama_procesada)
        
        figuras_pestañas['Filtro de Robinson'] = figuras_robinson
        figuras_pestañas['Filtro Umbralado'] = figuras_umbralado
        figuras_pestañas['Filtro Mínimo'] = figuras_min
        figuras_pestañas['Gama'] = figuras_gama

def mostrar_resultados_algoritmo(algoritmo, etiqueta_img_original, histograma_img_original, etiqueta_img_procesada, histograma_img_procesada):
    mostrar_imagen(img_seleccionada, etiqueta_img_original)
    figura_original = mostrar_histograma(img_seleccionada, histograma_img_original)

    img_procesada = algoritmo.aplicar(img_seleccionada)
    mostrar_imagen(img_procesada, etiqueta_img_procesada)
    figura_procesada = mostrar_histograma(img_procesada, histograma_img_procesada)

    return [figura_original, figura_procesada]

def mostrar_resultados_umbralado(algoritmo, etiqueta_img_original, histograma_img_original, etiqueta_img_procesada, histograma_img_procesada):
    img_gris = cv2.cvtColor(img_seleccionada, cv2.COLOR_BGR2GRAY)
    mostrar_imagen(img_gris, etiqueta_img_original)
    figura_original = mostrar_histograma_gris(img_gris, histograma_img_original)

    img_procesada = algoritmo.aplicar(img_seleccionada)  # Pasa la imagen original en color
    mostrar_imagen(img_procesada, etiqueta_img_procesada)
    figura_procesada = mostrar_histograma_gris(img_procesada, histograma_img_procesada)

    return [figura_original, figura_procesada]

def crear_cuadricula(pestaña):
    etiqueta_img_original = tk.Label(pestaña, bg=None)
    etiqueta_img_original.grid(row=0, column=0, padx=10, pady=10)

    histograma_img_original = tk.Label(pestaña, bg=None)
    histograma_img_original.grid(row=1, column=0, padx=10, pady=10)

    etiqueta_img_procesada = tk.Label(pestaña, bg=None)
    etiqueta_img_procesada.grid(row=0, column=1, padx=10, pady=10)

    histograma_img_procesada = tk.Label(pestaña, bg=None)
    histograma_img_procesada.grid(row=1, column=1, padx=10, pady=10)

    return etiqueta_img_original, histograma_img_original, etiqueta_img_procesada, histograma_img_procesada

etiqueta_robinson_original, histograma_robinson_original, etiqueta_robinson_procesada, histograma_robinson_procesada = crear_cuadricula(pestaña_robinson)
etiqueta_umbralado_original, histograma_umbralado_original, etiqueta_umbralado_procesada, histograma_umbralado_procesada = crear_cuadricula(pestaña_umbralado)
etiqueta_min_original, histograma_min_original, etiqueta_min_procesada, histograma_min_procesada = crear_cuadricula(pestaña_min)
etiqueta_gama_original, histograma_gama_original, etiqueta_gama_procesada, histograma_gama_procesada = crear_cuadricula(pestaña_gama)

figuras_pestañas = {}

def al_cambiar_pestaña(evento):
    pestaña_seleccionada = evento.widget.tab('current')['text']
    for pestaña, figuras in figuras_pestañas.items():
        if pestaña != pestaña_seleccionada:
            cerrar_plots(figuras)

control_pestañas.bind("<<NotebookTabChanged>>", al_cambiar_pestaña)

raiz.mainloop()
