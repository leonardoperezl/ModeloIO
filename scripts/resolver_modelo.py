import time
from pyomo.opt import SolverFactory
import pandas as pd
inicio1 = time.time()

def resolver_modelo(modelo):
    inicio1 = time.time()
    solver = SolverFactory('ipopt')
    resultado = solver.solve(modelo)

    print("Modelo resuelto correctamente")
    print(f"Valor de la función objetivo: ${round(modelo.cost(), 2)}")
    final1 = time.time()
    tiempo3 = final1 - inicio1
    return resultado, tiempo3


def guardar_resultados(modelo, ruta_csv='resultados/solucion.csv'):
    inicio2 = time.time()
    resultados = pd.DataFrame({
        'Ingrediente': ['Semillas de trigo', 'Semillas de sandia', 'Semillas de calabaza', 'Estofado sospechoso'],
        'Cantidad (kg)': [round((modelo.x1.value), 2), round((modelo.x2.value), 2), 
                          round((modelo.x3.value), 2), round((modelo.x4.value), 2)],
        'Costo Total ($)': [f'${round((modelo.x1.value * 6.2), 2)}', f'${round((modelo.x2.value * 11.5), 2)}', 
                            f'${round((modelo.x3.value * 18.7), 2)}', f'${round((modelo.x4.value * 40), 2)}']

    })

    with open(ruta_csv, 'w', newline='') as file:
        file.write(f"{'Ingrediente':<25}{'Cantidad (kg)':<15}{'Costo Total ($)':<15}\n")
        
        for index, row in resultados.iterrows():
            file.write(f"{row['Ingrediente']:<25}{row['Cantidad (kg)']:<15}{row['Costo Total ($)']:<15}\n")

        file.write("\n\n\n")
        file.write(f"{'Funcion Objetivo ($)':<25}{'':<15}{f'${round(modelo.cost(), 2)}':<15}\n")

    print(resultados)
    print(f"Resultados guardados en '{ruta_csv}'")
    final2 = time.time()
    tiempo4 = final2 - inicio2
    return tiempo4

