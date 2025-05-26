import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import pulp
import json
from typing import List, Dict, Any, Union, Optional

provinceMapper: List[str] = [
    "Pinar del Río",
    "La Habana",
    "Artemisa",
    "Mayabeque",
    "Matanzas",
    "Cienfuegos",
    "Ciego de Ávila",
    "Villa Clara",
    "Sancti Spíritus",
    "Las Tunas",
    "Holguín",
    "Camagüey",
    "Granma",
    "Santiago de Cuba",
    "Guantánamo"
]

# Lista de termoeléctricas y sus capacidades
termoelectricas: List[Dict[str, Any]] = []
demanda: List[int] = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]
demanda_bloques_habana: List[int] = [200, 100, 170, 130]


def execute_optimization(provincesDemand: List[Dict[str, Any]],
                         thermoelectricData: List[Dict[str, Any]],
                         blockDemand: List[int]) -> Dict[str, Any]:
    termoelectricas: List[Dict[str, Union[str, int]]] = []
    demanda: List[int] = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]

    for i in range(len(provincesDemand)):
        provinceIndex: int = provinceMapper.index(provincesDemand[i]["name"])
        demand: int = provincesDemand[i]["demand"]
        if demand != 0:
            demanda[provinceIndex] = demand

    for i in range(len(blockDemand)):
        if blockDemand[i] != 0:
            demanda[i] = blockDemand[i]

    for i in range(len(thermoelectricData)):
        termoelectricas.append({
            "nombre": thermoelectricData[i]["name"],
            "capacidad": thermoelectricData[i]["generationPerDay"]
        })

    print("Demanda:", demanda)
    print("Termoelectricas:", termoelectricas)
    print("Bloques Habana:", demanda_bloques_habana)

    def error_cuadratico(asignado: np.ndarray) -> float:
        error: float = 0
        for i in range(len(xdata)):
            deficit: float = (demanda[i] - asignado[i]) ** 2
            consumoPerHourProvince: float = demanda[i] / 24
            error += deficit / consumoPerHourProvince
        return error

    def constraint_sum(asignado: np.ndarray) -> float:
        return generacionTotal - np.sum(asignado)

    def constraint_habana(asignado: np.ndarray) -> float:
        return (5 / 100 * demanda[1]) - (demanda[1] - asignado[1])

    def constraint_never_exceed(asignado: np.ndarray) -> int:
        for i in range(len(asignado)):
            if asignado[i] < 0:
                return -1
        return 1

    # Calcular la disponibilidad total de MW
    generacionTotal: int = sum([t["capacidad"] for t in termoelectricas])

    xdata: range = range(0, 15)
    plt.plot(xdata, demanda, 'ro')

    # Define the constraint dictionary
    cons: List[Dict[str, Any]] = [
        {'type': 'ineq', 'fun': constraint_sum},
        {'type': 'ineq', 'fun': constraint_habana},
        {'type': 'ineq', 'fun': constraint_never_exceed},
    ]

    # Perform the optimization with constraints
    asignadoResult: spo.OptimizeResult = spo.minimize(error_cuadratico, [0] * 15, constraints=cons)

    # Calculate the deficit for each province
    deficit: List[float] = [demanda[i] - asignadoResult.x[i] for i in range(len(demanda))]

    # Plot the results
    plt.plot(xdata, demanda, 'ro')
    plt.plot(xdata, asignadoResult.x, 'bo')
    # Eliminar la línea que plotea el déficit: plt.plot(xdata, deficit, 'go')
    plt.xticks(ticks=xdata, labels=provinceMapper, rotation=45, ha='right')
    plt.legend(['Demanda', 'Asignados'])  # Actualizar la leyenda sin "Deficit"
    plt.savefig(f"static\\optimization_result.png")
    plt.show()

    # Print the results
    print(f"Optimization result: {asignadoResult}")
    provinceDataResponse: List[Dict[str, Any]] = []
    totalDeficit: float = sum(demanda) - sum(asignadoResult.x)
    for i in range(len(xdata)):
        deficit: float = demanda[i] - asignadoResult.x[i]
        consumoPerHourProvince: float = demanda[i] / 24
        timeToSatisfyAssigned: float = deficit / consumoPerHourProvince
        deficit_percentage: float = (deficit / demanda[i]) * 100
        provinceDataResponse.append({
            "id": i,
            "name": provinceMapper[i],
            "demand": demanda[i],
            "assigned": asignadoResult.x[i],
            "deficit": deficit,
            "powerCutHours": timeToSatisfyAssigned
        })
        print(
            f"{provinceMapper[i]}: Demanda: {demanda[i]}, Asignados: {asignadoResult.x[i]}, Deficit: {deficit}, Porcentaje Deficit: {deficit_percentage:.2f}%, Horas Apagon: {timeToSatisfyAssigned}")

    print(f"Total Asignado: {sum(asignadoResult.x)}")
    print(f"Total generado: {generacionTotal}")
    sumD: float = sum(demanda)
    print("Demanda Total:", sum(demanda))
    print(f"Deficit Total: {totalDeficit}")

    # Guardar los resultados en un archivo JSON
    result_data: Dict[str, Any] = {
        "provinces": provinceDataResponse,
        "totalDemand": sum(demanda),
        "totalGeneration": generacionTotal,
        "totalDeficit": totalDeficit,
        "chartUrl": "optimization_result.png",
    }

    # Guardar en un archivo JSON
    with open("static/optimization_results.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)

    return result_data