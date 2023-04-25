# -*- coding: utf-8 -*-
"""Untitled22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wjBILQe0ePUidIcJ_GOMgQfbI6fK6t4P
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import concurrent.futures

"""# Simulacion

"""

def simulacion(jugadores, probabilidades, album_completo) -> tuple[int, int, int]:

        #variables para el punto 1 del pc
        
        compra = 0
        frec_hasta_prim_rep = 0
        switch_primera_repetida = False
        frec_laminas_rep = 0

        #Se crea un set que actuará como álbum. Cuando el número de elementos del set sea igual que la longitud de las cartas, ya se habrá completado el álbum
        album = set()
        
        while len(album) != album_completo:

            #Se escoje una lamina alaeatoria basada en la probabilidad
            lamina = np.random.choice(jugadores, p = probabilidades)

            #se llama al método que trabaja la frecuencia de a las cuantas láminas sale la primera repetida
            if not(switch_primera_repetida):
                frec_hasta_prim_rep, switch_primera_repetida = frec_hasta_la_primera_repetida(frec_hasta_prim_rep, lamina, album, switch_primera_repetida)

            #se llama al método que trabaja la frecuencia de láminas repetidas
            frec_laminas_rep = frec_laminas_repetidas(frec_laminas_rep, lamina, album)

            #se suma 1 a la compra total de laminas para llenar el álbum
            compra += 1

            #Se marca la lamina como obtenida en el álbum
            album.add(lamina)

            #Se ejecutan los casos para el inciso 2 del pc
        
      
        return compra, frec_hasta_prim_rep, frec_laminas_rep

def frec_hasta_la_primera_repetida(frec: int, lamina: str, set_laminas: set, repetida: bool) -> list[int, bool]:

  #se suma 1 a la frecuencia total
  frec += 1

  #si la lamina sacada ya se encuentra en el set, entonces se ha hallado la primera repetida
  if lamina in set_laminas:
    repetida = True

  return frec, repetida

def frec_laminas_repetidas(frec: int, lamina: str, set_laminas: set) -> int:

  #si la lamina ya se encuentra en el set, se le summa 1 a la frecuencia de repetidas
  if lamina in set_laminas:
    frec += 1

  return frec 

def graficar_histograma(datos: list, grafica: int) -> None:

    # Calcular el histograma
    hist, bins = np.histogram(datos)

    # Calcular la moda, media y mediana
    moda = stat.mode(datos)
    media = np.round(np.mean(datos), 2)
    mediana = np.round(np.median(datos), 2)

    # Graficar el histograma
    plt.hist(datos, bins=bins, alpha=0.7, color='blue')
    plt.xlabel('Intervalos de frecuencias')
    plt.ylabel('Cantidad')
  
    if grafica == 1:
      plt.title('Frecuencia # de láminas que debe comprar')

    if grafica == 2:
      plt.title('Frecuencia de a las cuántas láminas sale la primera repetida')

    if grafica == 3:
      plt.title('Frecuencia # de láminas repetidas')

    plt.axvline(moda, color='red', linestyle='dashed', linewidth=2, label=f'Moda: {moda}')
    plt.axvline(media, color='green', linestyle='dashed', linewidth=2, label=f'Media: {media}')
    plt.axvline(mediana, color='purple', linestyle='dashed', linewidth=2, label=f'Mediana: {mediana}')
    plt.legend()
    plt.show()
    print("")

"""# Multiprocesamiento"""
def main() -> None:
  
    #Se lee el csv 
    df = pd.read_csv('World_Cup_players_Dataset_World_Cup_players_Dataset_csv.csv') 

    #Se seleccionan las columnas de interés
    df = df[["Player", "Probability", "National team"]]

    """# Pre Proccessing"""

    df[df["Probability"].isna()]

    df.loc[20,['Player','Probability', "National team"]] = ["Neymar Jr.", 0.005264696306, "Brazil"]
    df.loc[26,['Player','Probability', "National team"]] = ["Tite", 0.002783684881, "Brazil"]

    df["Probability"] = df["Probability"] / df["Probability"].sum()
    df.to_csv('datos_limpios.csv', index=False)

    df = pd.read_csv('datos_limpios.csv')
    nucleos = 4
    simulaciones = 10
    jugadores = df["Player"]
    probabilidades = df['Probability']
    album_completo = df.shape[0]

    with ProcessPoolExecutor(max_workers = nucleos) as executor:
      
        futures = [executor.submit(simulacion, jugadores, probabilidades, album_completo) for _ in range(simulaciones)]
        
        grafica_1 = []
        grafica_2 = []
        grafica_3 = []
        
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f"Error: {e}")
            else:
                print(f"Result: {result}")
                
                grafica_1.append(result[0])
                grafica_2.append(result[1])
                grafica_3.append(result[2])
        
        graficar_histograma(grafica_1, 1)
        graficar_histograma(grafica_2, 2)
        graficar_histograma(grafica_3, 3)
        
        print('\n ¿Cuántas láminas deberá comprar para llegar a obtener todos y cada uno de los cupones?')
        print(f"\n Se necesitarán comprar en promedio {np.round(np.mean(grafica_1), 2)} láminas")

if __name__ == "__main__":
  
  main()

