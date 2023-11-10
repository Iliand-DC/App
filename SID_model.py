import numpy as np
import dearpygui.dearpygui as dpg
from RungeKutta import rk4
from Model import sid_model

# Функция обновления графиков относительно
# изменения значений на слайдерах
# срабатывает при нажатии на соответствующую кнопку
def update_series():
    global beta, sigma, gamma
    beta = dpg.get_value('beta_slider')
    gamma = dpg.get_value('gamma_slider')
    sigma = dpg.get_value('sigma_slider')
    ode_system = sid_model(beta, gamma, sigma)

    solve = rk4(start, time, ode_system.SID)
    solve = np.array(solve)
    
    S = solve[:,0] # Колиство восприимчивых особей в момент времени t
    I = solve[:,1] # Колиство инфецированных особей в момент времени t
    D = solve[:,2] # Колиство погибших особей в момент времени t
    dpg.set_value('Survived_series', [time, S.tolist()])
    dpg.set_value('Infected_series', [time, I.tolist()])
    dpg.set_value('Dead_series', [time, D.tolist()])
    dpg.set_value('Survived_text', 'Survived creatures: ' + str(round(S[len(S)-1])))
    dpg.set_value('Infected_text', 'Infected creatures: ' + str(round(I[len(I)-1])))
    dpg.set_value('Dead_text', 'Dead creatures: ' + str(round(D[len(D)-1])))

time = np.linspace(0, 100, 100) # Массив времени (независимая переменная)
time = time.tolist()

dpg.create_context()

# Создать окно с разрешением 2560*1600
with dpg.window(tag = 'Main', autosize=True):

    # Создаём тему для графиков
    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)


    dpg.add_slider_float(label='Infection chance', default_value=0.2,
                          max_value=1., tag='beta_slider', format='%0.2f',
                          callback=update_series)
    dpg.add_slider_float(label='Recovery chance', default_value=0.05, 
                         max_value=1., tag='gamma_slider', format='%0.2f',
                         callback=update_series)
    dpg.add_slider_float(label='Death chance', default_value=0.05, 
                         max_value=1., tag='sigma_slider', format='%0.2f',
                         callback=update_series)

    beta = dpg.get_value('beta_slider') # Вероятность заразить
    gamma = dpg.get_value('gamma_slider') # Вероятность выздоровления
    sigma = dpg.get_value('sigma_slider') # Вероятность наличия у инфецированных 
    # особей сопутствующих заболеваний
    # приводящих к смерти

    ode_system = sid_model(beta, gamma, sigma)
    start = [99, 1, 0] # Начальные значения (99 восприимчивых, 1 инфецированный)
    solve = rk4(start, time, ode_system.SID) # численное решение Рунге-Кутта 4-го порядка
    solve = np.array(solve)

    S = solve[:,0] # Колиство восприимчивых особей в момент времени t
    I = solve[:,1] # Колиство инфецированных особей в момент времени t
    D = solve[:,2] # Колиство погибших особей в момент времени t

    dpg.add_text('Survived creatures: ' + str(round(S[len(S)-1])), tag='Survived_text')
    dpg.add_text('Infected creatures: ' + str(round(I[len(I)-1])), tag='Infected_text')
    dpg.add_text('Dead creatures: ' + str(round(D[len(D)-1])), tag='Dead_text')

    # Окно графиков с настройками
    with dpg.plot(width=-1):

        dpg.add_plot_legend()

        # создать x axis
        dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        dpg.set_axis_limits(dpg.last_item(), -10, 110)
        # создать y axis
        dpg.add_plot_axis(dpg.mvYAxis, label = 'Count of creatures',
                          tag='y_axis')
        dpg.set_axis_limits(dpg.last_item(), -10, 110)

        dpg.add_line_series(time, S.tolist(), label="Survived", 
                            parent='y_axis', tag='Survived_series')
        dpg.add_line_series(time, I.tolist(), label="Infected", 
                            parent='y_axis', tag='Infected_series')
        dpg.add_line_series(time, D.tolist(), label="Dead", 
                            parent='y_axis', tag='Dead_series')
        

        dpg.bind_item_theme('Survived_series', 'plot_theme')
        dpg.bind_item_theme('Infected_series', 'plot_theme')
        dpg.bind_item_theme('Dead_series', 'plot_theme')
        

dpg.create_viewport(title='Model SID', width=900, height=540)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Main', True)
dpg.start_dearpygui()
dpg.destroy_context()