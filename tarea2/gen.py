import pandas as pd
from pathlib import Path
import numpy as np
from numpy.typing import NDArray

def gen_A(I: list, J: list):

  I_N = len(I)
  J_N = len(J)

  # Mapea entre una restricción X_ij a un índice de la matriz A.
  IJ = np.arange(I_N*J_N).reshape(I_N, J_N)

  A = np.zeros(shape=(I_N + J_N, I_N * J_N))

  # Cada fila de la matriz A representa una restricción de igualdad.
  restriccion_base = 0

  # Por cada nodo fuente i
  # la suma de demanda de cada destino debe igualar a su oferta
  for i in I:
    for j in J:
      A[restriccion_base][IJ[i, j]] = 1

    restriccion_base += 1

  # Por cada nodo destino j
  # Su demanda debe ser satisfecha por todos los nodos
  for j in J:
    for i in I:
      A[restriccion_base][IJ[i, j]] = 1

    restriccion_base += 1

  return A

def gen_b(oferta_i, demanda_j):
  return np.append(oferta_i,  demanda_j)


def gen_mapping(I, J):
  I_N = len(I)
  J_N = len(J)

  return np.arange(I_N*J_N).reshape(I_N, J_N)