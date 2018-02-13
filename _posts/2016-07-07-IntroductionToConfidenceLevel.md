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
A usual form of conclusion is we say "it is highly unlikely that a particle with mass $X$ with such and such properties exists". The conclusion diagram we draw typically look like this:

<figure>
<a href="https://ghm.web.cern.ch/ghm/plots/public-results/publications/EXO-15-001/CMS-EXO-15-001_Figure_003-c.pdf">
<img src="https://ghm.web.cern.ch/ghm/plots/limitPlot_example.png"></a>
<figcaption>Example diagram from CMS plot style site</figcaption>
</figure>

In this diagram we say that:

* Everything observed (black dots) is within 2 $\sigma$ of the standard model(double coloured band)
* We could say that there is no apparent new $gg$ resonance with masses smaller than $3TeV$ with the colour-octet scalar model (where the pink line intersects the band).

In this article, I wanted to quickly go over what is being calculated, some very basic arguments as to why we are calculating it as such, as well as a brief summary of how the results are being presented and how it should be interperated.
It would not cover the mathematical rigor of what is being calculated is.

# The "fairness of a coin" experiment
To begin with lets consider our standard model, or null hypothesis of coins being "all coins have an equal chance of giving heads or tails when flipped".
Now someone claims that they have found a way of manufacturing magic coins that can break our standard model.
However, these coins break after one coin toss and are very expensive to produce.
With a limited amount of coin tosses, what can one say about how different the magic coins are from our standard coin-model?

## Defining an parameters and observables
First a **parameter** is define to characterise the property of the coin we are experimenting on.
For each coin, we assign a "unfairness factor" $\theta$: the probability of the coin giving a head minus the probability, rescaled so that $\theta$ spans the range of $[-1,1]$, with $\theta=0$ being the "fair" model.
Determine what value $\theta$ is for the coin is would be the goal of our experiment.

Now after $N$ coin tosses, we could obtain a **observed** unfairness $x$, defined as the fraction of head minus compared with the number of tosses (with the same rescaling theme).
Notice that $x$ could be 1 even if the underlying $\theta=0$.
To make a proper assessment of how probable the observable $x$ is to appear, we would need to invoke the likelihood function $L(x\rvert\theta)$:

>> $L(x\rvert\theta)$: the probability of observing $x$ under the condition that the coin has an underlying unfairness factor of $\theta$.

In our case, where the observable is a single variable, the likelihood function is equal to a probability function.

<figure>
  <img src="{{site.url}}/images/genimage/cls_article/CLS_Likelihood.png"/>
  <figcaption>
    Likelihood as a function of $x$ of our coin-toss experiment with $N=40$ and various $\theta$ values.
    The results with $x<0$ has been omitted.
  </figcaption>
</figure>

The key how is to compare the likelihood obtained when the underlying $\theta=0$ and when $\theta\neq0$. A new variable $y$, based on the observable $x$ and a proposed theory $\theta$ is defined as:

$$
y(\theta) = -2 \, \ln(Q) \equiv -2\, \ln\left( \frac{L_\text{alt}}{L_\text{null}} \right)
  = -2 \ln\left( \frac{L(x\rvert \theta)}{ L(x\rvert 0)} \right)
$$

For an actual experiment for $N$ tosses of a real, physical magic coin, a unique value of $y$ could be obtained for a specific test hypothesis with $\theta \neq 0$.
In the diagram above, we can see that a likelihood ratio could provide some sort of insight into how similar a single result is to one hypothesis or another (large ratio implys that the null hypothesis is "more likely" to be true and vice versa).
How to use these calculations to reach a solid conclusion still requires a little more work though.


## Defining how "non-standard" our observed result is
Now, for a given $\theta$ we are trying to validate/disprove, there are two probability distribution functions of interest:

>> $P_\text{null}( y \rvert \theta_{alt})$: The probability of observing $y$ with a given testing $\theta_\text{alt}$ when the coin has a actual $\theta=0$

>> $P_\text{alt} (y \rvert \theta_{alt})$: The probability of observing $y$ with a given testing $\theta_\text{alt}$ when the coin has a actual $\theta=\theta_\text{alt}$

Using these two distributions, we could begin to see how we could interpret the experimental results.
If the observed $y$ is "deeper in the distribution of $P_\text{null}$", it is likely that the null hypothesis is true; and vice-versa.
This testing scheme could also tell whether the experiment might be insufficient to distinguish between the new and old, if the two distribution have significant overlap.
By the definition of $y$ and $P$, the distribution $P_\text{null}$ will have a higher mean than $P_\text{alt}$.

<figure>
  <img src="{{sit.url}}/images/genimage/cls_article/CLS_ratio.png">
  <figcaption>
    Distribution of $P(y \rvert \theta_{alt})$ with test hypotheses $\theta=0.3$(left) and $\theta=0.6$(right).
    The number of coin tosses $N=40$.
    Take note that $P_\text{null}$ is defined with a specific test hypothesis, so the two $P_\text{null}$ in the left and right figures would not be the same.
  </figcaption>
