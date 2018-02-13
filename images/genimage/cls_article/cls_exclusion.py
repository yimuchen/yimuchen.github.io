import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import binom
from scipy.optimize import brentq
from scipy.interpolate import interp1d


def likelihood(x,N,theta):
    return binom.pmf(x,N,(1+theta)/2)

def y_from_x(x,N,theta):
    return -2 * np.log( likelihood(x,N,theta) / likelihood(x,N,0) )

def get_y_p(N,theta):
    x = np.linspace(0,N,N+1,endpoint=True)
    y = y_from_x(x,N,theta)
    p_alt = likelihood(x,N,theta)
    p_null =  likelihood(x,N,0)

    return y, p_null, p_alt


def get_confidence(x,N,theta):
    y, p_null, p_alt = get_y_p(N,theta)
    yobs = y_from_x(x,N,theta)

    clb = 0
    clbps = 0
    for idx, yinst in enumerate(y) :
        if yinst >= yobs:
            clb = clb + p_null[idx]
            clbps = clbps + p_alt[idx]
    return clbps / clb

def find_theta_ex(x,N):
    def f(v):
        return get_confidence(x,N,v)-0.05
    return brentq(f,0,0.9999)

def get_theta_prob(N):
    prob_theta = {}
    prob_sum = 0
    for x in range(0,N):
        print("Finding theta probability for observable x={:.3f},N={}".format((x/N-0.5)*2,N) )
        theta_ex = find_theta_ex(x,N)
        print("Found theta={:.3f}".format((x/N-0.5)*2,N) )
        prob_sum  = prob_sum + likelihood(x,N,0)
        if theta_ex in prob_theta:
            prob_theta[theta_ex] = prob_theta[theta_ex] + likelihood(x,N,0);
        else:
            prob_theta[theta_ex] = likelihood(x,N,0)

    return prob_theta

def get_quintiles( prob ):
    from collections import OrderedDict
    prob = OrderedDict(sorted(prob.items()))
    central = [key * value for key,value in prob.items()]
    central = sum(central)/sum(prob.values())

    prob_sum = 0
    freez2 = freez1 = False
    min2 = 0
    min1 = 0
    for term in prob.items():
        if min2 >=0 and not freez2:
            min2 = term[0]
        if min1 >=0 and not freez1:
            min1 = term[0]
        prob_sum = prob_sum + term[1]
        if prob_sum > 0.02275 and not freez2:
            freez2 = True
        if prob_sum > 0.1587 and not freez1:
            freez1 = True

    prob_sum = 0
    freez1 = freez2 = False
    plus1 = 0
    plus2 = 0

    for term in reversed(prob.items()):
        if plus1 >=0 and not freez1:
            plus1 = term[0]
        if plus2 >=0 and not freez2:
            plus2 = term[0]
        prob_sum = prob_sum + term[1]
        if prob_sum > 0.02275 and not freez2:
            freez2 = True
        if prob_sum > 0.1587 and not freez1:
            freez1 = True

    return central, min2, min1, plus1, plus2

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)

N1 = 40
N2 = 400

result1 = get_theta_prob(N1)
result2 = get_theta_prob(N2)

prob1 = [prob/sum(result1.values()) for prob in result1.values() ]
prob2 = [(N2/N1)/3* prob/sum(result2.values()) for prob in result2.values() ]

print(sum(result1.values()), sum(result2.values()),)

ax2.plot( prob1, result1.keys(),
    label=r"$R_{null}(\theta_{ex}|N)$"+"  N={}".format(N1) )
ax2.plot( prob2, result2.keys(),
    label=r"$R_{null}(\theta_{ex}|N)$"+"  N={}".format(N2) )
ax1.set_ylabel(r"$\theta_{ex}$")
ax2.set_xlabel(r"$P(\theta_{ex}|N)$")
ax2.set_xlim(xmin=0)
ax2.legend()


quin1 = get_quintiles(result1)
quin2 = get_quintiles(result2)


def draw_connect(axA, axB, q, r , qp, x):
    color = 'red' if qp ==0 else \
            'orange' if qp == 1 or qp == 4 else \
            'green'
    f = interp1d( list(r.keys()), list(r.values()) )
    x1 = 0 if x!= 0 else 1
    x2 = f(q[qp])  if x != 0  else 0
    print(q[qp],x2)

    axA.add_artist(
        patches.ConnectionPatch(
            xyA=(x1,q[qp]),
            xyB=(x2, q[qp]),
            coordsA="data", coordsB="data",
            axesA= axA, axesB=axB,
            color=color,
            zorder = 1000,
            linestyle = '--'
        )
    )

print(quin1)
print(quin2)
draw_connect(ax1, ax2, quin1, result1, 0 , 1 )
draw_connect(ax1, ax2, quin1, result1, 1 , 1 )
draw_connect(ax1, ax2, quin1, result1, 2 , 1 )
draw_connect(ax1, ax2, quin1, result1, 3 , 1 )
draw_connect(ax1, ax2, quin1, result1, 4 , 1 )

draw_connect(ax3, ax2, quin2, result2, 0 , 0 )
draw_connect(ax3, ax2, quin2, result2, 1 , 0 )
draw_connect(ax3, ax2, quin2, result2, 2 , 0 )
draw_connect(ax3, ax2, quin2, result2, 3 , 0 )
draw_connect(ax3, ax2, quin2, result2, 4 , 0 )


ax1.add_patch(
    patches.Rectangle(
        (0,quin1[1]), 1, quin1[4]-quin1[1],
        color='yellow',
        linewidth=0,
    )
)

ax1.add_patch(
    patches.Rectangle(
        (0,quin1[2]), 1, quin1[3]-quin1[2],
        color='green',
        linewidth=0,
    )
)


ax3.add_patch(
    patches.Rectangle(
        (0,quin2[1]), 1, quin2[4]-quin2[1],
        color='yellow',
        linewidth=0,
    )
)

ax3.add_patch(
    patches.Rectangle(
        (0,quin2[2]), 1, quin2[3]-quin2[2],
        color='green',
        linewidth=0,
    )
)

ttest = 0.25
tobs1 = find_theta_ex(int(N1*(0.5+ttest/2)),N1)
tobs2 = find_theta_ex(int(N2*(0.5+ttest/2)),N2)
ax1.plot( [0,1],[tobs1,tobs1], color='k', linewidth=3, label=r"$\theta_{ex}(x=0.25)$="+"{:.2f}".format(tobs1))
ax3.plot( [0,1],[tobs2,tobs2], color='k', linewidth=3, label=r"$\theta_{ex}(x=0.25)$="+"{:.2f}".format(tobs2))
ttest = 0.10
tobs1 = find_theta_ex(int(N1*(0.5+ttest/2)),N1)
tobs2 = find_theta_ex(int(N2*(0.5+ttest/2)),N2)
ax1.plot( [0,1],[tobs1,tobs1], color='blue', linewidth=3, label=r"$\theta_{ex}(x=0.10)$="+"{:.2f}".format(tobs1))
ax3.plot( [0,1],[tobs2,tobs2], color='blue', linewidth=3, label=r"$\theta_{ex}(x=0.10)$="+"{:.2f}".format(tobs2))
ax1.legend()
ax3.legend()
#ax1.set_yscale('log')
ax2.set_zorder(-1)
#ax2.set_xscale('log')
ax2.set_xlim(xmin = 0)

plt.tight_layout()
plt.savefig("cls_exclusion.png")
