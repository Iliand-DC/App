import numpy as np
import scipy as sp
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

# Метод Рунге-Кутта 4-го порядка точности
# Данная реализация работает для n уравнений, 
# если к ним есть n начальных условий
def rk4(y, t, System):
    h = t[len(t)-1] - t[len(t)-2]
    result = [y]
    for i in range(len(t)-1):
        k1 = [System(y, t[i])[j] * h for j in range(len(y))]

        y_2 = [y[j] + k1[j]/2 for j in range(len(y))]
        k2 = [System(y_2, t[i] + h/2)[j] * h for j in range(len(y))]

        y_3 = [y[j] + k2[j]/2 for j in range(len(y))]
        k3 = [System(y_3, t[i] + h/2)[j] * h for j in range(len(y))]

        y_4 = [y[j] + k3[j] for j in range(len(y))]
        k4 = [System(y_4, t[i] + h)[j] * h for j in range(len(y))]

        delta_y = [(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6 for j in range(len(y))]
        
        y = [y[j] + delta_y[j] for j in range(len(y))]
        result.append(y)

    return result

beta = 0.35 # Вероятность заразить
gamma = 0.2 # Вероятность выздоровления
sigma = 0.01 # Вероятность наличия у инфецированных особей сопутствующих заболеваний
# приводящих к смерти

# Определение системы ОДУ
def System(y, t):
    S, I, D = y
    N = S + I + D
    dSdt = - (beta * S * I) / N + gamma * I # Прирост выздоровливающих - 
    # прирост заболевания
    dIdt = beta * I * S / N - gamma * I - sigma * I # Прирост инфецированных минус
    # прирост выздоровления и минус прирост смертности
    dDdt = sigma * I # Прирост смертности
    return [dSdt, dIdt, dDdt]

time = np.linspace(0, 100, 10) # Массив времени (независимая переменная)
start = [99, 1, 0] # Начальные значения (99 восприимчивых, 1 инфецированный)

solve = rk4(start, time, System) # численное решение Рунге-Кутта 4-го порядка
solve = np.array(solve)

S = solve[:,0] # Колиство восприимчивых особей в момент времени t
I = solve[:,1] # Колиство инфецированных особей в момент времени t
D = solve[:,2] # Колиство погибших особей в момент времени t

# Печать результатов в консоль
print('Результаты, полученные с помощью метода Рунге-Кутта 4-го порядка')
print('Количество восприимчивых особей ', round(S[len(S)-1]))
print('Количество заражённых особей ', round(I[len(I)-1]))
print('Количество погибших особей ', round(D[len(D)-1]), '\n')

fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=S, name='Восприимчивые особи'))
fig.add_trace(go.Scatter(x=time, y=I, name='Заражённые особи'))
fig.add_trace(go.Scatter(x=time, y=D, name='Погибшие особи'))
fig.update_layout(legend_orientation='h',
                  title='Визуализация модели SID',
                  xaxis_title='Время',
                  yaxis_title='Количество особей')
fig.update_traces(hoverinfo='all', hovertemplate='Время: %{x}<br>Количество: %{y}')
fig.show()