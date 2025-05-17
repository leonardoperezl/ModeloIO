from scipy.optimize import minimize
import numpy as np
import pandas as pd


# Funcion para probar el modelo
def test_constraints(df: pd.DataFrame, x: list[float]) -> dict:
    """
    Evalua si una combinacion especifica de ingredientes cumple todas las restricciones del modelo.
    
    Parametros
    ----------
    df : pd.DataFrame
        DataFrame con columnas ["ingredientes", "costo", "proteina", "energia", "calcio"]
    x : list[float]
        Lista con las cantidades en kg de cada ingrediente [x1, x2, x3, x4]
    
    Retorna
    -------
    dict
        Resultado indicando si cumple o no cada restriccion
    """
    protein = df["proteina"].values
    energy = df["energia"].values
    calcium = df["calcio"].values
    
    results = {
        "Balance de masa": np.isclose(sum(x), 1000),
        "Proteina minima (17%)": np.dot(protein, x) >= 170,
        "Proteina maxima (20%)": np.dot(protein, x) <= 200,
        "Energia minima (2800 kcal/kg)": np.dot(energy, x) >= 2800000,
        "Energia maxima (3000 kcal/kg)": np.dot(energy, x) <= 3000000,
        "Calcio minimo (3.2%)": np.dot(calcium, x) >= 32,
        "Calcio maximo (4.5%)": np.dot(calcium, x) <= 45,
        "Restriccion no lineal (x3 \leq \sqrt{x1 + x2})": x[2] <= np.sqrt(x[0] + x[1]),
    }
    
    return results


def feedmix_model_solver(df: pd.DataFrame, x0: list[float] | None = None) -> dict:
    """
    Resuelve el modelo de optimizacion no lineal para la mezcla de alimento
    a partir de un DataFrame con columnas: ["ingredientes", "costo", "proteina", "energia", "calcio"].
    
    Parametros
    ----------
    df : pd.DataFrame
        DataFrame con informacion nutricional y de costos por ingrediente
    
    x0 : list[float]
        Lista con las cantidades iniciales en kg de cada ingrediente [x1, x2, x3, x4]
        (debe ser de la misma longitud que el numero de ingredientes en df)
    
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
    x0: list[int] = [250] * 4 if x0 is None else x0
    
    # Probar las restricciones iniciales
    initial_test = test_constraints(df, x0)
    
    if not all(initial_test.values()):
        return {"error": "La mezcla inicial no cumple con las restricciones."}
    
    result = minimize(total_cost, x0, method="SLSQP", bounds=bounds, constraints=constraints)
    
    if result.success:
        solucion = {nombre: f"{result.x[i]:,.2f}" for i, nombre in enumerate(df["ingredientes"])}
        solucion["Costo total"] = f"{result.fun:,.2f}"
    else:
        solucion = {"error": result.message}
    
    return solucion


if __name__ == "__main__":
    # Probar usando un DataFrame equivalente a ingredientes.csv
    ingredientes_base = pd.DataFrame({
        "ingredientes": ["trigo", "sandia", "calabaza", "estofado"],
        "costo": [6.2, 11.5, 18.7, 40],
        "proteina": [0.09, 0.46, 0.60, 0.15],
        "energia": [3350, 2800, 2900, 1500],
        "calcio": [0.0002, 0.0025, 0.05, 0.15]
    })
    
    mixes = {
        "Solo trigo (1000 kg)": [1000, 0, 0, 0],
        "Violacion raiz cuadrada (x3 = 20 > \\sqrt(100 + 100))": [100, 100, 20, 780],
        "Mezcla razonable ajustada": [400, 250, 100, 250]
    }
    
    for case in mixes:
        print(f"Probando caso: {case}")
        x0 = mixes[case]
        resultado = feedmix_model_solver(ingredientes_base, x0)
        print("Resultado:", resultado)
        print("-" * 40)