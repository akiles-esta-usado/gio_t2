import numpy as np
from numpy.typing import NDArray

def simplex_normalization(A: NDArray, entra: int, sale: int):
  A = A.copy()
  
  view_columna = A[:, entra]
  view_fila    = A[sale, :]


  view_fila /= A[sale, entra]
  
  AD = np.ones(shape=A.shape)

  escala = -view_columna
  for idx, value in enumerate(escala):
    AD[idx, :] = value*view_fila

  AD[sale, :] = 0 # Evita los cambios en fila donde está A[sale, entra]

  A = A + AD
  return A


def north_west_heuristic(oferta_i: NDArray, demanda_j: NDArray, costos_ij: NDArray):
  if oferta_i.sum() != demanda_j.sum():
    raise ValueError("Oferta != Demanda")
  
  oferta_i = oferta_i.copy()
  demanda_j = demanda_j.copy()

  factores_ij = np.zeros(shape=costos_ij.shape)

  i = 0
  j = 0

  while True:

    oferta_actual = oferta_i[i,0]
    demanda_actual = demanda_j[j,0]

    print(f"{   oferta_actual = }")
    print(f"{   demanda_actual = }")

    if oferta_actual == demanda_actual:
      print("   - iguales")
      factores_ij[i,j] = oferta_actual
      
      oferta_i[i,0] -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 1
      
    elif oferta_actual >= demanda_actual:
      print("   - demanda_actual es menor")
      factores_ij[i,j]=demanda_actual

      oferta_i[i,0]  -= demanda_actual
      demanda_j[j,0] -= demanda_actual

      di = 0
      dj = 1


    elif oferta_actual <= demanda_actual:
      print("   - oferta_actual es menor")
      factores_ij[i,j]=oferta_actual

      oferta_i[i,0]  -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 0

    if oferta_i[i,0] == 0 and demanda_j[j,0] == 0:
      print("Se llega al equilibrio")
      return factores_ij
    
    print(oferta_i)
    print(demanda_j)
    i += di
    j += dj

    print()


