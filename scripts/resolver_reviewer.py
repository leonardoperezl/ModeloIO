from scipy.optimize import minimize
import numpy as np
import pandas as pd


def feedmix_model_solver(df: pd.DataFrame) -> dict:
    """
    Resuelve el modelo de optimizacion no lineal para la mezcla de alimento
    a partir de un DataFrame con columnas: ["ingredientes", "costo", "proteina", "energia", "calcio"].
    
    Parametros
    ----------
        df : pd.DataFrame
            DataFrame con informacion nutricional y de costos por ingrediente
    
    Retorna
    -------
        dict
            Resultados optimos o mensaje de error
    """
    # Extraer los coeficientes del dataframe
    cost = df["costo"].values
    protein = df["proteina"].values
    energy = df["energia"].values
    calcium = df["calcio"].values
    
    # Funcion objetivo
    def total_cost(x):
        return np.dot(cost, x)
    
    # Restricciones lineales y no lineales
    def min_protein(x): return np.dot(protein, x) - 170
    def max_protein(x): return 200 - np.dot(protein, x)
    def min_energy(x): return np.dot(energy, x) - 2800000
    def max_energy(x): return 3000000 - np.dot(energy, x)
    def min_calcium(x): return np.dot(calcium, x) - 32
    def max_calcium(x): return 45 - np.dot(calcium, x)
    def mass_balance(x): return 1000 - sum(x)
    def nl_constraint(x): return np.sqrt(x[0] + x[1]) - x[2]  # x3 \leq \sqrt(x_1 + x_2)
    
    constraints = [
        {"type": "ineq", "fun": min_protein},
        {"type": "ineq", "fun": max_protein},
        {"type": "ineq", "fun": min_energy},
        {"type": "ineq", "fun": max_energy},
        {"type": "ineq", "fun": min_calcium},
        {"type": "ineq", "fun": max_calcium},
        {"type": "eq",   "fun": mass_balance},
        {"type": "ineq", "fun": nl_constraint},
    ]
    
    bounds: list[tuple[float]] = [(0, 1000)] * 4
    x0: list[int] = [250] * 4
    
    result = minimize(total_cost, x0, method="SLSQP", bounds=bounds, constraints=constraints)
    
    if result.success:
        solucion = {nombre: result.x[i] for i, nombre in enumerate(df["ingredientes"])}
        solucion["Costo total"] = result.fun
    else:
        solucion = {"error": result.message}
    
    return solucion


if __name__ == "__main__":
    # Probar usando un DataFrame equivalente a ingredientes.csv
    df_prueba = pd.DataFrame({
        "ingredientes": ["trigo", "sandia", "calabaza", "estofado"],
        "costo": [6.2, 11.5, 18.7, 40],
        "proteina": [0.09, 0.46, 0.60, 0.15],
        "energia": [3350, 2800, 2900, 1500],
        "calcio": [0.0002, 0.0025, 0.05, 0.15]
    })
    
    print(feedmix_model_solver(df_prueba))