import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo



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
termoelectricas = [
    {"nombre": "CTE Máximo Gómez", "ubicacion": "Mariel, Artemisa", "capacidad": 370},
    {"nombre": "CTE Otto Parellada", "ubicacion": "La Habana", "capacidad": 60},
    {"nombre": "CTE Ernesto Guevara", "ubicacion": "Santa Cruz del Norte, Mayabeque", "capacidad": 295},
    {"nombre": "CTE Antonio Guiteras", "ubicacion": "Matanzas", "capacidad": 317},
    {"nombre": "CTE Carlos Manuel de Céspedes", "ubicacion": "Cienfuegos", "capacidad": 316},
    {"nombre": "CTE Diez de Octubre", "ubicacion": "Nuevitas, Camagüey", "capacidad": 375},
    {"nombre": "CTE Lidio Ramón Pérez", "ubicacion": "Felton, Holguín", "capacidad": 480},
    {"nombre": "CTE Antonio Maceo", "ubicacion": "Renté, Santiago de Cuba", "capacidad": 380}
]

def execute_optimization(provincesDemand, thermoelectricData):
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

    # Restriccion, el deficit de la habana no puede ser mayor al 10% de la demanda
    def constraint_habana(asignado):
        return (5 / 100 * demanda[1]) - (demanda[1] - asignado[1])

    def constraint_never_exceed(asignado):
        for i in range(len(asignado)):
            if asignado[i] < 0:
                return -1
        return 1

    # Calcular la disponibilidad total de MW
    generacionTotal = sum([t["capacidad"] for t in termoelectricas])

    demanda = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]

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

    # Plot the results
    plt.plot(xdata, asignadoResult.x, 'bo')
    plt.xticks(ticks=xdata, labels=provinceMapper, rotation=45, ha='right')
    plt.show()

    # Print the results
    print(f"Optimization result: {asignadoResult}")
    provinceDataResponse = []
    totalDeficit = sum(demanda) - sum(asignadoResult.x)
    for i in range(len(xdata)):
        deficit = demanda[i] - asignadoResult.x[i]
        consumoPerHourProvince = demanda[i] / 24
        timeToSatisfyAssigned = deficit / consumoPerHourProvince
        provinceDataResponse.append({
            "id": i,
            "name": provinceMapper[i],
            "demand": demanda[i],
            "assigned": asignadoResult.x[i],
            "deficit": deficit,
            "powerCutHours": timeToSatisfyAssigned
        })
        print(f"{provinceMapper[i]}: Demanda: {(demanda[i])} , Asignados: {asignadoResult.x[i]}, Deficit: {deficit} , Horas Apagon: {timeToSatisfyAssigned}")

    print(f"total Asignado: {sum(asignadoResult.x)}")
    print(f"total generado: {generacionTotal}")
    print("Demanda Total:",sum(demanda))
    print(f"Deficit Total: {totalDeficit}")
    return {
        "provinces": provinceDataResponse,
        "totalDemand": sum(demanda),
        "totalGeneration": generacionTotal,
        "totalDeficit": totalDeficit
    }
