import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def optimize_power_cuts(powerCutHours, num_blocks):
    """
    Optimiza la distribución de cortes de energía por bloque.

    Args:
        powerCutHours (int): Horas de corte por día (misma cantidad cada día).
        num_blocks (int): Número de bloques (zonas).

    Returns:
        list: Lista de diccionarios con {blockNumber, schedule} donde schedule es
              un array de {dayOfWeek, startCut, endCut} para cada día.
    """
    days = 7
    hours_per_day = 24

    # Función para crear matriz de cortes para un bloque
    def create_block_matrix(schedules):
        matrix = np.zeros((hours_per_day, days))
        for day in range(days):
            start = schedules[day]['startCut']
            end = schedules[day]['endCut']
            matrix[start:end, day] = 1
        return matrix

    # Función objetivo a minimizar
    def objective(x):
        # x contiene los parámetros de inicio y fin para cada bloque y día
        # Reorganizar x en una matriz de (num_blocks * days, 2)
        params = x.reshape((num_blocks * days, 2))

        block_matrices = []
        total_penalty = 0

        for block in range(num_blocks):
            schedules = []
            block_matrix = np.zeros((hours_per_day, days))

            for day in range(days):
                idx = block * days + day
                start = int(round(params[idx, 0]))
                end = int(round(params[idx, 1]))

                # Asegurar que el corte sea consecutivo y de duración correcta
                duration = end - start
                penalty = abs(duration - powerCutHours)
                total_penalty += penalty * 1000  # Penalización fuerte por incumplir duración

                block_matrix[start:end, day] = 1
                schedules.append({
                    'dayOfWeek': day,
                    'startCut': start,
                    'endCut': end
                })

            block_matrices.append(block_matrix)

        # Calcular suma de elementos por fila
        sum_rows = sum(np.sum(matrix, axis=1).sum() for matrix in block_matrices)

        # Calcular superposición (suma de todas las matrices / 2)
        overlap_matrix = sum(block_matrices)
        sum_overlap = np.sum(overlap_matrix[overlap_matrix > 1]) / 2

        return sum_rows + sum_overlap + total_penalty

    # Condiciones iniciales (distribución aleatoria)
    x0 = []
    for _ in range(num_blocks):
        for _ in range(days):
            start = np.random.randint(0, hours_per_day - powerCutHours)
            end = start + powerCutHours
            x0.extend([start, end])

    # Límites (0 ≤ start < end ≤ 24)
    bounds = []
    for _ in range(num_blocks * days):
        bounds.append((0, hours_per_day - 1))  # start
        bounds.append((1, hours_per_day))  # end

    # Optimización
    result = minimize(
        objective,
        x0,
        bounds=bounds,
        method='SLSQP',
        options={'maxiter': 1000, 'ftol': 1e-8}
    )

    # Procesar resultado
    optimized_params = result.x.reshape((num_blocks * days, 2))
    blocks_schedule = []

    for block in range(num_blocks):
        schedule = []
        for day in range(days):
            idx = block * days + day
            start = int(round(optimized_params[idx, 0]))
            end = int(round(optimized_params[idx, 1]))
            schedule.append({
                'dayOfWeek': day,
                'startCut': start,
                'endCut': end
            })

        blocks_schedule.append({
            'blockNumber': block + 1,
            'schedule': schedule
        })

    return blocks_schedule


def plot_power_cuts(schedule):
    """
    Muestra un gráfico de los rangos de cortes por bloque.

    Args:
        schedule (list): Lista de diccionarios con {blockNumber, schedule}.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    day_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    for block in schedule:
        block_num = block['blockNumber']
        for day_schedule in block['schedule']:
            day = day_schedule['dayOfWeek']
            start = day_schedule['startCut']
            end = day_schedule['endCut']

            ax.add_patch(Rectangle(
                (day, start), 1, end - start,
                edgecolor='black', linewidth=1,
                facecolor=f'C{block_num - 1}', alpha=0.6,
                label=f'Bloque {block_num}' if day == 0 else None
            ))

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 24)
    ax.set_xticks(np.arange(7) + 0.5)
    ax.set_xticklabels(day_names)
    ax.set_yticks(np.arange(24))
    ax.set_ylabel('Hora del día')
    ax.set_title('Distribución de cortes de energía por bloque')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    powerCutHours = 3  # 3 horas de corte por día
    num_blocks = 4  # 4 bloques (zonas)

    optimized_schedule = optimize_power_cuts(powerCutHours, num_blocks)

    # Imprimir resultados
    for block in optimized_schedule:
        print(f"\nBloque {block['blockNumber']}:")
        for day in block['schedule']:
            day_name = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][day['dayOfWeek']]
            print(f"{day_name}: {day['startCut']}:00 - {day['endCut']}:00")

    # Mostrar gráfico
    plot_power_cuts(optimized_schedule)