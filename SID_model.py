import numpy as np
import dearpygui.dearpygui as dpg
import scipy as sp

# Определение системы ОДУ
def System(y, t):
    S, I, D = y
    N = S + I + D

    for i in range(len(y)-1):
        if y[i] < 0:
            y[i] = 0
        elif y[i] > N:
            y[i] = N

    dSdt = - (beta * S * I) / N + gamma * I # Прирост выздоровливающих - 
    # прирост заболевания
    dIdt = beta * I * S / N - gamma * I - sigma * I # Прирост инфецированных минус
    # прирост выздоровления и минус прирост смертности
    dDdt = sigma * I # Прирост смертности
    return [dSdt, dIdt, dDdt]

# Метод Рунге-Кутта 4-го порядка точности
# Данная реализация работает для n уравнений, 
# если к ним есть n начальных условий
def rk4(y, t, System, ac = [0,0,0]):
    h = t[len(t)-1] - t[len(t)-2]
    eps = 1e-9
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

        #ac += delta_y
        ac = [ac[j] + delta_y[j] for j in range(len(delta_y))]

        for j in range(len(delta_y)):
            print(y[j], ac[j], (y[j] + ac[j]) - y[j])
            if abs((y[j] + ac[j]) - y[j]) > eps:
                print("Entered")
                y[j] += ac[j]
                ac[j] = 0
     
        y = [y[j] + delta_y[j] for j in range(len(y))]
        
        result.append(y)

    return result

# Функция обновления графиков относительно
# изменения значений на слайдерах
# срабатывает при нажатии на соответствующую кнопку
def update_series():
    global beta, sigma, gamma, ac
    beta = dpg.get_value('beta_slider')
    gamma = dpg.get_value('gamma_slider')
    sigma = dpg.get_value('sigma_slider')

    solve = rk4(start, time, System, ac)
    ac = [0,0,0]
    #solve = sp.integrate.odeint(System, start, time)
    solve = np.array(solve)
    S = solve[:,0] # Колиство восприимчивых особей в момент времени t
    I = solve[:,1] # Колиство инфецированных особей в момент времени t
    D = solve[:,2] # Колиство погибших особей в момент времени t
    y1 = S.tolist()
    y2 = I.tolist()
    y3 = D.tolist()
    dpg.set_value('Survived_series', [time, y1])
    dpg.set_value('Infected_series', [time, y2])
    dpg.set_value('Dead_series', [time, y3])

time = np.linspace(0, 100, 10) # Массив времени (независимая переменная)
time = time.tolist()

dpg.create_context()

# Создать окно с разрешением 2560*1600
with dpg.window(tag = 'Main', autosize=True):

    dpg.add_slider_float(label='Infection chance', default_value=0.2,
                          max_value=1., tag='beta_slider', format='%0.2f')
    dpg.add_slider_float(label='Recovery chance', default_value=0.05, 
                         max_value=1., tag='gamma_slider', format='%0.2f')
    dpg.add_slider_float(label='Death chance', default_value=0.05, 
                         max_value=1., tag='sigma_slider', format='%0.2f')

    beta = dpg.get_value('beta_slider') # Вероятность заразить
    gamma = dpg.get_value('gamma_slider') # Вероятность выздоровления
    sigma = dpg.get_value('sigma_slider') # Вероятность наличия у инфецированных 
    # особей сопутствующих заболеваний
    # приводящих к смерти

    start = [99, 1, 0] # Начальные значения (99 восприимчивых, 1 инфецированный)
    ac = [0,0,0]
    solve = rk4(start, time, System, ac) # численное решение Рунге-Кутта 4-го порядка
    #solve = sp.integrate.odeint(System, start, time)
    solve = np.array(solve)

    S = solve[:,0] # Колиство восприимчивых особей в момент времени t
    I = solve[:,1] # Колиство инфецированных особей в момент времени t
    D = solve[:,2] # Колиство погибших особей в момент времени t

    dpg.add_button(label="Update Series", callback=update_series)

    # Окно графиков с настройками
    with dpg.plot(width=-1):
        dpg.add_plot_legend()

        # создать x axis
        dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        # создать y axis
        dpg.add_plot_axis(dpg.mvYAxis, label = 'Count of creatures',
                          tag='y_axis')

        y1 = S.tolist()
        y2 = I.tolist()
        y3 = D.tolist()

        dpg.add_line_series(time, y1, label="Survived", 
                            parent='y_axis', tag='Survived_series')
        dpg.add_line_series(time, y2, label="Infected", 
                            parent='y_axis', tag='Infected_series')
        dpg.add_line_series(time, y3, label="Dead", 
                            parent='y_axis', tag='Dead_series')
        
dpg.create_viewport(title='Model SID', width=900, height=540)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Main', True)
dpg.start_dearpygui()
dpg.destroy_context()