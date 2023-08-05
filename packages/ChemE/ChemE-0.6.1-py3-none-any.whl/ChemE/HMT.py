

Churchill = lambda Re,Pr:.3+(.62*Re**.5*Pr**(1/3))/(1+(.4/Pr)**(2/3))**.25*(1+(Re/282000)**(5/8))**(4/5)

class Fin(object):
    def __init__(self, Tb, Tinf,h,k,L,P):
        self.Tb = Tb
        self.Tinf = Tinf
        self.h = h
        self.k = k
        self.L = L
        self.P = P
    def case_c(self,x):
        pass

