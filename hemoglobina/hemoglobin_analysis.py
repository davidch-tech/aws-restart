
import os
import json

'''Este script analiza el archivo 'hemoglobin_clean.txt' para contar el número total de caracteres que contiene.'''

def get_base_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 1. Leer y parsear el archivo FASTA
    with open(os.path.join(script_dir, 'hemoglobin_seq.txt'), 'r') as f:
        lines = f.readlines()
    header = ""
    sequence = ""
    for line in lines:
        if line.startswith(">"):
            header = line.strip()[1:]       # quita el ">"
        else:
            sequence += line.strip()        # acumula líneas de secuencia

    # 2. Separar id y nombre del encabezado
    protein_id, protein_name = header.split(" ", 1)
    # 3. Armar el diccionario por tipo
    data = {
        "metadata": {
            "id": protein_id,
            "name": protein_name
        },
        "sequence": {
            "raw": sequence,
            "length": len(sequence)
        }
    }

    return data

def get_amino_acid_list():
    """Devuelve la lista de los 20 aminoácidos estándar
    representados por su código de una letra.

    La lista proviene de la bioquímica estándar (IUPAC).
    Cada letra corresponde a un aminoácido:
        A=Ala  R=Arg  N=Asn  D=Asp  C=Cys
        E=Glu  Q=Gln  G=Gly  H=His  I=Ile
        L=Leu  K=Lys  M=Met  F=Phe  P=Pro
        S=Ser  T=Thr  W=Trp  Y=Tyr  V=Val
    """
    amino_acids = [
        'A', 'R', 'N', 'D', 'C',
        'E', 'Q', 'G', 'H', 'I',
        'L', 'K', 'M', 'F', 'P',
        'S', 'T', 'W', 'Y', 'V'
    ]
    return amino_acids

def get_hidrophobic_list():
    """Devuelve la lista de aminoácidos hidrofóbicos representados por su código de una letra."""
    hydrophobic_amino_acids = ['A', 'I', 'L', 'M', 'F', 'W', 'Y', 'V']
    return hydrophobic_amino_acids

def get_molecular_weights():
    """Retorna diccionario con pesos moleculares (g/mol) de los 20 aminoácidos estándar."""
    weights = {
        "A": 89.09,  "R": 174.20, "N": 132.12, "D": 133.10, "C": 121.16,
        "E": 147.13, "Q": 146.15, "G": 75.03,  "H": 155.16, "I": 131.17,
        "L": 131.17, "K": 146.19, "M": 149.21, "F": 165.19, "P": 115.13,
        "S": 105.09, "T": 119.12, "W": 204.23, "Y": 181.19, "V": 117.15
    }
    return weights
def calculate_molecular_weight(sequence):
    """calcula el peso molecular total de la secuencia dada sumando los pesos moleculares de cada aminoácido presente en la secuencia."""
    weights = get_molecular_weights()
    total = 0
    for aa in sequence:
        if aa in weights:
            total += weights[aa]
    return total

def calculate_composition(sequence):
    """cuenta cuantas veces aparece cada aminoácido en la secuencia dada."""
    #obtenemos la lista de aminoácidos para inicializar el diccionario de composición
    amino_acids = get_amino_acid_list()
    #inicializamos el diccionario de composición con 0 para cada aminoácido
    composition = {}
    # creamos un for para contar cada aminoácido en la secuencia iterando sobre cada letra de la secuencia
    ## aa es la letra del aminoácido actual en la iteración
    for aa in sequence:
        ## contamos cuántas veces aparece el aminoácido actual en la secuencia usando el método count() de las cadenas de texto
        count = sequence.count(aa)
        ## guardamos el resultado en el diccionario de composición usando la letra del aminoácido como clave y el conteo como valor
        composition[aa] = count
    # ordenamos el diccionario de composición por la cantidad de aminoácidos en orden descendente usando sorted() y una función lambda como clave de ordenamiento
    composition = dict(sorted(composition.items(), key=lambda item: item[1], reverse=True))
    return composition

def build_result(protein_name, length, composition, mol_weight):
    """Construye un diccionario con los resultados del análisis de la secuencia de hemoglobina."""
    return {
        "protein_name": protein_name,
        "length": length,
        "amino_acid_count": composition,
        "molecular_weight": mol_weight
    }

def save_results(data, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def get_percentage_composition(secuence):
    """Calcula el porcentaje de cada aminoácido en la secuencia dada la composición y la longitud total."""
    hydrophobic_amino_acids = get_hidrophobic_list()
    secuence_composition = {}
    count = 0
    # iteramos sobre cada aminoácido hidrofóbico para contar cuántas veces aparece en la secuencia usando el método count() de las cadenas de texto
    for aa in hydrophobic_amino_acids:
        # sumamos el conteo de cada aminoácido hidrofóbico a la variable count para obtener el total de aminoácidos hidrofóbicos en la secuencia
        count += secuence.count(aa)
        print(f"El aminoácido {aa} aparece {secuence.count(aa)} veces en la secuencia.")
    percentage = (count / len(secuence)) * 100
    return percentage


def print_lines (number=int,text=""):
    """Imprime una línea de separación para mejorar la legibilidad de la salida."""
    if text == "":
        print("-" * number)
    else:
        print("-" * number)
        print(text)
        print("-" * number)
                

if __name__ == "__main__":
    print_lines(50,"Analizando el archivo 'hemoglobin_seq.txt' para obtener datos básicos...")
    result = get_base_data()
    print_lines(50,json.dumps(result, indent=4))
    print_lines(50,"json obtenido del análisis del archivo 'hemoglobin_seq.txt'")
    print_lines(50,"Calculando la composición de aminoácidos en la secuencia...")
    composition = calculate_composition(result["sequence"]["raw"])
    print_lines(50,json.dumps(composition, indent=4))
    mol_weight = calculate_molecular_weight(result["sequence"]["raw"])
    print(mol_weight)
    final_data = build_result(result["metadata"]["name"], result["sequence"]["length"], composition, mol_weight)
    save_results(final_data, "hemoglobin_analysis_result.json")
    print_lines(50,"Resultado final del análisis de la secuencia de hemoglobina:")
    pct = get_percentage_composition(result["sequence"]["raw"])   
    print_lines(50, f"Porcentaje hidrofóbicos: {pct:.2f}%")