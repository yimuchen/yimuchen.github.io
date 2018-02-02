---
layout: post
title: Introduction to the Confidence Level Diagram
description: Understanding how to interpret results and simple explanations as to what is being calculated
tags: [mathematics, statistics, physics ,particle physics]
modified: 2016-07-07
image:
  feature: thoughts.jpg
  credit: ensc
---

The confidence level diagram is one of the most common form of "conclusion diagrams" in particle physics, particularly in exotic searches.
Our usual form of conclusion is we say "it is highly unlikely that there is a particle with mass $X$ with such and such properties". The conclusion diagram we draw typically look like this:

<figure>
<a href="https://ghm.web.cern.ch/ghm/plots/public-results/publications/EXO-15-001/CMS-EXO-15-001_Figure_003-c.pdf">
<img src="https://ghm.web.cern.ch/ghm/plots/limitPlot_example.png" alt=""></a>
<figcaption>Example diagram from CMS plot style site</figcaption>
</figure>

In this diagram we say that:

* Everything observed (black dots) is within 2 $\sigma$ of the standard model(double coloured band)
* We could say that there is no apparent new $gg$ resonance with masses smaller than $3TeV$ with the colour-octet scalar model (where the pink line intersects the band).

I wanted to quickly go over what is being calculated and why we interpret it as such.

## The "fairness of a coin" experiment
To begin with lets consider our standard model of coins being "all coins have an equal chance of giving heads or tails when flipped". Now someone claims that they have found a way of manufacturing magic coins that can break our standard model. However, these coins break after one coin toss and are very expensive to produce. With a limited amount of coin tosses, what can one say about how different the magic coins are from our standard model?

### Defining the parameters / observables
First we need to be able to define how a coin could be different. For each coin, we assign a "unfairness factor" $\theta$:

>> $\theta:$ The probability of the coin giving a head minus the probability of the coin giving a tail (absolute value taken)

We could see that $\theta$ is definitely positive and our standard model declares that all $\theta$s for every coin should be at the minimal value 0. Now we could say.

Now we after $N$ coin tosses, we could obtain a observed unfairness $x$, notice that $x$ could be 1 even if $\theta$ is 0! In fact the chances that $x=0$ when $N$ is large is very small even if $\theta$ is 0! So the correct way of comparing the results is by the likelihood function $L(x \rvert \theta)$:

>> $L(x\rvert\theta)$: the probability of observing $x$ under the condition that the coin has a value unfairness factor of $\theta$

Here we are going to compare the likelihood of our standard model $\theta \neq 0$(otherwise called the null hypothesis), and out alternative model $\theta=\theta_\text{test}$ by the value:

$$
y = -2 \, \ln(Q) \equiv -2\, \ln\left( \frac{L_\text{alt}}{L_\text{null}} \right)
  = -2 \ln\left( \frac{L(x\rvert \theta_\text{alt})}{ L(x\rvert 0)} \right)
$$

For our actual experiment for $N$ tosses of real, physical magic coin, we get a unique value of $y$.


### Defining how "non-standard" our observed result is
Now, for a given $\theta$ we are trying to validate/disprove, we are interested in to probability distribution functions:

>> $P_\text{null}( y \rvert \theta_{alt})$: The probability of observing $y$ with a given testing $\theta_\text{alt}$ when the coin has a actual $\theta=\theta_\text{null}$

>> $P_\text{alt} (y \rvert \theta_{alt})$: The probability of observing $y$ with a given testing $\theta_\text{alt}$ when the coin has a actual $\theta=\theta_\text{alt}$

Using these two distributions, we could begin to see how we could interpret the experimental results. If the observed $y$ is closer to the central value of $P_\text{null}$, it is likely that the standard model is true and vice-versa. It could also tell you when your experiment might be insufficient to distinguish between the new and old if the two distribution have significant overlap.

<figure>
	<img src="{{sit.url}}/images/figures/2016-07-07-Distribution.png" alt="">
	<figcaption>Example taken from Physics Colloquium (2012) @ NTU by Kei-Feng Chen</figcaption>
</figure>

