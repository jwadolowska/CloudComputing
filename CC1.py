import sys
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt

#x = [0.04, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75]
x = [x * 0.005 for x in range(8, 150)]
P = [0.25*ct.one_atm, 0.5*ct.one_atm, 0.75*ct.one_atm, ct.one_atm, 1.25*ct.one_atm, 1.5*ct.one_atm]
#T = [300]
ignition_temp = []
ignition_delay = []
result_file = open('wyniki_symulacji.txt', 'w')
result_file2 = open('temperatura_i_opoznienie_samozaplonu.txt', 'w')

for i in x:                     #dla kolejnych skladow mieszaniny
    print 'x = %f' % (i)
    result_file.write('\nx = %f\n' % (i))
    result_file2.write('\nx = %f\n' % (i))
    for c in P:                 #zmieniam cisnienie
       # for t in T:             #zmieniam temperature
            result_file.write('p = %f\n' % (c))
            j = (1-i)*0.21
            k = (1-i)*0.79
            gri3 = ct.Solution('gri30.cti')
            gri3.TPX = 1000.0, c, 'H2:'+str(i)+', O2:'+str(j)+', N2:'+str(k)+''
            r = ct.IdealGasReactor(gri3)
    
            sim = ct.ReactorNet([r])
            time = 0.0
            times = np.zeros(100)
            data = np.zeros((100,4))
    
            Tmax = 0
            ignition_time = 0
            OH = 0
        
            result_file.write('%10s %10s %10s %14s \n' % ('t [s]','T [K]','P [Pa]','u [J/kg]'))
        
            for n in range(100):
                time += 1.e-5
                sim.advance(time)
                times[n] = time * 1e3  # time in ms
                data[n,0] = r.T
                data[n,1:] = r.thermo['OH','H','H2'].X
                result_file.write('%e %f %f %e\n' % (sim.time, r.T, r.thermo.P, r.thermo.u))
    
                if r.thermo['OH'].X > OH:
                    OH = r.thermo['OH'].X
                    Tmax = r.T
                    ignition_time = time
                    ignition_temp.append(Tmax)
                    ignition_delay.append(ignition_time)
        
    result_file2.write('%s %s %s\n' % ('P [Pa]', 'T [K]', 't [s]'))
    
    for index in range(0, len(P)):
        result_file2.write('%f %f %f\n' % (P[index], ignition_temp[index], ignition_delay[index]))

    ignition_temp = []
    ignition_delay = []

    plt.clf()
    plt.plot(times, data[:,0])
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (K)')
    plt.savefig('wykres'+str(i)+'.png')

result_file.close()
result_file2.close()
"""
    plt.clf()
    plt.subplot(2, 2, 1)
    plt.plot(times, data[:,0])
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (K)')
    plt.subplot(2, 2, 2)
    plt.plot(times, data[:,1])
    plt.xlabel('Time (ms)')
    plt.ylabel('OH Mole Fraction')
    plt.subplot(2, 2, 3)
    plt.plot(times, data[:,2])
    plt.xlabel('Time (ms)')
    plt.ylabel('H Mole Fraction')
    plt.subplot(2, 2, 4)
    plt.plot(times,data[:,3])
    plt.xlabel('Time (ms)')
    plt.ylabel('H2 Mole Fraction')
    plt.tight_layout()
    plt.savefig('wykres'+str(i)+'.png')
"""