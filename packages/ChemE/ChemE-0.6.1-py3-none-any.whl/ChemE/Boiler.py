from scipy.optimize import fsolve, curve_fit
from numpy import log as ln
from scipy.integrate import odeint, quad
import numpy as np
from numpy import sin,cos,tan
from numpy import sinh, cosh,tanh
from numpy import pi
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import pandas as pd
from scipy.special import erf,erfc,erfinv,erfcinv
from prettytable import PrettyTable as pptt

def paste_to_df(s:str,sep=' ',rows=True,rowsplit='\n'):
    df = pd.DataFrame()
    if not rows:
        s = s.split(sep)
        df[1] = s
    else:
        s = s.split(rowsplit)
        s = list(map(lambda x: x.split(sep),s))
        ml = 0
        for row in s:
            ml = len(row) if len(row) > ml else ml
        for i, row in enumerate(s):
            while len(row)<ml:
                row.append(np.NaN)
            df[f'{i}'] = row
    return df
water_lcp = lambda T: (276370+-2090.1*T+8.125*T**2+-.014116*T**3+9.3701e-6*T**4)/18.01 #j/kg
water_lrho = lambda T: (-13.851+.64038*T-.0019124*T**2+1.8211e-6*T**3)*18.01 #kg/m3
def water_lk(T):
    stuff = [-0.432,0.0057255,-8.078E-06,1.861E-09]
    cool = sum(stuff[i]*T**i for i in range(len(stuff)))
    return cool #W/m/K
def water_lmu(T):
    a,b,c,d,e = -52.843,3703.6,5.866,-5.879E-29,10
    cool = np.exp(a+b/T+c*ln(T)+d*T**e)
    return cool #Pa*s
def water_lvp(T):
    a,b,c,d,e = 73.649,-7258.2,-7.3037,4.1653E-06,2
    cool = np.exp(a+b/T+c*ln(T)+d*T**e)
    return cool#Pa
def water_Hvap(T):
    Tc = 374+273.15
    a,b,c,d = 56600000,0.612041,-0.625697,0.398804
    Tr = T/Tc
    return a*(1-Tr)**(b+c*Tr+d*Tr**2)/18.01 #j/kg
def water_vk(T):
    a,b,c,d = 6.2041E-06,1.3973,0.0,0.0
    return a*T**b/(1+c/T+d/T**2)#w/m/K

def air_cp(T):
    a,b,c,d,e = 28958,9390,3012,7580,1484
    cool = a+b*(c/T/sinh(c/T))**2+d*(e/T/cosh(e/T))**2
    return cool/28.96 #j/kg/k
def air_k(T):
    a,b,c,d = 0.00031417,0.7786,-0.7116,2121.7
    return a*T**b/(1+c/T+d/T**2) #w/m/k
def air_mu(T):
    a,b,c,d = 1.425E-06,0.5039,108.3,0
    return a*T**b/(1+c/T+d/T**2) #Pa*s
air_rho_ig = lambda P,mw,R,T:P*mw/R/T
def dippr_print():
    stuff = '''water_lcp = lambda T: (276370+-2090.1*T+8.125*T**2+-.014116*T**3+9.3701e-6*T**4)/18.01 #j/kg/K
water_lrho = lambda T: (-13.851+.64038*T-.0019124*T**2+1.8211e-6*T**3)*18.01 #kg/m3
def water_lk(T):
    stuff = [-0.432,0.0057255,-8.078E-06,1.861E-09]
    cool = sum(stuff[i]*T**i for i in range(len(stuff)))
    return cool #W/m/K
def water_lmu(T):
    a,b,c,d,e = -52.843,3703.6,5.866,-5.879E-29,10
    cool = np.exp(a+b/T+c*ln(T)+d*T**e)
    return cool #Pa*s
def water_lvp(T):
    a,b,c,d,e = 73.649,-7258.2,-7.3037,4.1653E-06,2
    cool = np.exp(a+b/T+c*ln(T)+d*T**e)
    return cool#Pa
def water_Hvap(T):
    Tc = 374+273.15
    a,b,c,d = 56600000,0.612041,-0.625697,0.398804
    Tr = T/Tc
    return a*(1-Tr)**(b+c*Tr+d*Tr**2)/18.01 #j/kg
def water_vk(T):
    a,b,c,d = 6.2041E-06,1.3973,0.0,0.0
    return a*T**b/(1+c/T+d/T**2)#w/m/K

def air_cp(T):
    a,b,c,d,e = 28958,9390,3012,7580,1484
    cool = a+b*(c/T/sinh(c/T))**2+d*(e/T/cosh(e/T))**2
    return cool/28.96 #j/kg/k
def air_k(T):
    a,b,c,d = 0.00031417,0.7786,-0.7116,2121.7
    return a*T**b/(1+c/T+d/T**2) #w/m/k
def air_mu(T):
    a,b,c,d = 1.425E-06,0.5039,108.3,0
    return a*T**b/(1+c/T+d/T**2) #Pa*s
air_rho_ig = lambda P,mw,R,T:P*mw/R/T '''
    print(stuff)
def dT_lm(Thin,Thout,tcin,tcout):
    dT1 = Thin-tcout
    dT2 = Thout-tcin
    return (dT1-dT2)/ln(dT1/dT2)
avg = lambda x: sum(x)/len(x)
if __name__== '__main__':
    print(paste_to_df('204.9, 206.1, 203.9, 207.0, 203.5, 206.3, 203.5, 206.7, 205.8\n1.317, 1.318, 1.301, 1.307, 1.374, 1.323',', '))