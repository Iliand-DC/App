# Метод Рунге-Кутта 4-го порядка точности
# Данная реализация работает для n уравнений, 
# если к ним есть n начальных условий
def rk4(y, t, function):
    h = t[len(t)-1] - t[len(t)-2]
    result = [y]
    for i in range(len(t)-1):
        k1 = [function(y, t[i])[j] * h for j in range(len(y))]

        y_2 = [y[j] + k1[j]/2 for j in range(len(y))]
        k2 = [function(y_2, t[i] + h/2)[j] * h for j in range(len(y))]

        y_3 = [y[j] + k2[j]/2 for j in range(len(y))]
        k3 = [function(y_3, t[i] + h/2)[j] * h for j in range(len(y))]

        y_4 = [y[j] + k3[j] for j in range(len(y))]
        k4 = [function(y_4, t[i] + h)[j] * h for j in range(len(y))]

        delta_y = [(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6 for j in range(len(y))]
     
        y = [y[j] + delta_y[j] for j in range(len(y))]
        
        result.append(y)

    return result