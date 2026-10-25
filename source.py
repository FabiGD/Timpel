# Prova de Selecao - Timpel
# Vaga: Analista de Desenvolvimento I
# Autora: Fabiana Gomes Diniz 

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import errno

# Defines the number of decimal places displayed by pandas
pd.set_option('display.float_format', '{:.15f}'.format)

def data_validation_and_opt_PEEP_identification(hyperdistension, PEEP, collapse):
    """
    Validates data and identifies the ideal PEEP value given 
    the collapse and hyperdistension values of the respiratory system.

    Args:
        hyperdistension (pandas Series): Hyperdistension values.
        PEEP (pandas Series): PEEP values.
        collapse (pandas Series): Collapse values.

    Returns:
        opt_PEEP (array): Array with the possible optimal points found; 
        if the number of points is different from 1, they will not be displayed on the graph.
    """

    # Checks dimentions
    if not len(PEEP) == len(collapse) == len(hyperdistension):
        raise ValueError("All inputs must have the same length.")
    
    if PEEP.ndim != 1 or collapse.ndim != 1 or hyperdistension.ndim != 1:
        raise ValueError("All inputs must be one-dimensional.")

    # Checks for missing or non-finite values
    if not (np.isfinite(PEEP).all() and np.isfinite(collapse).all() and np.isfinite(hyperdistension).all()):
        raise ValueError("Inputs cannot contain NaN or infinite values.")
    
    # Checks if PEEP steps are in descending order
    if not np.all(np.diff(PEEP.to_numpy(dtype=float)) < 0):
        raise ValueError("PEEP steps must be in descending order.")
    
    # Checks if there is less than two samples
    if len(hyperdistension) < 2:
        raise ValueError("More than one sample is needed to identify PEEP.")
    
    # Difference between the curves
    difference = hyperdistension - collapse

    # Creates a list to store the crossind indices
    crossing_idx = []

    for i in range(len(difference) - 1):

        # If the difference is equal to zero and it is not the first step, 
        # the intersection is associated with the previous step.
        if difference[i] == 0 and i > 0:
            crossing_idx.append(i - 1)

        # If a sign change has occurred, then the previous index precedes the intersection
        elif difference[i] * difference[i + 1] < 0:
            crossing_idx.append(i)

    # If the difference occurred in the last sample, 
    # then the best PEEP is in the second-to-last sample
    if difference.iloc[-1] == 0:
        crossing_idx.append(len(difference) - 2)

    # Obtains the optimal PEEP
    opt_PEEP = PEEP[crossing_idx]

    return opt_PEEP


