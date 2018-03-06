---
layout: post
title: 謊言、該死的謊言和統計
description: 看到一則奇怪的題目之後，決定用比較統計的方式來說明題目的盲點
tags: [statistics, education,]
modified: 2018-03-05
---

最近在同學的留言板上看他們在討論一道頗神秘的題目：

> XX國中某次段考（滿分100），學生成績呈常態分佈，平均 80 分，標準差 15 分。以下關於這次考試的解釋何者正確？

先不論選項答案選項有什麼，在說明學生的分數分佈的時候，題目所引述的數字充滿著詭異的氛圍：比平均高 $4/3$ 個標準差就到滿分了，那「呈現常態分佈」一詞該如何說明？
這一則題目其實可以說明多數人對「統計解釋」（Statistical Inference）的一些謬思，期中最常被引用但是也潛在很多誤解的就是 **平均數** （*mean*）、**標準差** （*standard deviation*） 和 **分佈** （*distribution*）之間的關係。
我想試試看用我所熟悉的工具來解釋這一到題目**可能**在說什麼，說明期中弔詭的地方，和自己對這些統計工具的一些看法。

我需要先說明，我自己是物理底子出來的，只是因為實驗室的需求會多接觸到統計相關的工具。這些工具用嚴謹的數學來說到底是不是這一回事我不敢保證，還有請讀者幫忙補充。

# 所謂常態分佈和「平均數」、「標準差」？

