import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import pulp


provinceMapper = [
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
termoelectricas = []
demanda = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]
demanda_bloques_habana = [200, 100, 170, 130]


def execute_optimization(provincesDemand, thermoelectricData, blockDemand):
    termoelectricas = []
    demanda = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]


    for i in range(len(provincesDemand)):
        provinceIndex = provinceMapper.index(provincesDemand[i]["name"])
        demand = provincesDemand[i]["demand"]
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


    def error_cuadratico(asignado):
        error = 0
        for i in range(len(xdata)):
            deficit = (demanda[i] - asignado[i]) ** 2
            consumoPerHourProvince = demanda[i] / 24
            error += deficit / consumoPerHourProvince
        return error

    # Constraint function: sum of asignado should be less than or equal to generacionTotal
    def constraint_sum(asignado):
        return generacionTotal - np.sum(asignado)

    # Restriccion, el deficit de la habana no puede ser mayor al 5% de la demanda
    def constraint_habana(asignado):
        return (5 / 100 * demanda[1]) - (demanda[1] - asignado[1])

    def constraint_never_exceed(asignado):
        for i in range(len(asignado)):
            if asignado[i] < 0:
                return -1
        return 1
    # Calcular la disponibilidad total de MW
    generacionTotal = sum([t["capacidad"] for t in termoelectricas])


    xdata = range(0, 15)
    plt.plot(xdata, demanda, 'ro')

    # Define the constraint dictionary
    cons = [
        {'type': 'ineq', 'fun': constraint_sum},
        {'type': 'ineq', 'fun': constraint_habana},
        {'type': 'ineq', 'fun': constraint_never_exceed},
    ]

    # Perform the optimization with constraints
    asignadoResult = spo.minimize(error_cuadratico, [0]*15, constraints=cons)

    # Calculate the deficit for each province
    deficit = [demanda[i] - asignadoResult.x[i] for i in range(len(demanda))]

    # Plot the results
    plt.plot(xdata, asignadoResult.x, 'bo')
    plt.plot(xdata, deficit, 'go')
    plt.xticks(ticks=xdata, labels=provinceMapper, rotation=45, ha='right')
    plt.legend(['Demanda', 'Asignados', 'Deficit'])
    plt.savefig(f"static\\optimization_result.png")
    plt.show()

    # Print the results
    print(f"Optimization result: {asignadoResult}")
    provinceDataResponse = []
    totalDeficit = sum(demanda) - sum(asignadoResult.x)
    for i in range(len(xdata)):
        deficit = demanda[i] - asignadoResult.x[i]
        consumoPerHourProvince = demanda[i] / 24
        timeToSatisfyAssigned = deficit / consumoPerHourProvince
        deficit_percentage = (deficit / demanda[i]) * 100
        provinceDataResponse.append({
            "id": i,
            "name": provinceMapper[i],
            "demand": demanda[i],
            "assigned": asignadoResult.x[i],
            "deficit": deficit,
            "powerCutHours": timeToSatisfyAssigned
        })
        print(f"{provinceMapper[i]}: Demanda: {demanda[i]}, Asignados: {asignadoResult.x[i]}, Deficit: {deficit}, Porcentaje Deficit: {deficit_percentage:.2f}%, Horas Apagon: {timeToSatisfyAssigned}")

    print(f"Total Asignado: {sum(asignadoResult.x)}")
    print(f"Total generado: {generacionTotal}")
    sumD = sum(demanda)
    print("Demanda Total:", sum(demanda))
    print(f"Deficit Total: {totalDeficit}")

    return {
        "provinces": provinceDataResponse,
        "totalDemand": sum(demanda),
        "totalGeneration": generacionTotal,
        "totalDeficit": totalDeficit,
        "chartUrl": "optimization_result.png",
    }
