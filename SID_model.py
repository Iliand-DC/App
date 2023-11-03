import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

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

beta = 0.2 # Вероятность заразить
gamma = 0.05 # Вероятность выздоровления
sigma = 0.1 # Вероятность наличия у инфецированных особей сопутствующих заболеваний
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

# Печать графиков
fig = plt.figure(facecolor = 'white')
# plt.subplot(121)
plt.title('Рунге-Кутта 4-го порядка')
plt.plot(time, S, '-o', label='Восприимчивые особи', color = 'green',linewidth=2)
plt.plot(time, I,'-o', label='Заражённые особи', color = 'red',linewidth=2)
plt.plot(time, D ,'-o', label='Погибшие особи', color = 'black',linewidth=2)
plt.xlabel('Время')
plt.ylabel('Количество особей')
plt.grid(True)
plt.legend()

# Печать результатов в консоль
print('Результаты, полученные с помощью метода Рунге-Кутта 4-го порядка')
print('Количество восприимчивых особей ', round(S[len(S)-1]))
print('Количество заражённых особей ', round(I[len(I)-1]))
print('Количество погибших особей ', round(D[len(D)-1]), '\n')

solve = sp.integrate.odeint(System, start, time) # odeint - решение систем ОДУ
solve = np.array(solve)

S = solve[:,0] # Колиство восприимчивых особей в момент времени t
I = solve[:,1] # Колиство инфецированных особей в момент времени t
D = solve[:,2] # Колиство погибших особей в момент времени t

"""
# Печать графиков
plt.subplot(122)
plt.title('Scipy.integrate.odeint')
plt.plot(time, S, '-o', label='Восприимчивые особи', color = 'green',linewidth=2)
plt.plot(time, I,'-o', label='Заражённые особи', color = 'red',linewidth=2)
plt.plot(time, D ,'-o', label='Погибшие особи', color = 'black',linewidth=2)
plt.xlabel('Время')
plt.ylabel('Количество особей')
plt.grid(True)
plt.legend()

# Печать результатов в консоль
print('Результаты, полученные с помощью odeint')
print('Количество восприимчивых особей ', round(S[len(S)-1]))
print('Количество заражённых особей ', round(I[len(I)-1]))
print('Количество погибших особей ', round(D[len(D)-1]), '\n')

"""

plt.show()
