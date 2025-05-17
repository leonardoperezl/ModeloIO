import time
from pyomo.environ import *
inicio = time.time()

def definir_modelo():
    """
    Define el modelo de optimización no lineal para la mezcla de alimento
    a partir de un DataFrame con columnas: ["ingredientes", "costo", "proteina", "energia", "calcio"].
    
    Retorna
    -------
    model : ConcreteModel
        Modelo de optimización definido con las variables, restricciones y función objetivo.
    tiempo2 : float
        Tiempo que tomó definir el modelo.
    """
    
    inicio = time.time()
    model = ConcreteModel()
    
    model.x1 = Var(within=NonNegativeReals)
    model.x2 = Var(within=NonNegativeReals)
    model.x3 = Var(within=NonNegativeReals)
    model.x4 = Var(within=NonNegativeReals)
    
    # Definicion de la funciOn objetivo
    model.cost = Objective(expr=6.2 * model.x1 + 11.5 * model.x2 + 18.7 * model.x3 + 40 * model.x4, sense=minimize)
    
    # Definicion de las restricciones
    model.mass_balance = Constraint(expr=model.x1 + model.x2 + model.x3 + model.x4 == 1000)
    
    model.protein = Constraint(expr=0.09 * model.x1 + 0.46 * model.x2 + 0.60 * model.x3 + 0.15 * model.x4 >= 170)
    model.protein_max = Constraint(expr=0.09 * model.x1 + 0.46 * model.x2 + 0.60 * model.x3 + 0.15 * model.x4 <= 200)
    model.energy = Constraint(expr=3350 * model.x1 + 2800 * model.x2 + 2900 * model.x3 + 1500 * model.x4 >= 2800000)
    model.energy_max = Constraint(expr=3350 * model.x1 + 2800 * model.x2 + 2900 * model.x3 + 1500 * model.x4 <= 3000000)
    model.calcium = Constraint(expr=0.0002 * model.x1 + 0.0025 * model.x2 + 0.05 * model.x3 + 0.15 * model.x4 >= 32)
    model.calcium_max = Constraint(expr=0.0002 * model.x1 + 0.0025 * model.x2 + 0.05 * model.x3 + 0.15 * model.x4 <= 45)
    model.non_linear = Constraint(expr=model.x3 <= (model.x1 + model.x2 + 1e-5)**0.5)
    
    # Imprimir mensaje de confirmacion
    print("Modelo definido correctamente")
    final = time.time()
    tiempo2 = final - inicio
    
    return model, tiempo2