</figure>

For each observed $y_0$ value, we could define $CL_b$ and $CL_\text{s+b}$ as:

$$
CL_b(y_0 , \theta_\text{alt}) \equiv \int_{y_0}^\infty P_\text{null}(y\rvert \theta_\text{alt}) dy ; \quad
CL_\text{s+b}(y_0 , \theta_\text{alt}) \equiv \int_{y_0}^\infty P_\text{alt}(y \rvert \theta_\text{alt}) dy
$$

The discriminating value $CL_s$ is label such for historically being called the **confidence level** of this observed $y_0$ being a consequence of $\theta_\text{alt}$ hypothesis rather than of null hypothesis.
But note that the value does not directly correspond to the [confidence level](https://en.wikipedia.org/wiki/Confidence_interval) more commonly used.
The final discriminator used is defined as:

$$
CL_s(y_0,\theta_\text{alt}) = \frac{CL_\text{s+b}}{CL_b}
$$

A $CL_s$ value implies two things:

  * This observed results lies closer towards the standard model distribution.
  * The two distributions are far apart enough for small values to occur.

The use of this statistic is the same as the original confidence level used by the scientific community: if $CL_s <0.05$, the results are considered "statistically significant"; and if $CL_s < 10^{-6}$, the results indicate "a new discovery".

## Defining exclusion limit
For each observed $x_o$ value, there is a corresponding value of $\theta_\text{ex}$ where $CL = 0.05$.
Meaning that given the observation $x_o$, one can not confidently distinguish if the observation is the result of a statistical fluctuation of the null hypothesis, or if it due to an alternative model with $\theta < \theta_\text{ex}$.
So this our 95% confidence exclusion limit for a single observation.
In our coin-toss experiment with a single observed $x_o$, there is of course *two* values of $\theta_\text{ex}$, one positive and one negative.
We will be focusing only on the positive side for now.

By the given model, we could also get the probability distribution of measuring $\theta_\text{ex}$ **if the null hypothesis is right**, which we will notate as $R_\text{null}(\theta_\text{ex}|N)$.
Typically, $R$ is summarized as double banded region with $\theta_\text{ex}$ as the $y$ axis, with yellow for the corresponding "$2\sigma$" region of the distribution, and green for the "$1\sigma$" region.

<figure>
  <img src="{{sit.url}}/images/genimage/cls_article/cls_exclusion.png"/>
  <figcaption>
    Confidence levels and $\theta_\text{ex}$ of coin toss experiments with 40 (left,cyan) and 400 (right,orange) coin tosses.
    The solid lines on the left and right plots are expected limit calculated with an observation of  $x=0.25$ (black) and $x=0.1$(blue).
  </figcaption>
</figure>

Notice that there are two "95%" intervals implied in this diagram:

  * Any $\theta_{ex}$ obtained from a real experiment has a 95% chance to fall within the double band region if the null hypothesis is indeed true.
  In this context, the double band demonstrate how powerful the experiment is at excluding non-null hypothesis theories, under the assumption that the null hypothesis is true.
  A powerful experiment would have a small exclusion $\theta_\text{ex}$, with a very small band, with the null hypothesis strongly favouring certain results over all possible outcomes.  
  * Experimentally, any theory with the $\theta$ value below the solid **observed limit** can be exclude by our observation with 95% confidence, regardless of whether this solid line lines within the double-banded region or not.
  In the case that the solid line does not lay in the double-banded region, the claims of exclusion of certain models could still be made, but more detailed discussion would have to be made as to why the observation deviates from the null-hypothesis.



# Corresponding variables in High Energy Physics
In high energy physics, the $x$ we want to observe is typically number of events, and the $\theta$ is typically the signal strength, with the theoretical value being $1$ and the standard model (the null hypothesis) being $0$.
If, in performing the experiment, the standard model is epxected to exclude $\theta\geq1$, then this theory could be disproved by our experiment;
After assessing the actual experimental data, if the observed exclusion is also similar to a predictions of the standard model, then there is a high chance that the standard model is correct.

Back to the first example diagram:
<figure>
	<a href="https://ghm.web.cern.ch/ghm/plots/public-results/publications/EXO-15-001/CMS-EXO-15-001_Figure_003-c.pdf"><img src="https://ghm.web.cern.ch/ghm/plots/limitPlot_example.png" alt=""></a>
	<figcaption>Example diagram from CMS plot style site</figcaption>
</figure>
One for the calculations above is performed for every mass point (since each mass point could give a different likelihood function), and we can see that the observed values seems to be consistent with the standard model prediction, and that the standard model is able of discriminating this theory up to 3TeV.
Do not think that our artificial coin toss experiment is too farfetched, either.
In the case of discrete symmetry experiments (ex. observation of CP violating processes), the observable on interest would be the *sign* of an inner product of three vectors, so even our very simple toy model has it's uses in physics analysis.
