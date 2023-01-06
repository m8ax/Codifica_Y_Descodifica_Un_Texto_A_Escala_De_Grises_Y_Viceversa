#################################################################################################################################
#
#  PROGRAMA CREADO POR M8AX - MARCOS OCHOA DIEZ, PARA DESCODIFICAR PIXELES EN ESCALA DE GRISES A TEXTO, PREVIAMENTE HABREMOS
#  USADO EL PROGRAMA PARA CODIFICARLOS, FUNCIONA COMO UN COMPRESOR Y DESCOMPRESOR, AUNQUE TAMBIÉN SIRVE A MODO DE ENCRIPTADO
#  YA QUE EL RESULTADO, SE VE EN FORMA DE PIXELES PINTADOS EN ESCALA DE GRISES, EN EL FICHERO CODIFICADO, OTRA COSA ES DESCIFRARLO
#  A SIMPLE VISTA... xD... EL FICHERO DE ENTRADA ES M8AX-TextoCodificado.PnG Y EL FICHERO DE SALIDA ES Texto_Descodificado.TxT.
#
#  Ejemplo - py m8ax_descodificar_letras.py
#
#################################################################################################################################

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


fichero = open("Texto_Descodificado.TxT", "w", encoding="Latin-1")

os.system("cls")
print("")

imagencodigris = cv2.imread("M8AX-TextoCodificado.PnG")
imagencodigris = cv2.cvtColor(imagencodigris, cv2.COLOR_BGR2GRAY)
wip = imagencodigris.shape[1]
hep = imagencodigris.shape[0]
pixeles = hep * wip
cuenta = 0

if hep > wip:
    cambiando = wip
    wip = hep
    hep = cambiando
else:
    cambiando = hep
    hep = wip
    wip = cambiando

tiembarra = time.time()

while cuenta < pixeles:
    for fila in range(wip):
        for columna in range(hep):
            cuenta = cuenta + 1
            if cuenta > pixeles:
                break
            numpi = imagencodigris[fila, columna]
            fichero.write(chr(numpi))
        barra_progreso_vibrante((fila * columna * 100) / (wip * hep), 100, tiembarra)

barra_progreso_vibrante((wip * hep * 100) / (wip * hep), 100, tiembarra)
fichero.close()
print(
    f"\n\nDescodificación Realizada En {segahms(time.time()-tiembarra)}, A {round(cuenta/(time.time()-tiembarra),3)} Pixeles/Seg."
)
print(
    "\n... Trabajo Realizado Correctamente ...\n\nResultados En El Fichero M8AX-TextoDescodificado.TxT.\n\nBy M8AX..."
)
cv2.imshow("--- M8AX IMAGEN DESCODIFICADA ---", imagencodigris)
cv2.waitKey(0)
cv2.destroyAllWindows()
