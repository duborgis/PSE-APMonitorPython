import numpy as np
from gekko import GEKKO
import matplotlib.pyplot as plt

#inicializa a instancia GEKKO e não utiliza o servidor remoto
#utiliza o servidor LOCAL,instalado na maquina
m = GEKKO(remote=True)

#CRIAR AS VARIAVEIS NO GEKKO
#SS value é o chute inicial
#OTimi Dina value -é CI
xA = m.Var(value=1, lb=0, ub=1)
xB = m.Var(value=0, lb=0, ub=1)
xC = m.Var(value=0, lb=0, ub=1)

#definir parametros do modelo
k01=4e3
k02=6.2e5
E1=2500
E2=5000
T=350

#Criar Intermediates
#AVALIADO QUANDO RESOLVIDO O SISTEMA
#utilizar funç~eso configuradas no GEKKO, não usar math ou numpy
k1 = m.Intermediate(k01*m.exp(-E1/T))
k2 = m.Intermediate(k02*m.exp(-E2/T))

#criar as restrições do sistema
m.Equation( xB.dt() == k1*xA**2 - k2*xB )
m.Equation( xA.dt() == -k1*xA**2)
m.Equation( xA + xB + xC == 1 )


# OUTRA FORMA DE DEFINIR EQUAÇÕES
# eqs = [
# xB.dt() == k1*xA**2 - k2*xB,
# xA.dt() == -k1*xA**2,
# xA + xB + xC == 1 
# ]
# m.Equations(eqs)


# OUTRA FORMA DE DEFINIR EQUAÇÕES
def func():
	f1 = k1*xA**2 - k2*xB
	f2 = -k1*xA**2
	f3 = xA + xB + xC - 1
	return [f1, f2, f3]


f = func()

m.Equation( xB.dt() == f[0])
m.Equation( xA.dt() == f[1])
m.Equation( 0 == f[2] )


#Resolver um problema do tipo simulação dinamica
#Setar o modo de operação
m.options.IMODE = 4

#Dizer quais são os intervalos de tempo para as soluções serem obtidas
nt=50
m.time = np.linspace(0,1,nt)

# chamar o solver -> método de solução
m.solve(disp=False)


#plotar gráficos
plt.figure()
plt.plot( m.time, xA.value, m.time, xB.value, m.time, xC.value )
plt.xlabel("Tempo")
plt.ylabel("Concentrações")
plt.legend(["$ x_A $", "$ x_B $", "$ x_C $"])
plt.show()








