import numpy as np
import cantera as ct
import matplotlib.pyplot as plt

x = [x * 0.005 for x in range(8, 150)]
o = ct.one_atm
P = [0.2*o, 0.3*o, 0.4*o, 0.5*o, 0.6*o, 0.7*o, 0.8*o, 0.9*o, o, 1.1*o, 1.2*o, 1.3*o, 1.4*o, 1.5*o]
elements = len(x)*len(P)
print elements
ignition_temp = []
ignition_delay = []
result_file = open('results.txt', 'w')
result_file2 = open('temperature&delay.txt', 'w')
ign_res = np.zeros((4,elements))
iterator = 0

for i in x:                     #different mixtures
    print 'x = %f' % (i)
    result_file.write('\nx = %f\n' % (i))
    result_file2.write('\nx = %f\n' % (i))  
    
    start = iterator*len(P)
    end = iterator*len(P) + len(P)
    for aa in range(start,end):
        ign_res[0,aa] = i
    
    iterator1 = iterator*len(P)
    
    for c in P:         #different pressures
        result_file.write('p = %f\n' % (c))
        j = (1-i)*0.21
        k = (1-i)*0.79
        gri3 = ct.Solution('gri30.cti')
        gri3.TPX = 1000.0, c, 'H2:'+str(i)+', O2:'+str(j)+', N2:'+str(k)+''
        r = ct.IdealGasReactor(gri3)
    
        sim = ct.ReactorNet([r])
        time = 0.0
        times = np.zeros(150)
        data = np.zeros((150,4))
    
        Tmax = 0
        ignition_time = 0
        OH = 0
        tab = np.zeros((14,150))
        number = c/ct.one_atm  * 10 - 2

        place = iterator1
        ign_res[1,place] = c
            
        iterator1 = iterator1 + 1
        
        result_file.write('%10s %10s %10s %14s \n' % ('t [s]','T [K]','P [Pa]','u [J/kg]'))
        
        for n in range(150):
            time += 1.e-5
            sim.advance(time)
            times[n] = time * 1e3  # time in ms
            data[n,0] = r.T
            data[n,1:] = r.thermo['OH','H','H2'].X
            tab[number, n] = r.T
            result_file.write('%e %f %f %e\n' % (sim.time, r.T, r.thermo.P, r.thermo.u))
    
            if r.thermo['OH'].X > OH:
                OH = r.thermo['OH'].X
                Tmax = r.T
                ignition_time = time
                ignition_temp.append(Tmax)
                ignition_delay.append(ignition_time)
                ign_res[2,place] = time
                ign_res[3,place] = r.T

    result_file2.write('%s %s %s\n' % ('P [Pa]', 'T [K]', 't [s]'))
    
    for index in range(0, len(P)):
        result_file2.write('%f %f %f\n' % (P[index], ignition_temp[index], ignition_delay[index]))
    
    ignition_temp = []
    ignition_delay = [] 
    
    iterator = iterator + 1    

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(ign_res[1,:], ign_res[2,:], 'ro')
plt.xlabel('Pressure (Pa)')
plt.ylabel('Autoignition delay (ms)')
plt.subplot(2, 1, 2)
plt.plot(ign_res[1,:], ign_res[3,:], 'bo')
plt.xlabel('Pressure (Pa)')
plt.ylabel('Autoignition temperature (K)')
plt.tight_layout()
plt.show()
plt.savefig('figure_1_'+str(i)+'.png')

plt.clf()
plt.subplot(2, 1, 1)
plt.plot(ign_res[0,:], ign_res[2,:], 'ro')
plt.axis([0, 0.8, 0, 0.004])
plt.xlabel('Hydrogen percentage')
plt.ylabel('Autoignition delay (ms)')
plt.subplot(2, 1, 2)
plt.plot(ign_res[0,:], ign_res[3,:], 'bo')
plt.xlabel('Hydrogen percentage')
plt.ylabel('Autoignition temperature (K)')
plt.tight_layout()
plt.show()
plt.savefig('figure_2_'+str(i)+'.png')
    
print ign_res    
    
result_file.close()
result_file2.close()