import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Control objects
N = 40
x = np.linspace(0,N,N+1,endpoint=True)
thetalist = [0,0.3,0.5,0.8]
ylist     = [];
for theta in thetalist:
    rho = (1 + theta)/2
    y = binom.pmf(x,N,rho)
    plt.plot( (x/N-0.5)*2 , y , label=r'$\theta$={}'.format(theta) )
    ylist.append(y)

plt.xlabel(r'$x$')
plt.ylabel(r'$L(x|\theta)$')
plt.legend()
plt.ylim(ymin=0)
plt.xlim(0,1)

# Add additional vertical line for highlighting
plt.axvline(x=0.1, color='gray', linestyle='--')
plt.text(0.1,0.15,
    r"x=0.1,   y($\theta=0.3$)={:.3f}".format(-2*np.log(ylist[1][2]/ylist[0][2])),
    rotation=90)


plt.savefig('CLS_Likelihood.png')
