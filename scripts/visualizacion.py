import matplotlib.pyplot as plt
import pandas as pd
from pyomo.environ import value

def visualizar_resultados(modelo, datos, tiempos):
    try:
        resultados = pd.DataFrame({
            "Ingrediente": ["Semillas de trigo", "Semillas de sandia", "Semillas de calabaza", "Estofado sospechoso"],
            "Cantidad (kg)": [value(modelo.x1), value(modelo.x2), value(modelo.x3), value(modelo.x4)],
            "Porcentaje (%)": [value(modelo.x1)/10, value(modelo.x2)/10, value(modelo.x3)/10, value(modelo.x4)/10],
            "Costo Total ($)": [value(modelo.x1)*6.2, value(modelo.x2)*11.5, value(modelo.x3)*18.7, value(modelo.x4)*40]
        })
        
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        labels = resultados["Ingrediente"]
        sizes = resultados["Cantidad (kg)"]
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
        plt.title("Composicion de la mezcla optima")
        plt.axis("equal")
        
        plt.subplot(1, 3, 2)
        plt.bar(resultados["Ingrediente"], resultados["Costo Total ($)"], color="#4682B4")
        plt.title("Costo total por ingrediente")
        plt.ylabel("Costo ($)")
        plt.xticks(rotation=45)
        
        plt.subplot(1, 3, 3)
        etapas = ["Cargar datos", "Definir modelo", "Resolver modelo", "Guardar resultados"]
        plt.bar(etapas, [tiempos["tiempo1"], tiempos["tiempo2"], tiempos["tiempo3"], tiempos["tiempo4"]], color="#76D7C4")
        plt.title("Tiempos de ejecucion por etapa")
        plt.ylabel("Segundos")
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        print(f"Graficas generadas correctamente")
    
    except Exception as e:
        print("Error al generar las graficas:", e)
        raise