def saves_opt_PEEP_graphs(patient_ID, hyperdistension, PEEP, collapse, opt_PEEP):
    """
    Plots collapse values, hyperdistension values and optimal PEEP as a function of PEEP.
    Saves the graphs in the 'opt_PEEP_plots' file.

    Args:
        patient_ID (str): Patient identification
        hyperdistension (pandas Series): Hyperdistension values.
        PEEP (pandas Series): PEEP values.
        collapse (pandas Series): Collapse values.
        opt_PEEP (array): Array with the possible optimal points found; 
        if the number of points is different from 1, they will not be displayed on the graph.
        

    Returns:
        None.
    """
        
    # Creates a list for applicable warnings
    warnings = []

    ## Validates values before plotting:
    opt_PEEP_found = True
    display_warnings = False

    # Checks if any of the values ​​remain at 0%
    if np.all(hyperdistension == 0) or np.all(collapse == 0):
        warnings.append("Valores permanecem em 0%")
        display_warnings = True

    # Checks if any of the values ​​remain at 100%
    if np.all(hyperdistension == 100) or np.all(collapse == 100):
        warnings.append("Valores permanecem em 100%")
        display_warnings = True

    # Checks if the values ​​are between 0 and 100%
    if np.any(hyperdistension < 0) or np.any(hyperdistension > 100) or np.any(collapse < 0) or np.any(collapse > 100):
        warnings.append("Os valores de colapso e hiperdistensão devem estar entre 0 e 100%")
        display_warnings = True
        
    # Checks if the curves don't intersect at any point 
    if len(opt_PEEP) == 0:
        # If the curves only meet at the first step, there is no previous step to associate
        if hyperdistension.iloc[0] == collapse.iloc[0]:
            warnings.append("As curvas se encontram apenas no primeiro passo")
        else:
            warnings.append("As curvas não se cruzam")
        opt_PEEP_found = False
        display_warnings = True

    # Checks if the curves intersect more than once 
    if len(opt_PEEP) > 1:
        warnings.append("As curvas se cruzam mais de uma vez")
        opt_PEEP_found = False
        display_warnings = True
    
    # Plots the graph
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(PEEP, hyperdistension, marker='s', label = "Hiperdistensão")
    plt.plot(PEEP, collapse, marker='o', label = "Colapso")

    if opt_PEEP_found:
        # Draws a line at optimal PEEP
        opt_PEEP = float(opt_PEEP.item())
        plt.axvline(opt_PEEP, color='red', linestyle='--', linewidth=2, label = "Melhor PEEP")
    if display_warnings:
        # Organizes the list in text format
        warning_text = "; ".join(item for item in warnings)

        plt.text(
                0.5, 0.95,
                f"{warning_text}",
                transform=ax.transAxes,
                ha="center",
                va="top",
                color="red"
            )

    plt.gca().invert_xaxis()
    plt.xlabel(r"PEEP ($cmH_2O$)", fontsize=14)
    plt.ylabel("(%)", fontsize=14)
    plt.title(f"PEEP ótimo para o paciente {patient_ID}", fontsize=14)
    plt.grid()
    plt.legend()

    # Tries saving the graph in a folder created in the directory of the .py file
    try:
        # Plot directory
        file_directory = Path(__file__).resolve().parent
        plot_dir = os.path.join(file_directory, 'opt_PEEP_plots')
        os.makedirs(plot_dir, exist_ok=True)

        # Plot path
        plot_path = os.path.join(plot_dir, f"opt_PEEP_{patient_ID}")
        plt.savefig(f"{plot_path}.png", dpi=300, bbox_inches="tight", pad_inches=0.2)
        plt.close(fig)

        # Confirmation on the terminal
        print(f"Graph of optimal PEEP for the patient {patient_ID} saved: {plot_path}.png")

    # Generates an error message if Python indicates an OSError: [Errno 22] Invalid argument
    except OSError as e:
        if e.errno == errno.EINVAL: 
            raise RuntimeError("Error: Please ensure the graph file is closed before attempting to overwrite it.")
        else:
            raise  # If it's a different type of OSError, Python displays the original error

def peep_identification_and_plot(json_path):
    """
    Loads data from the.json file containing the collapse and hyperdistension values of the respiratory system;
    validates data;
    identifies the ideal PEEP value;
    plots collapse values, hyperdistension values and optimal PEEP as a function of PEEP; and
    saves the graphs in the 'opt_PEEP_plots' file.

    Args:
        json_path (str): Path to the .json file containing the data.

    Returns:
        None.
    """
    
    # Loads .json file 
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        raise RuntimeError(f"Error: File {json_path} not found.")
    
    # Debug print
    print(".json data:", data)

    # Iterates over each patient
    for patient in data:

        # Extracts Patient ID, Hyperdistension, PEEP and Collapse from data
        df = pd.DataFrame(patient['Titration Steps'])
        patient_ID = patient['Patient ID']
        hyperdistension = df['Hyperdistension']
        PEEP = df['PEEP']
        collapse = df['Collapse']

        print("\n ## Patient_ID:", patient_ID, "## \n")
        print(df)

        # Identifies optimal PEEP
        try:
            opt_PEEP = data_validation_and_opt_PEEP_identification(hyperdistension, PEEP, collapse)
            print(f"Optimal PEEP for patient {patient_ID}:", opt_PEEP.item())
        except ValueError as e:
            print(f"[{patient_ID}] ValueError: {e}")
            continue  # Skips this patient and moves on to the next one

        # Plots and saves the graphs
        saves_opt_PEEP_graphs(patient_ID, hyperdistension, PEEP, collapse, opt_PEEP)



# Application
if __name__ == "__main__":

    # Identificates the optimum PEEP for each case
    json_path = "C:/Users/reina/Vscode_projects/Timpel/dataset.json"
    peep_identification_and_plot(json_path)             
