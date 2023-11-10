# Модель Восприимчивые-Инфецированные-Мёртвые
# Система дифференциальных уравнений, учитывающая
# Шансы на заражение инфекцией, выздоровления, смерти

class sid_model:
    def __init__(self, beta, gamma, sigma):
        self.beta = beta
        self.gamma = gamma
        self.sigma = sigma
    
    # Определение системы ОДУ
    def SID(self, y, t):
        S, I, D = y
        N = S + I + D

        dSdt = - (self.beta * S * I) / N + self.gamma * I # Прирост выздоровливающих - 
        # прирост заболевания
        dIdt = self.beta * I * S / N - self.gamma * I - self.sigma * I # Прирост инфецированных минус
        # прирост выздоровления и минус прирост смертности
        dDdt = self.sigma * I # Прирост смертности

        return [dSdt, dIdt, dDdt]