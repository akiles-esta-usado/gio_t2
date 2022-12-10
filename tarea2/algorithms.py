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

    # print(f"{   oferta_actual = }")
    # print(f"{   demanda_actual = }")

    if oferta_actual == demanda_actual:
      # print("   - iguales")
      factores_ij[i,j] = oferta_actual
      
      oferta_i[i,0] -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 1
      
    elif oferta_actual >= demanda_actual:
      # print("   - demanda_actual es menor")
      factores_ij[i,j]=demanda_actual

      oferta_i[i,0]  -= demanda_actual
      demanda_j[j,0] -= demanda_actual

      di = 0
      dj = 1


    elif oferta_actual <= demanda_actual:
      # print("   - oferta_actual es menor")
      factores_ij[i,j]=oferta_actual

      oferta_i[i,0]  -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 0

    if oferta_i[i,0] == 0 and demanda_j[j,0] == 0:
      # print("Se llega al equilibrio")
      return factores_ij
    
    # print(oferta_i)
    # print(demanda_j)
    i += di
    j += dj

    # print()


def costos_reducidos(idx_B: NDArray, idx_NB: NDArray, A: NDArray, c: NDArray) -> NDArray:
  c_B = c[idx_B]
  A_B = A[:, idx_B]
  c_NB = c[idx_NB]
  A_NB = A[:, idx_NB]
  
  return c_NB - np.linalg.multi_dot( [c_B,  np.linalg.inv(A_B) , A_NB])



def es_factible(X_B):
  return (X_B >= 0).all()

def es_optimo(cr):

  if (cr >= 0).all():
    print("Tenemos un óptimo")

    if (cr == 0).any():
      print("Son múltiples óptimos")
    else:
      print("Es único")

    return True

  return False

def direccion_costo_reducido(X: NDArray, A: NDArray, B:NDArray, NB: NDArray, c: NDArray, NB_i: int) -> NDArray:
  d = np.zeros(shape=X.shape)
  d_B = - np.dot(
    np.linalg.inv(A[:,B]),
    A[:, NB_i]
  )

  np.put(d, NB_i, 1)
  np.put(d, B, d_B)


  cr = c[NB_i] + np.dot(c[B].T, d[B])

  # i, d, cr
  return NB_i, d, cr.flatten()

def lista_direccion_costos_reducidos(X: NDArray, A: NDArray, c: NDArray, B:NDArray, NB: NDArray) -> NDArray:

  d_cr_list = list()

  for NB_i in NB:
    d = np.zeros(shape=X.shape)
    d_B = - np.dot(
      np.linalg.inv(A[:,B]),
      A[:, NB_i]
    )

    np.put(d, NB_i, 1)
    np.put(d, B, d_B)


    cr = c[NB_i] + np.dot(c[B].T, d[B])

    d_cr_list.append((NB_i, d, cr.flatten()))

  return d_cr_list