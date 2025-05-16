"""
Modulo creado para cargar y validar los datos base para resolver el problema.
Los datos oficiales del problema se encuentran en el archivo 
"datos/ingredientes.csv". En la misma carpeta se encuentran archivos de ejemplo
"datos/ejemplo_1.csv" y "datos/ingredientes_ejemplo_2.csv" que pueden ser
utilizados para probar el funcionamiento del modulo (y de otros modulos) sin
necesidad de descargar los datos oficiales. 

> **Nota 1**. Para ver más información sobre el problema, leer el archivo
"README.md" en el directorio raíz del proyecto, en la sección "Descripción del
problema".

> **Nota 2**. Para ver más información los archivos de ejemplo, leer el archivo
"README.md" en el directorio raíz del proyecto, en la sección "Ejemplos de uso".
"""

from pathlib import Path

import pandas as pd
import numpy as np

type DataPath = str | Path


class DataPathDescriptor:
    """
    Descriptor para la ruta de los datos. Se utiliza para validar que la ruta
    proporcionada es un archivo CSV y que existe en el sistema de archivos.
    """
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value: DataPath):
        if not isinstance(value, (str, Path)):
            raise TypeError("La ruta debe ser una cadena o un objeto Path.")
        
        if not value.endswith(".csv"):
            raise ValueError("La ruta debe terminar con '.csv'.")
        
        if not Path(value).exists():
            raise FileNotFoundError(f"El archivo {value} no existe.")
        
        instance.__dict__[self.name] = value


class DataDataFrameDescriptor:
    """
    Descriptor para el DataFrame. Se utiliza para validar que el DataFrame
    proporcionado es válido y contiene las columnas necesarias. En caso de que
    una columna tenga un nombre similar, se estandariza.
    """
    
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value: pd.DataFrame):
        df: pd.DataFrame = value  # Inicio del error principal
        
        # Palabras clave y sus validaciones de rango asociadas
        required_columns: dict[str, None | tuple] = {
            "ingredientes": None,  # Solo verificar presencia, tipo string
            "costo": (0, float("inf")),
            "proteina": (0, 100),
            "energia": (0, float("inf")),
            "calcio": (0, 100),
        }
        
        renamed_columns = {}
        obtained_columns = df.columns.tolist()
        
        # Renombrar columnas segun palabras clave
        for column, _ in required_columns.items():
            found: bool = False
            
            for col in obtained_columns:
                if column in col.lower():
                    renamed_columns[col] = column
                    found = True
                    break
            
            if not found:
                raise ValueError(
                    f"No se encontro ninguna "
                    f"columna correspondiente a: '{column}'"
                )
        
        print(f"Las columnas obtenidas son: {obtained_columns}")
        print(f"Las columnas renombradas son: {renamed_columns}")
        
        df = df.rename(columns=renamed_columns)
        
        # Validar que no existan nulos en las columnas requeridas
        for column in required_columns:
            if not df[column].isnull().any():
                continue
            
            raise ValueError(f"La columna '{column}' contiene valores nulos.")
        
        # Validar tipos y rangos
        for column, range in required_columns.items():
            if column == "ingredientes":
                continue
            
            column_s: pd.Series = df[column].astype("float32")
            min_val, max_val = range
            
            if not column_s.between(min_val, max_val).all():
                raise ValueError(
                    f"La columna '{column}' contiene valores "
                    f"fuera del rango permitido ({min_val}-{max_val})."
                )
        
        print(f"Las columnas del valor inicial son: {value.columns.tolist()}")
        
        # Error: `df` es ahora el valor corregido, pero no se asigna
        # correctamente al atributo de la instancia.
        instance.__dict__[self.name] = value 


class ProblemData:
    path: DataPath = DataPathDescriptor()
    df: pd.DataFrame = DataDataFrameDescriptor(
        required_columns=[
            "ingredientes",
            "costo",
            "proteina",
            "energia",
            "calcio"
        ]
    )
    
    NA_VALUES: list[str] = ["", " ", "NA", "N/A", "n/a", "na"]
    
    _csv_lecture_params: dict = {
        "na_values": NA_VALUES,
        "keep_default_na": True,
        "skip_blank_lines": True,
        "low_memory": False
    }
    
    def __init__(self, path: DataPath) -> None:
        self.path: DataPath = path
        self.df: pd.DataFrame = (
            pd.read_csv(self.path, **self._csv_lecture_params)
        )
        self.normalize_data()
    
    def normalize_data(self) -> pd.DataFrame:
        """
        Normaliza los datos del DataFrame. Las columnas que almacenan texto se
        convierten a minúsculas y se eliminan los espacios en blanco al inicio y
        al final de la cadena. Las columnas que almacenan números se convierten a
        números flotantes.
        
        Retorna
        -------
        pd.DataFrame
            El DataFrame normalizado.
        """
        
        text_columns: list[str] = ["ingredientes"]
        numeric_columns: list[str] = ["costo", "proteina", "energia", "calcio"]
        
        for column in text_columns:
            self.df[column] = (
                self.df[column]
                .astype("string")
                .str.lower()
                .str.strip()
            )
        
        for column in numeric_columns:
            self.df[column] = (
                self.df[column]
                .astype("string")
                .str.replace(",", ".", regex=False)
                .str.strip()
                .astype("float32")
                .round(2)
            )
        
        # Eliminar filas con valores duplicados en "ingredientes"
        self.df = self.df.drop_duplicates(subset=["ingredientes"])
        
        return self.df


def download_data(path: DataPath, output_format: str = "dataframe") -> pd.DataFrame | np.ndarray | list[list]:
    """
    Descarga los datos del archivo CSV y los carga en un DataFrame.
    
    Parametros
    ----------
    path : str or Path
        La ruta del archivo CSV.
    
    output_format : str, default "dataframe"
        El formato de salida. Puede ser "dataframe", "matrix" o "list".
        - "dataframe": Devuelve un DataFrame.
        - "matrix": Devuelve una matriz NumPy.
        - "list": Devuelve una lista de listas.
    
    Retorna
    -------
    pd.DataFrame
        El DataFrame con los datos del archivo CSV.
    """
    
    data = ProblemData(path).normalize_data()
    
    if output_format == "matrix":
        return data.to_numpy()
    elif output_format == "list":
        return data.values.tolist()
    
    return data


if __name__ == "__main__":
    # Ejemplo de uso
    path = "../datos/ingredientes.csv"
    
    try:
        data = download_data(path)
        print(data)
    except Exception as e:
        print(f"Error: {e}")