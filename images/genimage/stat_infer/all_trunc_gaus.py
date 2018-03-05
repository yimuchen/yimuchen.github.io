#!/bin/env python
#-------------------------------------------------------------------------------
#
#  Filename    : all_trunc_gaus.py
#  Description : Matplotlib file for generating allthe various Truncated
#                Gaussians determined describe in the article
#  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
#
#
#-------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as spc
from scipy.integrate import quad
from scipy.optimize import ridder
from scipy.optimize import root
from scipy.optimize import minimize_scalar

def gaussian( x, mu ,sigma ):
    return np.exp( -(x-mu)*(x-mu)/(2*sigma**2)) / (sigma*np.sqrt(2*np.pi))

def gaussian_cdf( x, mu, sigma):
    return 1/2 * (1 + spc.erf((x-mu)/(np.sqrt(2)*sigma)))

def TrucGaus(x,mu,sigma):
    return gaussian(x,mu,sigma) / (gaussian_cdf(100,mu,sigma) - gaussian_cdf(0,mu,sigma) )

def expval(mu,sigma):
    def intgrad(x,mu,sigma):
        return x*TrucGaus(x,mu,sigma)
    return quad( intgrad, 0, 100, args=(mu,sigma))[0]

def varval(mu,sigma):
    def intgrad(x,mu,sigma):
        ex = expval(mu,sigma)
        return (x-ex)*(x-ex) * TrucGaus(x,mu,sigma)
    return np.sqrt(quad( intgrad, 0, 100, args=(mu,sigma))[0])

x = np.linspace(0,100,101,endpoint=True)

def fsolve1(x):
    return varval(80,x) - 20
def fsolve2(x):
    return expval(x,20) - 80
def fsolve3(x):
    mu,sigma = x[0], x[1]
    return [expval(mu,sigma)-80,varval(mu,sigma)-20]

mu = [0,0,0,0]
sigma = [0,0,0,0]
mu[0],sigma[0] = 80,20
mu[1],sigma[1] = 80,ridder(fsolve1,10,30)
mu[2],sigma[2] = ridder(fsolve2,60,95),20
solved = root(fsolve3,[100,50],tol=10**-8).x
mu[3],sigma[3] = solved[0],solved[1]

def ratio(mu,sigma):
    return 100*quad(TrucGaus,0,65,args=(mu,sigma))[0]

for i in range(0,4):
    plt.plot( x,
        TrucGaus(x,mu[i],sigma[i]),
        label=r"$G_{{T,{}}}:\mu={:.1f}, \sigma={:.1f}, e={:.1f}, \sqrt{{v}}={:.1f}$, Below 65pts={:.1f}%".format(
            i,
            mu[i],sigma[i],
            expval(mu[i],sigma[i]),
            varval(mu[i],sigma[i]),
            ratio(mu[i],sigma[i])
            )
        )

plt.xlabel("Score")
plt.ylabel("Probability density")
plt.xlim(0,100)
plt.ylim(ymin=0)
plt.legend()
plt.tight_layout()
plt.savefig('all_trunc_gauss.png')

for i in range(0,4):
    for j in range(i+1,4):
        def dist(x):
            firstcdf = quad(TrucGaus,0,x,args=(mu[i],sigma[i]))[0]
            secondcdf = quad(TrucGaus,0,x,args=(mu[j],sigma[j]))[0]
            return  -(firstcdf-secondcdf)**2
        maxx = minimize_scalar( dist, [0,100], method='bounded',bounds=[0,100]).x
        distmax = np.sqrt(-dist(maxx))
        print(i,j,maxx,(spc.kolmogorov(distmax)/distmax)**2)