一般來說，我們會用**分佈** ([distribution](https://en.wikipedia.org/wiki/Probability_distribution))一詞，代表著我們相信有一個機率(密度)函數在決定我們測驗的結果。
以**常態/高斯分佈**([Normal/Gaussian distribution](https://en.wikipedia.org/wiki/Normal_distribution))來說，這個機率密度函數定義為：

$$
G(x;\mu,\sigma) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\enc{- \frac{1}{2} \efrac{x-\mu}{\sigma}^2},
$$

其中 $x$ 是我們的測量值，$\mu$、$\sigma$ 是控制常態分佈長相的兩個**控制變量**(parameter)，$\mu$ 會控制「最常出現的分數」，$\sigma$ 分數有多分散，我們先姑且稱他們為我們分佈的**高斯平均**和**高斯標準差**。
但是這邊要特別注計，$G$ 要符合機率密度函數的定義($G$ 對 $x$ 積分的結果為 $1$)的話，$x$ 要可以為負無限大到正無限大的任意值。
一般我們的測驗都會有某個範圍（以今天的題目而言 $x$ 是測驗分數的話，那 $x$ 的定義域應該為 $0--100$ ），所以我們應該定義一個 **截斷常態分佈** (Truncated normal distribution):

$$
G_T(x;\mu,\sigma,a,b) =
\begin{cases}
\frac{I(\mu,\sigma,a,b)}{\sqrt{2\pi\sigma^2}} \exp\enc{- \frac{1}{2} \efrac{x-\mu}{\sigma}^2} & x\in[a,b] \\
0 & x \notin[a,b]
\end{cases}
$$

其中 $I$ 為一個使 $G_T$ 對 $x$ 積分為 $1$ 的歸一化變量（Normalisation factor）：

$$
\frac{1}{I(\mu,\sigma,a,b)} = \int_a^b G(x;\mu,\sigma) dx 。
$$

我們看到當 $b \gg\mu\gg a$ 的時候，$I\sim 1$ ，所以我們的截斷分佈基本上跟我們的常態分佈是一樣的。
那可能我們就會很單純的以為我們可以定清楚的定義一個「$0--100$ 之間，*平均* 為 $80$，*標準差為*  $15$ 的(截斷)常態分佈」。

但是問題是**我們不知道我們的原始分佈是什麼**。
統計工具可以做的事情就是用有限的樣本(也就是有限的學生測驗)，回推我們的原始分佈是什麼。
也就是說，給定若干的測驗結果：$\set{x_i}$，在假定分佈 $P(x;\mu,\nu,\ldots)$ 的條件之下，我沒有沒有辦法「得知」$\mu$、$\nu$……等等控制變量的值？
一個統計常用的方法是所謂的**最大似然估計**([Maximum likelihood estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation))：給定觀測結果 $\set{x_i}$ 與假定分佈 $P(x;\mu,\nu,\ldots)$，該測驗解果出現的似然度 (Likelihood) 為：

$$
L(\mu,\nu,\ldots) = \prod_i P(x_i;\mu,\nu,\ldots)
$$

那對於實際分佈中控制變量的「好」估計（$\tilde\mu$、$\tilde\nu$），就是可以將似然函數極大化的數值 （也就是 $L(\tilde\mu,\tilde\nu,\ldots)$ 是 $L$ 函數的極值）。
一般來說，似然函數有點難操作，所以我們在這邊給他取對數，變成：

$$
\mathcal{L}(\mu,\nu) = \ln\enc{L(\mu,\nu)} = \sum_i \ln\enc{P(x_i;\mu,\nu,\ldots)}
$$

由於對數是一嚴格遞增函數，所以將似然函數極大化，就是將似然函數的對數函數極大化。
這個套用到常態分佈的時候會有很漂亮的結果：

$$
\mathcal{L}(\mu,\sigma) = \sum_i \encsq{-\frac{1}{2}\ln\enc{2\pi\sigma^2} - \frac{(x_i-\mu)^2}{2\sigma^2} }
$$

找極值解就是找偏微分為零的地方，所以我們可以列式找 $\tilde\mu$：

$$
\begin{align}
\pdc{\mathcal{L}}{\mu}{\mu=\tilde\mu} = 0 & = \sum_i \frac{1}{\sigma^2} (x_i -\tilde\mu) \\\\
\Rightarrow 0 & = N \tilde\mu - \sum_i x_i \\\\
\Rightarrow \tilde\mu & = \frac{1}{N} \sum_i x_i \\\\
\end{align}
$$

也可以列式找 $\tilde\sigma$：

$$
\begin{align}
\pdc{\mathcal{L}}{\sigma}{\sigma=\tilde\sigma} = 0 & = - \sum_i \encsq{ \frac{1}{\tilde\sigma} + \frac{1}{\tilde\sigma^3}(x_i-\tilde\mu)^2} \\\\
\tilde\sigma^2 = &\frac{1}{N} \sum_i (x_i - \tilde\mu)^2
\end{align}
$$

這些結果可能看起來很眼熟：這就是我們一般數據統計中的**樣本平均數**和**樣本標準差**！
也就是說，我們一般在算樣本平均數和樣本標準差的時候，其實就在偷偷的做最大似然分析：給定我們這些數字，什麼樣的常態分佈最可以描述這些數據？
不過，都我們套用到**截斷**常態分佈的時候，這個問題就沒有這麼單純了。因為似然函數裡面多了我們的歸一化函數 $I(\mu,\nu,a,b)$，所以**樣本平均數**並不會對應到我們放在截斷函數裡面的**高斯平均數**。同樣的，**樣本標準差**並不會不會對應到我們的**高斯表準差**。
在這種時候當我們說「分數符合常態分佈，平均為$80$分，標準差為$15$分」，我們應該要假設這個「平均」指的是分佈平均數還是樣本平均？甚至我們推到無限大樣本的時候，樣本平均數變成**分佈期望值**([Expected value](https://en.wikipedia.org/wiki/Expected_value))$e$、樣本標準差變成**分佈變異量**([Variance](https://en.wikipedia.org/wiki/Variance))$v$時，這差異亦存在：

$$
\begin{align}
e \equiv& \int_a^b x G_t(x;\mu,\sigma) dx  \\\\
v \equiv& \int_a^b (x-e)^2G_t(x;\mu,\sigma) dx
\end{align}
$$

不要以為這個差異會是小的！題目其中一選項「$65$分以下的$15$％學生」的對錯會大大的被所謂的「平均、標準差指的是什麼統計變量」決定！也就是說題目應該要說明「平均」、「標準差」二詞指的是描述常態分佈形狀的變量，還是樣本計算出來的統計量。

<figure>
  <img src="{{site.url}}/images/genimage/stat_infer/all_trunc_gauss.png"/>
   <figcaption>將分佈期望值($e$)、高斯平均數($\mu$)，分佈變異量(開根號)($\sqrt{v}$)、高斯標準($\sigma$)差詮釋為題中「平均數」，「標準差」所得的四種不同分佈，期中最後一個分佈（
   分佈期望值為80，分佈變異量為20的分佈）在可見的範圍內實在難以稱為「常態分佈」)
   </figcaption>
</figure>

# 符合一個分佈？
眼尖的讀者可能注意到最大似然分佈沒有辦法告訴我們所取得的分佈 $\set{x_i}$ 到底符不符合我們遠本假定的分佈：50人得100分、50人得60分的結果一樣會給你一個樣本平均 80 分、樣本標準差 20 分的結果，但是這結果給人的感覺很不符合高斯分佈吧？

一個數據到底多符合一個給定的分佈，需要執行所謂的**拟合優度測試**(goodness-of-fit tests)。
舉一個常用的科氏--斯氏測驗（[Kolmogorov–Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test)）：給定一個組數據 $\set{x_i}$，我們可以定義一個**經驗機率累計函數**：

$$
F_\text{ex} (x) \equiv \frac{1}{N} \sum_i \theta(x-x_i)
$$

其中$\theta(x)$ 為階躍函數（[step function](https://en.wikipedia.org/wiki/Step_function)），拿這個累計函數與我們模型的累計函數比較：

$$
F \equiv \int_{-\infty}^x P(x;\mu,\nu,\ldots) dx
$$

者兩個函數的對大差距 $D$ ，若$\set{x_i}$是由機率函數$P$產生的數據，在$N\rightarrow\infty$的時候被證明會趨進一**科氏分佈**(Kolmogorov distribution)。

$$
\sqrt{n}D \rightarrow K(s)\;;\quad \int_{-\infty}^s K(s') ds' = \frac{\sqrt{2\pi}}{s} \sum_{k=1}^{\infty} \exp\enc{-\frac{(2k-1)^2\pi^2}{8s^2}}
$$

這兩個累積函數之間的距離一定會是機率性的，畢竟有機會你用一個常態分佈產生的 100 數字都落在原本高斯分佈的 $2\sigma$ 以外。當然這種機率應該是小的(以這例子而言，大概是 $0.05^{100}\sim10^{-130}$)，所以當我暪所算出來的數值在科氏分佈中所對定的p值(p-value)足夠大，那我可以結論說：「在 1-p 的信心水準下，K--S測試無法分辨我們的數據與函數模型的差異」。

題目中沒有題中任何優度測試的資訊。但是我們可以來比較一下 $n$ 大概在多少以下，我們沒有辦法分辨我們上一個段落所產生的 4 種機率函數。這邊我們直接兩兩比較機率累計函數相差的對大值，看 $n$ 多少的時候，統計量在科氏分佈裡對應的p-值會開始 $\leq0.5$:

|   | $G_0$ | $G_1$ | $G_2$ | $G_3$ |
|---| ---  | ---  | --- | --- |
|$G_0$| $NAN$ | 79 | 41 | 23 |
|$G_1$| 79 | $NAN$ | 17 | 15 |
|$G_2$| 41 | 17 | $NAN$ | 253 |

我們可以看到要真的隨便我們選分佈，那參與學生大概只剩下 15 人了呢！看來說清楚到你到底是什麼分佈的什麼數值對應到平均、標準差很重要呢！

# 結語
俗話說「世界上有三種謊言：謊言、該死的謊言、和統計」。統計本來就是將很多數據濃縮成少少的幾個輸字來說故事的一門學問。
但是往往引用這些數字的時候，我們忽略了得這些數字背後的假設與條件。
當沒以把話說清楚，結果可以差非常多的！
錯誤的使用的些工具或是表述方式往往代表算出來的數字無從評論對錯。
不過也也些人會惡意操作這些工具，讓一組數據「證明」他想說的故事。
下次看到問一個文章中引數據，不妨想一想中間到底藏的多少假設在其中，也自己拿筆算算這些假設到底何不合理。

*P.S.* 可能眼尖的人會注意到樣本標準差和最大似然分析所得到的樣本差不一樣，應該要把 $N$ 換成 $N-1$。文中的算法其實有一些統計性質沒有最完善的考慮到（我們直接用 $\tilde\mu$ 帶入 $\mu$ 的位置，而忽略了 $\tilde\mu$ 可能有的統計誤差）。詳細可以看維基百科的原文！
