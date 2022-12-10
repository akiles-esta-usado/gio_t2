from pathlib import Path
import pandas as pd


def get_data(data_path: Path):
  alpha_i_path = data_path / "alpha_i.csv"
  if not alpha_i_path.exists():
    RuntimeError("El archivo alpha_i.csv no existe :(")

  beta_j_path = data_path / "beta_j.csv"
  if not beta_j_path.exists():
    RuntimeError("El archivo beta_j.csv no existe :(")

  a_ij_path = data_path / "a_ij.csv"
  if not a_ij_path.exists():
    RuntimeError("El archivo a_ij.csv no existe :(")


  alpha_i = pd.read_csv(alpha_i_path, header=None).to_numpy() # Oferta de nodo origen
  beta_j = pd.read_csv(beta_j_path, header=None).to_numpy()   # Demanda de nodo destino
  a_ij = pd.read_csv(a_ij_path, header=None).to_numpy()

  I = [i for i in range(len(alpha_i))] # N=20, Conjunto de origenes, quienes ofrecen
  J = [j for j in range(len(beta_j))]  # M=30, Conjunto de destinos, quienes demandan

  return I, J, alpha_i, beta_j, a_ij
