#@author ol-<( ConciseVerbosity18

import numpy as np
import pandas as pd
import os
from scipy.optimize import fsolve
from scipy.integrate import quad
from numpy import NaN
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


kb = 1.38064852e-23
avnum = 6.022e23
c_light = 299792458
pi = 3.141592653589
_ROOT = os.path.abspath(os.path.dirname(__file__))
def assure_path(path):
    return os.path.join(_ROOT, path)
def read_in_table(path, index):
    table =  pd.read_csv(assure_path(path), delimiter=' ').astype(float, errors='ignore').set_index(index)
    return table
def lame_doc(f = 'Thermo.py'):
    path1 = assure_path(f)
    text = ''
    with open(path1,'r') as fil1:
        text = fil1.read()
    with open('lame_doc.txt','w') as fil:
        fil.write(text)
    return

def strf(s):
    try:
        s = float(s)
    except ValueError:
        s = str(s)
    return s
def str0(s):
    try:
        s = float(s)
    except ValueError:
        s = 0
    return s
def reminder(*val):
    val = [val]
    if NaN in val:
        print('One of the inputs to this function is not a number')
#todo make Z have float column names
Table_B1 = pd.read_csv(assure_path(os.path.join('Data_files', 'Table_B1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('name')
Table_B1['acentric'] = pd.to_numeric(Table_B1['acentric'], errors='coerce')
Table_B1 = Table_B1.transpose()
Table_B2 = pd.read_csv(assure_path(os.path.join('Data_files', 'Table_B2.txt')), delimiter=' ').astype(float, errors='ignore').set_index('name').transpose()
Table_B2 = Table_B2.transpose()
Table_Lee_Kesler_Z0 = pd.read_csv(assure_path(os.path.join('Data_files', 'Lee_Kesler_Z0.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_Lee_Kesler_Z0.columns = list(map(lambda x: strf(x),Table_Lee_Kesler_Z0.keys()))
Table_Lee_Kesler_Z1 = pd.read_csv(assure_path(os.path.join('Data_files', 'Lee_Kesler_Z1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_Lee_Kesler_Z1.columns = list(map(lambda x: strf(x),Table_Lee_Kesler_Z1.keys()))
Table_E1 = pd.read_csv(assure_path(os.path.join('Data_files', 'Table_E1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('t_(c)')
Table_HR0 = pd.read_csv(assure_path(os.path.join('Data_files', 'HR0.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_HR1 = pd.read_csv(assure_path(os.path.join('Data_files', 'HR1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_PHI0 = pd.read_csv(assure_path(os.path.join('Data_files', 'phi0.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
TablePHI1 = pd.read_csv(assure_path(os.path.join('Data_files', 'phi1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_SR0 = pd.read_csv(assure_path(os.path.join('Data_files', 'SR0.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_SR1 = pd.read_csv(assure_path(os.path.join('Data_files', 'SR1.txt')), delimiter=' ').astype(float, errors='ignore').set_index('tr')
Table_CP_gases = pd.read_csv(assure_path(os.path.join('Data_files', 'CP_gases.txt')), delimiter=' ').astype(float, errors='ignore').set_index('name').transpose()
Table_C4 = pd.read_csv(assure_path(os.path.join('Data_files', 'Table_C4.txt')), delimiter=' ').astype(float, errors='ignore').set_index('name').transpose()
Table_Super_Steam = pd.read_csv(assure_path(os.path.join('Data_files', 'Superheat.txt')),delimiter=' ').astype(float, errors='ignore').set_index('P/kPa').transpose()
#todo change substance to search for name and autofill. Default all none and parameter autofill=True
def show_variables():
    options = ['kb', 'avnum', 'c_light', 'pi', 'Table_B1', 'Table_B2', 'Table_Lee_Kesler_Z0', 'Table_Lee_Kesler_Z1', 'Table_E1', 'Table_HR0', 'Table_HR1', 'Table_PHI0', 'TablePHI1', 'Table_SR0', 'Table_SR1']
    print(options)
    return
def search_steam(pressures:list,types:str,temperatures='all'):
    table = pd.DataFrame()
    for i,val in enumerate(pressures):
        pressures[i] = str(val) + '_' + types

    if temperatures == 'all':
        table = Table_Super_Steam[pressures]
    else:
        for i, val in enumerate(temperatures):
            temperatures[i] = str(val)
        table = Table_Super_Steam[pressures][temperatures]
    return table
def view_valid_temps(pressure):
    table = Table_Super_Steam[str(pressure) + '_H'].dropna()
    print(table.index[2:])
def find_hi_lo(num, options):
    hi = 0
    low = 0
    highnum = None
    lownum = None
    try:
        while True:
            if options[low] <= num:
                low +=1
            elif options[low]>num:
                break
    except IndexError:
        low -= 1
        lownum = options[low]
    op = options[::-1]
    try:
        while True:
            if op[hi] >= num:
                hi +=1
            elif op[hi]<num:
                break
    except IndexError:
        hi -= 1
        highnum = op[hi]
    highnum = op[hi] if highnum is None else highnum
    lownum = options[low] if lownum is None else lownum
    return highnum, lownum
def find_hi_lo2(num, options):
    if num in options:
        return num,num
    hi = 0
    low = 0
    highnum = None
    lownum = None
    try:
        while True:
            if options[low] <= num:
                low +=1
            elif options[low]>num:
                break
    except IndexError:
        low -= 1
        lownum = options[low]
    op = options[::-1]
    try:
        while True:
            if op[hi] >= num:
                hi +=1
            elif op[hi]<num:
                break
    except IndexError:
        hi -= 1
        highnum = op[hi]
    highnum = op[hi] if highnum is None else highnum
    lownum = options[low] if lownum is None else lownum
    return highnum, lownum
def get_steam_value(pressure,temperature):
    def stripextra(l: list):
        for i, val in enumerate(l):
            ii = 0
            while val[ii].isdigit():
                ii += 1
                if ii >= len(val):
                    break
            try:
                l[i] = int(l[i][:ii])
            except ValueError:
                print(l[i],l[i][ii])
        return l

    tempoptions = stripextra(list(Table_Super_Steam.index[2:]))
    tempoptions = list(set(tempoptions))
    tempoptions.sort()
    pressoptions = stripextra(list(Table_Super_Steam.columns))
    pressoptions = list(set(pressoptions))
    pressoptions.sort()
    Ps = find_hi_lo2(pressure,pressoptions)
    Ts = find_hi_lo2(temperature,tempoptions)
    H = ('H',Table_Super_Steam[str(Ps[0]) + '_H'][str(Ts[0])], Table_Super_Steam[str(Ps[1]) + '_H'][str(Ts[1])])
    U = ('U',Table_Super_Steam[str(Ps[0]) + '_U'][str(Ts[0])], Table_Super_Steam[str(Ps[1]) + '_U'][str(Ts[1])])
    V = ('V',Table_Super_Steam[str(Ps[0]) + '_V'][str(Ts[0])], Table_Super_Steam[str(Ps[1]) + '_V'][str(Ts[1])])
    S = ('S',Table_Super_Steam[str(Ps[0]) + '_S'][str(Ts[0])], Table_Super_Steam[str(Ps[1]) + '_S'][str(Ts[1])])
    table = pd.DataFrame([H,U,V,S], columns=['Type',Ts[0],Ts[1]])
    return table
def PxyWilson(T,V1,V2,a12,a21,Psat1,Psat2,params1,params2,R = 8.314):
    ln = np.log
    y1a = []
    x1s = np.linspace(0,1)
    Ps = []
    Λ12 = lambda T: V2/V1*np.exp(-a12/R/T)
    Λ21 = lambda T: V1/V2*np.exp(-a21/R/T)
    grt = lambda T,x1: -(x1*ln(x1 + (1-x1)*Λ12(T)) + (1-x1)*ln((1-x1)+x1*Λ21(T)))
    gam1 = lambda T,x1: np.exp(-ln(x1 + (1-x1)*Λ12(T))+(1-x1)*(Λ12(T)/(x1+(1-x1)*Λ12(T))-Λ21(T)/(x1*Λ21(T) + (1-x1))))
    gam2 = lambda T,x1: np.exp(-ln((1-x1)+x1*Λ21(T)) + x1*(Λ21(T)/((1-x1)+x1*Λ21(T))-Λ12(T)/((1-x1)*Λ12(T) + x1)))
#     psat = lambda T,a,b,c,d,e: np.exp(a+b/T + c*ln(T) + d*T**e)
    for x1 in x1s:
        x2 = 1-x1
        P = Psat1(T,*params1)*x1*gam1(T,x1)+Psat2(T,*params2)*x2*gam2(T,x1)
        Ps.append(P)
        y1 = x1*Psat1(T,*params1)*gam1(T,x1)/P
        y1a.append(y1)
#     plt.plot(Ps,x1s,'r-',label='x1')
#     plt.plot(Ps,y1a,'k-',label='y1')
    plt.plot(x1s,Ps,'r-',label='x1')
    plt.plot(y1a,Ps,'k-',label='y1')
    plt.legend()
    plt.title('PxyWilson')
    plt.show()
    return

ex = lambda T,a,b,c,d,e: T
def TxyWilson(P,V1,V2,a12,a21,Psat1:ex,Psat2:ex,params1,params2,R=8.314):
    ln =np.log
    y1a = []
    x1s = np.linspace(0,1)
    Ts = []
    Λ12 = lambda T: V2/V1*np.exp(-a12/R/T)
    Λ21 = lambda T: V1/V2*np.exp(-a21/R/T)
    grt = lambda T,x1: -(x1*ln(x1 + (1-x1)*Λ12(T)) + (1-x1)*ln((1-x1)+x1*Λ21(T)))
    gam1 = lambda T,x1: np.exp(-ln(x1 + (1-x1)*Λ12(T))+(1-x1)*(Λ12(T)/(x1+(1-x1)*Λ12(T))-Λ21(T)/(x1*Λ21(T) + (1-x1))))
    gam2 = lambda T,x1: np.exp(-ln((1-x1)+x1*Λ21(T)) + x1*(Λ21(T)/((1-x1)+x1*Λ21(T))-Λ12(T)/((1-x1)*Λ12(T) + x1)))
    psat = lambda T,a,b,c,d,e: np.exp(a+b/T + c*ln(T) + d*T**e)
    for x1 in x1s:
        x2 = 1-x1
        fun = lambda T:  x1*Psat1(T,*params1)*gam1(T,x1)+gam2(T,x1)*x2*Psat2(T,*params2)-P
        T = fsolve(fun,300)[0]
        Ts.append(T)
        y1a.append(x1*Psat1(T,*params1)*gam1(T,x1)/P)
#     plt.plot(Ts,x1s,'r-',label='x1')
#     plt.plot(Ts,y1a,'k-',label='y1')
    plt.plot(x1s,Ts,'r-',label='x1')
    plt.plot(y1a,Ts,'k-',label='y1')
    plt.legend()
    plt.title('TxyWilson')
    plt.show()
    return
class Substance(object):

    def __init__(self, name=None, T=NaN, P = NaN, state='g', Tc= NaN, molar_mass=NaN, Pc = NaN, Tr=NaN, Pr=NaN, acentric=NaN, R=8.314e-5, autofill=True,nu = np.NaN):
        self.Tc = Tc
        self.P = P
        self.T = T
        self.Pc = Pc
        self.name = name
        self.R = R
        self.acentric = acentric
        self.molar_mass = molar_mass
        self.state = state
        self.nu = nu
        if autofill:
            try:
                self.Tc = Table_B1[self.name]['tc/k']
                self.Pc = Table_B1[self.name]['pc/bar']
                self.acentric = Table_B1[self.name]['acentric']
                self.molar_mass = Table_B1[self.name]['molar_mass']

            except KeyError:
                print('Your substance name was not in the table')
        try:
            self.Tr = float(self.T/self.Tc) if Tr is  NaN else Tr
            self.Pr = float(self.P/self.Pc) if Pr is  NaN else Pr
            self.Vc = self.R*self.Tc/self.Pc
            self.alphaSRK = (1 + (.48 + 1.574 * self.acentric - .176 * self.acentric ** 2) * (1 - self.Tr ** .5)) ** 2
            self.alphaPR = (1 + (.37464 + 1.54226 * self.acentric - .26992 * self.acentric ** 2) * (1 - self.Tr ** .5)) ** 2
            self.EOSconts = {'vdW': [1, 0, 0, 1 / 8, 27 / 64, 3 / 8],
                             'RK': [self.Tr ** (-1 / 2), 1, 0, 0.08664, .42748, 1 / 3],
                             'SRK': [self.alphaSRK, 1, 0, .08664, .42748, 1 / 3],
                             'PR': [self.alphaPR, 1 + 2 ** .5, 1 - 2 ** .5, .07780, .45724, .30740]}
        except KeyError:
            print('EOS data or critical values for',self.name)
        try:
            self.cpA = str0(Table_CP_gases[self.name]['a'])
            self.cpB = str0(Table_CP_gases[self.name]['b'])*10**-3
            self.cpC = str0(Table_CP_gases[self.name]['c'])*10**-6
            self.cpD = str0(Table_CP_gases[self.name]['d'])*10**5
            self.cpR = str0(Table_CP_gases[self.name]['cpig/r'])
            self.cpRR = str0(Table_CP_gases[self.name]['cpig/r'])*self.R
        except KeyError:
            print('No gaseous cp data for substance')
        try:
            self.dH = strf(Table_C4[self.name + '_(' + self.state + ")"]['dhf298'])
            self.dG = strf(Table_C4[self.name + '_(' + self.state + ")"]['dgf298'])

        except KeyError:
            print('No dH or Gibss for substance', self.name)
            self.dG = np.NaN
            self.dH = np.NaN
    def gas_cp(self, T=None):
        if T is None:
            T = self.T
        return self.cpA + self.cpB*T + self.cpC*T**2 + self.cpD*T**-2
    def gas_cp_int(self,T1,T2):
        T = T2-T1
        return self.cpA*T + self.cpB * T**2 + self.cpC * T ** 3 + -self.cpD * T ** -1

    def change_attr(self,attr:str,value:str):
        setattr(self,attr,value)
        return getattr(self,attr)
    # def change_acentric(self,w):
    #     self.acentric = w
    #     self.alphaSRK = (1 + (.48 + 1.574 * self.acentric - .176 * self.acentric ** 2) * (1 - self.Tr ** .5)) ** 2
    #     self.alphaPR = (1 + (.37464 + 1.54226 * self.acentric - .26992 * self.acentric ** 2) * (
    #                 1 - self.Tr ** .5)) ** 2
    #     self.EOSconts = {'vdW': [1, 0, 0, 1 / 8, 27 / 64, 3 / 8], 'RK': [self.Tr ** (-1 / 2), 1, 0, 0.08664, .42748, 1 / 3],
    #                 'SRK': [self.alphaSRK, 1, 0, .08664, .42748, 1 / 3],
    #                 'PR': [self.alphaPR, 1 + 2 ** .5, 1 - 2 ** .5, .07780, .45724, .30740]}
    #     return

    def vdW(self,guess):
        which = 'vdW'
        alpha = self.EOSconts[which][0]
        sigma = self.EOSconts[which][1]
        epsilon = self.EOSconts[which][2]
        omega = self.EOSconts[which][3]
        psi = self.EOSconts[which][4]
        Zc = self.EOSconts[which][5]
        Beta = omega*self.Pr/self.Tr
        q = psi*alpha/omega/self.Tr
        eq = lambda Z: 1+Beta-q*Beta*((Z-Beta)/(Z+epsilon*Beta)/(Z+sigma*Beta))-Z
        reminder(guess)
        return fsolve(eq,guess)[0]

    def RK(self,guess):
        which = 'RK'
        try:
            alpha = self.EOSconts[which][0]
            sigma = self.EOSconts[which][1]
            epsilon = self.EOSconts[which][2]
            omega = self.EOSconts[which][3]
            psi = self.EOSconts[which][4]
            Zc = self.EOSconts[which][5]
        except KeyError:
            raise NameError('Acentric Factor not defined')
        Beta = omega * self.Pr / self.Tr
        q = psi * alpha / omega / self.Tr
        eq = lambda Z: 1 + Beta - q * Beta * ((Z - Beta) / (Z + epsilon * Beta) / (Z + sigma * Beta)) - Z
        reminder(guess)
        return fsolve(eq, guess)[0]

    def SRK(self,guess):
        which = 'SRK'
        try:
            alpha = self.EOSconts[which][0]
            sigma = self.EOSconts[which][1]
            epsilon = self.EOSconts[which][2]
            omega = self.EOSconts[which][3]
            psi = self.EOSconts[which][4]
            Zc = self.EOSconts[which][5]
        except KeyError:
            raise NameError('Acentric Factor not defined')
        Beta = omega * self.Pr / self.Tr
        q = psi * alpha / omega / self.Tr
        eq = lambda Z: 1 + Beta - q * Beta * ((Z - Beta) / (Z + epsilon * Beta) / (Z + sigma * Beta)) - Z
        reminder(guess)
        return fsolve(eq, guess)[0]

    def PR(self,guess):
        which = 'PR'
        try:
            alpha = self.EOSconts[which][0]
            sigma = self.EOSconts[which][1]
            epsilon = self.EOSconts[which][2]
            omega = self.EOSconts[which][3]
            psi = self.EOSconts[which][4]
            Zc = self.EOSconts[which][5]
        except KeyError:
            raise NameError('Acentric Factor not defined')
        Beta = omega * self.Pr / self.Tr
        q = psi * alpha / omega / self.Tr
        eq = lambda Z: 1 + Beta - q * Beta * ((Z - Beta) / (Z + epsilon * Beta) / (Z + sigma * Beta)) - Z
        reminder(guess)
        return fsolve(eq, guess)[0]

    def double_interp_LK(self, Prs, Trs):
        if self.acentric is NaN:
            raise NameError('Acentric Factor Not Defined')
        t0 = Table_Lee_Kesler_Z0
        t1 = Table_Lee_Kesler_Z1
        Z0 = np.array([[t0[Prs[0]][Trs[0]], t0[Prs[0]][Trs[1]]], [t0[Prs[1]][Trs[0]], t0[Prs[1]][Trs[1]]]])
        Z1 = np.array([[t1[Prs[0]][Trs[0]], t1[Prs[0]][Trs[1]]], [t1[Prs[1]][Trs[0]], t1[Prs[1]][Trs[1]]]])
        Xm = self.Pr
        Ym = self.Tr
        Xf = float((Xm - float(Prs[0])) / (float(Prs[1]) - float(Prs[0])))
        Yf = float((Ym - float(Trs[0])) / (float(Trs[1]) - float(Trs[0])))
        Z0mY1 = (Z0[1,0] - Z0[0,0]) * Xf + Z0[0,0]
        Z0mY2 = (Z0[1, 1] - Z0[0, 1]) * Xf + Z0[0, 1]

        Z1mY1 = (Z1[1, 0] - Z1[0, 0]) * Xf + Z1[0, 0]
        Z1mY2 = (Z1[1, 1] - Z1[0, 1]) * Xf + Z1[0, 1]

        Z0 = (Z0mY2 - Z0mY1) * Yf + Z0mY1
        Z1 = (Z1mY2 - Z1mY1) * Yf + Z1mY1

        Z = Z0 + self.acentric*Z1
        reminder(Prs,Trs)
        return Z

    def z_from_LK(self):
        t0 = Table_Lee_Kesler_Z0
        t1 = Table_Lee_Kesler_Z1
        try:
            Z0 = t0[self.Pr][self.Tr]
            Z1 = t1[self.Pr][self.Tr]
            return  Z0 + self.acentric*Z1
        except KeyError:
            return self.double_interp_LK(find_hi_lo(self.Pr,t0.keys()),find_hi_lo(self.Tr,t0.index))

    def Pitzer(self):
        if self.acentric is NaN:
            raise NameError('Acentric factor not defined')

        B0 = .083-.422/self.Tr**1.6
        B1 = .139-.172/self.Tr**4.2
        reminder(self.Tr,self.Pr)
        return 1 + B0 * self.Pr / self.Tr + self.acentric * B1 * self.Pr / self.Tr

def mixture_cp(subs:Substance,T1,T2):
    pass
#todo add Lee_Kesler
#todo add liquid versions
if __name__ == '__main__':
    sub = Substance('methanol',400,1)
    print(sub.Pc)
    tab = Table_Super_Steam
    # print(tab.columns)
    table =search_steam([10, 8600], 'S')
    patHH = '_H'
    # grouped = tab.groupby(tab.columns.str.extract(patHH, expand=False), axis=1)
    view_valid_temps(150)
    print(get_steam_value(4570,453))
    print(Substance('iso_butane').cpA)
    print(Substance('Sulfur').dH)