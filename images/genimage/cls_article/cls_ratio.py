import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom


N = 40
x = np.linspace(0,N,N+1,endpoint=True)

def likelihood(x,theta):
    return binom.pmf(x,N,(1+theta)/2)

def y_from_x(x,theta):
    return -2 * np.log( likelihood(x,theta) / likelihood(x,0) )

def get_y_p(theta):
    y = y_from_x(x,theta)
    p_alt =  likelihood(x,theta)
    p_null =  likelihood(x,0)

    return y, p_null, p_alt

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

result1 = get_y_p(0.3)
result2 = get_y_p(0.6)

ax1.plot( result1[0], result1[1], label=r'$P_{null}(y | \theta = 0.3)$' )
ax1.plot( result1[0], result1[2], label=r'$P_{alt}(y | \theta = 0.3)$' )
ax2.plot( result2[0], result2[1], label=r'$P_{null}(y | \theta = 0.6)$' )
ax2.plot( result2[0], result2[2], label=r'$P_{alt}(y | \theta = 0.6)$' )

ax1.legend()
ax2.legend()

ax1.set_xlabel(r'$y=-2 ln\left(L_{alt}/L_{null}\right)$   $\theta=0.3$')
ax2.set_xlabel(r'$y=-2 ln\left(L_{alt}/L_{null}\right)$   $\theta=0.6$')
ax1.set_ylabel(r'$P(y|\theta)$')
# plt.legend()
ax1.set_ylim(ymin=0)
ax1.set_xlim(result1[0][-int(N/6)],result1[0][int(N/6)])
ax2.set_xlim(result2[0][-int(N/6)],result2[0][int(N/6)])


tobs = 0.2
x = int(N * (0.5 + tobs/2) )
yobs1 = y_from_x(x,0.3)
yobs2 = y_from_x(x,0.6)
textheight = 0.8 * max(
    max( np.amax( result1[1] ) , np.amax(result1[2] ) ),
    max(np.amax(result2[1]), np.amax(result2[2]))
     )
ax1.axvline(x=yobs1,color='gray',linestyle='--')
ax2.axvline(x=yobs2,color='gray',linestyle='--')
ax1.text(yobs1,textheight,r'Observed x={:.2f}, $y(\theta=0.3)$={:.3f}'.format(tobs,yobs1), rotation=90)
ax2.text(yobs2,textheight,r'Observed x={:.2f}, $y(\theta=0.6)$={:.3f}'.format(tobs,yobs2), rotation=90)

plt.tight_layout()

plt.savefig('CLS_ratio.png')
