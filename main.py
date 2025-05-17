from scripts.carga_datos import download_data
from scripts.definir_modelo import definir_modelo
from scripts.resolver_modelo import resolver_modelo, guardar_resultados
from scripts.visualizacion import *

print("------------------------------------ @ Datos @ ------------------------------------")
datos, tiempo1 = download_data("datos/ingredientes.csv")
print("------------------------------- @ Modelo definido @ -------------------------------")
modelo, tiempo2 = definir_modelo()
print("---------------------------- @ Resolución del modelo @ ----------------------------")
resultado, tiempo3 = resolver_modelo(modelo)
print("---------------------------------- @ Resultados @ ---------------------------------")
tiempo4 = guardar_resultados(modelo)
print("----------------------------- @ Tiempos de ejecucion @ ----------------------------")
print(f"El tiempo de cargar_datos() es:       {tiempo1}")
print(f"El tiempo de definir_modelo() es:     {tiempo2}")
print(f"El tiempo de resolver_modelo() es:    {tiempo3}")
print(f"El tiempo de guardar_resultados() es: {tiempo4}\n")
print(f"El tiempo de total es:                {tiempo1 + tiempo2 + tiempo3 + tiempo4}")
print("------------------------- @ Visualización de Resultados @ -------------------------")
visualizar_resultados(modelo, datos, {
    "tiempo1": tiempo1,
    "tiempo2": tiempo2,
    "tiempo3": tiempo3,
    "tiempo4": tiempo4
})

print("------------------------------- @ Proceso exitoso @ -------------------------------")
