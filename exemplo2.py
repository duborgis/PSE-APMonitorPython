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
Tf = m.Var(value=0.1, lb=0.1, ub=100)
# T = m.MV(value=298, lb=273, ub=373 )
# T.STATUS = 1 #LIBERA A VARIAVEL PARA O APMONITOR MEXER
# T.DMAX = 2
# T.DCOST = 0.5
#definir parametros do modelo
k01=4e3
k02=6.2e5
E1=2500
E2=5000
T=300
#Criar Intermediates
#AVALIADO QUANDO RESOLVIDO O SISTEMA
#utilizar funç~eso configuradas no GEKKO, não usar math ou numpy
# evitar aumentar a dimensão do sistema
# como T é uma variável gekko, ela só pode ser utilizada dentro de intermediate
k1 = m.Intermediate(k01*m.exp(-E1/T))
k2 = m.Intermediate(k02*m.exp(-E2/T))
#criar as restrições do sistema
# m.Equation( xB.dt() == k1*xA**2 - k2*xB )
# m.Equation( xA.dt() == -k1*xA**2)
# m.Equation( xA + xB + xC == 1 )
# OUTRA FORMA DE DEFINIR EQUAÇÕES
# eqs = [
# xB.dt() == k1*xA**2 - k2*xB,
# xA.dt() == -k1*xA**2,
# xA + xB + xC == 1 
# ]
# m.Equations(eqs)
# OUTRA FORMA DE DEFINIR EQUAÇÕES
def func():
	f1 = Tf*(k1*xA**2 - k2*xB)
	f2 = Tf*(-k1*xA**2)
	f3 = xA + xB + xC - 1
	return [f1, f2, f3]
f = func()
m.Equation( xB.dt() == f[0])
m.Equation( xA.dt() == f[1])
m.Equation( 0 == f[2] )
# m.Equation(xB >= 0.2)
#Resolver um problema do tipo simulação dinamica
#Setar o modo de operação
m.options.IMODE = 6
#Dizer quais são os intervalos de tempo para as soluções serem obtidas
nt=50
m.time = np.linspace(0,1,nt)
# CRIAR A CLASSE PARAM, ONDE O GEKKO SABE QUE É UM ARRAY VARIÁVEL NO TEMPO
h=np.zeros(nt)
# MUDA O ULTIMO ELEMENTO PARA 1 NO VETOR DE ZEROS
h[-1] = 1
final = m.Param(value=h)
precoB = 400
custoT = m.Intermediate(0.01*abs(300-T))

# CRIAR A FUNÇÃO OBJETIVO
# MAX DE F = MIN DE -F
# GEKKO SOMENTE OTIMIZA PARA O MINIMO
m.Obj( -xB*final*10 + Tf )
# chamar o solver -> método de solução
m.solve(disp=False)
#plotar gráficos
plt.figure()
# plt.subplot(2,1,1)
plt.plot( m.time*Tf.value[-1], xB.value )
plt.xlabel("Tempo")
plt.ylabel("$x_B$")

# plt.subplot(2,1,2)
# plt.plot(m.time, T.value, "r")
# plt.ylabel("Temperatura")
# plt.xlabel("Tempo")
# plt.legend("Fobj = " + str[xB.value[-1]*precoB - custoT.value[-1]])
plt.show()