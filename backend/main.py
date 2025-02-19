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

    ##################################################################################################################################################################

    # Datos de entrada

    demanda_habana = 800


    asignados_habana = 700


    # Calcular proporciones y asignación por bloque
    proporciones_habana = [d / demanda_habana for d in demanda_bloques_habana]
    asignados_bloques_habana = [asignados_habana * p for p in proporciones_habana]

    # Calcular consumo promedio por hora
    consumo_promedio_bloques = [d / 24 for d in demanda_bloques_habana]

    # Calcular tiempo con fluido eléctrico por bloque
    tiempo_con_fluido = [
        (asignados_bloques_habana[i] / consumo_promedio_bloques[i])
        for i in range(len(demanda_bloques_habana))
    ]

    # Número de bloques y horas
    num_bloques = len(demanda_bloques_habana)
    horas = 24

    # Crear el problema de optimización
    problema = pulp.LpProblem("Distribucion_Fluido_Electrico", pulp.LpMinimize)

    # Variables de decisión
    x = pulp.LpVariable.dicts("Encendido", ((i, t) for i in range(num_bloques) for t in range(horas)), cat="Binary")
    d = pulp.LpVariable.dicts("Diferencia", ((i, t) for i in range(num_bloques) for t in range(1, horas)), lowBound=0)

    # Función objetivo: Minimizar la cantidad de cambios en el estado (de encendido a apagado y viceversa)
    problema += pulp.lpSum(d[i, t] for i in range(num_bloques) for t in range(1, horas))

    # Restricciones
    for i in range(num_bloques):
        # Cada bloque debe cumplir con su tiempo de fluido eléctrico
        problema += pulp.lpSum(x[i, t] for t in range(horas)) == tiempo_con_fluido[i]

        for t in range(1, horas):
            problema += d[i, t] >= x[i, t] - x[i, t - 1]
            problema += d[i, t] >= x[i, t - 1] - x[i, t]

    for t in range(horas):
        for i in range(num_bloques - 1):
            # No permitir que dos bloques contiguos estén apagados al mismo tiempo
            problema += x[i, t] + x[i + 1, t] >= 1

    # Resolver el problema
    problema.solve()

    # Mostrar resultados
    print("Estado:", pulp.LpStatus[problema.status])
    print("Cantidad mínima de cambios en el estado:", pulp.value(problema.objective))

    resultados = np.zeros((num_bloques, horas))
    for i in range(num_bloques):
        for t in range(horas):
            resultados[i, t] = pulp.value(x[i, t])

    # Create a list to store the intervals for each block
    block_intervals = []

    # Iterate through the blocks and their respective hours to determine the intervals of being turned on
    for i in range(num_bloques):
        intervals = []
        encendido = False
        inicio_intervalo = 0

        for t in range(horas):
            if resultados[i, t] == 1 and not encendido:
                encendido = True
                inicio_intervalo = t
            elif resultados[i, t] == 0 and encendido:
                encendido = False
                intervals.append((inicio_intervalo, t - 1))

        if encendido:
            intervals.append((inicio_intervalo, horas - 1))

        block_intervals.append(intervals)
    # Verificar la energía consumida para cada bloque
    block_energy_details = []

    # Iterate through the blocks to calculate the hours turned on and energy consumed
    for i in range(num_bloques):
        horas_encendido = np.sum(resultados[i, :])
        energia_consumida = horas_encendido * consumo_promedio_bloques[i]
        block_energy_details.append({
            "block": i + 1,
            "consumoPromedioBloques": consumo_promedio_bloques[i],
            "horasEncendido": horas_encendido,
            "energiaConsumida": energia_consumida,
            "energiaAsignada": asignados_bloques_habana[i],
            "intervals": block_intervals[i]
        })

    # Graficar los resultados
    plt.figure(figsize=(12, 8))

    for i in range(num_bloques):
        plt.plot(range(horas), resultados[i, :], label=f'Bloque {i + 1}')

    plt.xlabel('Hora')
    plt.ylabel('Estado (1: Encendido, 0: Apagado)')
    plt.title('Distribución del fluido eléctrico por hora')
    plt.legend()
    plt.grid()
    plt.savefig(f"static\\power-cut-hour.png")
    plt.show()



    # Return the updated dictionary
    return {
        "provinces": provinceDataResponse,
        "totalDemand": sum(demanda),
        "totalGeneration": generacionTotal,
        "totalDeficit": totalDeficit,
        "chartUrl": "optimization_result.png",
        "blockIntervals": block_intervals,
        "blockEnergyDetails": block_energy_details
    }
