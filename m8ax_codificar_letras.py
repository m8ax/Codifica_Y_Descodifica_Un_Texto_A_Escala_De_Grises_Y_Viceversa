##############################################################################################################################
#
#  PROGRAMA CREADO POR M8AX - MARCOS OCHOA DIEZ, PARA PINTAR PÍXELES EN ESCALA DE GRISES, SEGÚN LOS CARACTERES
#  QUE SE ENCUENTRAN EN EL FICHERO TEXTO.TXT, USANDO PARA ELLO EL VALOR ASCII DE CADA CARÁCTER Y PINTÁNDOLO DEL COLOR
#  CORRESPONDIENTE AL VALOR ASCII. ESCALA DE GRISES Y ASCII USAN VALORES DE 0 A 255.
#  CON ESTE PROGRAMA PODREMOS CODIFICAR EL TEXTO QUE QUERAMOS EN UNA IMÁGEN EN ESCALA DE GRISES.
#  EL FICHERO DE TEXTO A CODIFICAR SERA TEXTO.TXT Y EL FICHERO DE IMÁGEN DE SALIDA SE LLAMARÁ M8AX-TEXTOCODIFICADO.PNG
#
#  Ejemplo - py m8ax_codificar_letras.py
#
##############################################################################################################################

import time
import math
from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageChops, ImageEnhance, ImageOps
import sympy
import numpy as np
import os
import cv2
import sys


def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"


def barra_progreso_vibrante(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        f"\r\033[38;2;{np.random.randint(0, 256)};{np.random.randint(0, 256)};{np.random.randint(0, 256)}m|{barra}| - ETA - {segahms(segrestante*-1)} - {porcen:.2f}%",
        end="\r\033[0m",
    )


fichero = open("texto.txt", "r", encoding="Latin-1")
caracteres = 0

for linea in fichero:
    caracteres += len(linea)
fichero.close()

tamaimagen = (caracteres**0.5) + 1
os.system("cls")
print("")
img = Image.new("RGB", (int(tamaimagen), int(tamaimagen)), color="black")
img.save("Imagen.PnG")

imagencodigris = cv2.imread("Imagen.PnG")
imagencodigris = cv2.cvtColor(imagencodigris, cv2.COLOR_BGR2GRAY)
wip = imagencodigris.shape[1]
hep = imagencodigris.shape[0]
pixeles = hep * wip
cuenta = 0
bien = 1

file = open("Texto.TxT", "r", encoding="Latin-1")

if hep > wip:
    cambiando = wip
    wip = hep
    hep = cambiando
else:
    cambiando = hep
    hep = wip
    wip = cambiando

tiembarra = time.time()

while bien == 1 and cuenta < pixeles:
    for fila in range(wip):
        for columna in range(hep):
            cuenta = cuenta + 1
            if cuenta > pixeles:
                break
            try:
                char = file.read(1)
                numpi = int(ord(char))
            except:
                bien = 0
                break
            imagencodigris[fila, columna] = numpi

        barra_progreso_vibrante((fila * columna * 100) / (wip * hep), 100, tiembarra)

barra_progreso_vibrante((wip * hep * 100) / (wip * hep), 100, tiembarra)
print(
    f"\n\nCodificación Realizada En {segahms(time.time()-tiembarra)}, A {round(caracteres/(time.time()-tiembarra),3)} Pixeles/Seg."
)
print("\n... Trabajo Realizado Correctamente ...\n\nBy M8AX...")
file.close()
cv2.imwrite("M8AX-TextoCodificado.PnG", imagencodigris)
cv2.imshow(
    "--- M8AX IMAGEN DE TEXTO CODIFICADAS EN ESCALA DE GRISES ---", imagencodigris
)
metadata = PngInfo()
imagencodigris = Image.open("M8AX-TextoCodificado.PnG")
metadata.add_text(
    "MvIiIaX.M8AX - Comentario - ",
    "... Por Muchas Vueltas Que Demos, Siempre Tendremos El Culo Atrás ...",
)
metadata.add_text("M8AX-ID", str(10031977))
imagencodigris.save("M8AX-TextoCodificado.PnG", pnginfo=metadata)
cv2.waitKey(0)
cv2.destroyAllWindows()