We could also see that due to the definition of $y$ and $P$, the $P_\text{null}$, will typically have a higher mean that $P_\text{alt}$.

For each observed $y_0$ value, we could define $CL_b$ as

$$
CL_b(y_0 , \theta_\text{alt}) \equiv \int_{y_0}^\infty P_\text{null}(y\rvert \theta_\text{alt}) dy
$$

And $CL_\text{s+b}$ as:

$$
CL_\text{s+b}(y_0 , \theta_\text{alt}) \equiv \int_{y_0}^\infty P_\text{alt}(y \rvert \theta_\text{alt}) dy
$$

The discriminating value $CL_s$ is called the **confidence level** of this observed $y_0$ to a standard model event as

$$
CL_s(y_0,\theta_\text{alt}) = \frac{CL_\text{s+b}}{CL_b}
$$


<figure>
	<img src="{{sit.url}}/images/figures/2016-07-07-ConfidenceLevel.png" alt="">
	<figcaption>Example taken from Physics Colloquium (2012) @ NTU by Kei-Feng Chen</figcaption>
</figure>

Since we could see that if this value is small it means two things:

   * This observed results lies closer towards the standard model distribution.
   * The two distributions are far apart enough for small values to occur.

The connection of this dicrimination value and the statistical intepretation of **confidence level** would be an article for next time.

We are going to take the convention of the scientific community of saying that if $CL_s <0.05$, the results are "statistically significant"; and if $CL_s < 10^{-6}$, the results indicate "a new discovery".

### Defining exclusion limit
For each $y_0$ value, there is a corresponding value of $\theta_\text{ex}(y_0)$ where $CL = 0.05$. Meaning that if we observe this $y_0$, then we can not tell if it is a statistical fluctuation of the standard model, of if it due to an alternative model with $\theta < \theta_\text{ex}$! So this our 95% confidence exclusion limit for a single observation.

Now from our theory/simulation, we could get the distribution of this $\theta_\text{ex}$ **if the standard model is right**! Typically, we plot this as a double banded region with $\theta$ as the $y$ axis.

<figure>
	<img src="{{sit.url}}/images/figures/2016-07-07-ConfidenceLevel_Cont.png" alt="">
	<figcaption>Confidence levels of coin toss experiments with 10 coin tosses, Example taken from Physics Colloquium (2012) @ NTU by Kei-Feng Chen</figcaption>
</figure>

In the above diagram, we say that by our 10 coin toss experiment, with the assumption that the standard model is right:

* We could exclude the models with $\theta > 0.59$ with 95% confidence.
* Any $\theta_{ex}$ obtained from a real experiment has a 95% chance to fall within the double band region.

So returning to our new coin experiment . If the theorists, say that the new coins have a unfairness factor of $0.95$, we could say we are able to verify this experiment with the 10 toss-budget that we have, but if they say the proposed unfairness factor is $0.2$, we say that we cannot would not be able to exclude this theory with 10 coin toss alone.

Also, if the observed exclusion $\theta$ is far deviating from the double side band (for example at $\theta_{ex}=0.91$), then we could say that this observation shows that our system is behaving very differently from the standard model!


## Corresponding variables in High Energy Physics
In high energy physics, the $x$ we want to observe is typically number of events, and the $\theta$ is typically the signal strength, with the theoretical value being $1$ and the standard model being $0$. So if the standard model could exclude $\theta$ up to $1$, then this theory could be disproved by our experiment, and if the observed exclusion is also similar to a predictions of the standard model, then there is a high chance that the standard model is correct.

Back to the first example diagram:
<figure>
	<a href="https://ghm.web.cern.ch/ghm/plots/public-results/publications/EXO-15-001/CMS-EXO-15-001_Figure_003-c.pdf"><img src="https://ghm.web.cern.ch/ghm/plots/limitPlot_example.png" alt=""></a>
	<figcaption>Example diagram from CMS plot style site</figcaption>
</figure>
One for the calculations above is performed for every mass point ( since each mass point could give a different likelihood function ), and we can see that the observed values seems to be consistent with the standard model prediction, and that the standard model is able of discriminating this theory up to 3TeV.
