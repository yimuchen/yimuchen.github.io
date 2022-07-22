---
layout: post
title: 深思熟慮(6) - 電動勢的計算
description: 一個看似簡單的問題，讓人重新整理電動勢的定義與計算
tags: [physics, thoughts, education]
modified: 2022-07-26
---

最近我看到一個看似簡單的問題:給定下面電路，磁場只存在灰色區間，而灰區間的總磁通量 $\Phi_B(t)$ 隨時間變化為

$$\Phi_B(t) = 1 \mathrm{Tesla-m}^{2}\mathrm{sec}$$

那兩電壓計 $V_1$ 和 $V_{2}$ 量到的電壓分別為多少？寂靜是不是一樣？

我後來又衍生我的問題：若電壓計 $V_1$ 接點位置由 BA 換為 B'A' ，電壓計 $V_2$ 接點位置由 CD 換為 C'D' 的話，測量電壓有沒有變化？若電壓計 $V_1$ 接點位置由 BA 換為 EF ，電壓計 $V_2$ 接點位置由 CD 換為 EF 的話，測量電壓有沒有變化？

<figure >
	<img src="/images/posts/20220722/circuit.png" alt="">
</figure>

## 定義感應電動勢

電磁學裡面的定義：電動勢 (EMF 或是 $\varepsilon$) 一般定義為電場環積分不為零的總和：

$$\varepsilon = \oint \vec{E}\cdot d\vec{l}$$

現實世界中有各式各樣得機制可以產生這種不遵循靜電場的電動勢。而這邊最重要的就是冷次電磁感應，或是法拉第定律：

$$\varepsilon = \oint \vec{E} \cdot d\vec{l} = \int \frac{d\vec{B}}{dt} \cdot d \vec{a}  = \frac{d\Phi_B}{dt}$$

這邊一般高中會交得作法就是用 $\varepsilon$ 與 $\frac{d\Phi_B}{dt}$ 之間的關係，配合歐姆定律還解電流：

$$
\varepsilon = I (R_1 + R_2)\;;\quad
I = \frac{1}{(R_1 + R_2)}\frac{d\Phi_B}{dt}
$$

如此一來確有另一個問題：我們用電壓計量 AB 之間的電壓，我們會得到 $IR_1$；然而我
們量 CD 之間得電壓會得 $IR_2$？這怎麼可能呢？取一個極限：我們把測量點拉到途中的
EF ，我們測兩點的電壓竟然可以得到兩個不一樣的答案？

## 一個錯誤的解

很多人最常用的「解」就是說迴圈裡面的每一個線段都會貢獻這個總電動勢 $\varepsilon$ 的一部分。也就是說 $AB$, $BC$, $CD$, $DA$ 迴路中的四個片段都大致上個貢獻 $\varepsilon/4$ 的總感應電動勢。若取連續極限，那我們就可以解決 EF 測量兩點可以得到兩個不同的解的問題了。

但若此假設為真，一個最直接的問題就是 $BC$ 之間現在有一個不可忽略的電場，若沒有一個非無限大的電流，歐姆定律：$\vec{E} = \rho \vec{J}$ 在這邊就不適用了。如過這個解釋是正確得話，好像不是法拉第定律有問題，就是歐姆定律有問題，又或是我們對電動勢得定義有問題？

這個解的盲點在於：電動勢是一個可以被區域化的物理量嗎？回到電動勢的定義：

$$\varepsilon = \oint \vec{E}\cdot d\vec{l}$$

他必須是一個完整的迴路的電場計算，我們可以只因為線段 $AB$, $BC$, $CD$, $DA$ 長度一樣，所以就說這四個線段長的對電動勢有一樣的貢獻嗎？

## 完整的解

如果我們要完整的解這個問題，就是需要把我們用的定律完整的寫出來：

- 法拉第定律(積分式)：
  $$ \oint \vec{E} \cdot d\vec{l} = \frac{d\Phi_B}{dt}$$

- 歐姆定律（電流密度式）：

$$ \vec{E} (\vec{x}) = \rho(x) \vec{J}(\vec{x}) $$

- 克希荷夫電流定律（電賀守恆微分式）：

$$\vec{\nabla}\cdot \vec{J}(\vec{x}) = 0$$

因為我們的迴路不是均勻材質：我們迴路中有理想導體 $\rho=0$ 也有 $\rho$ 是有限值的電阻。所以我們的電場環積分是裡面 ，即便長度 $BC$ 和 $AB$ 看起來是一樣長的，他們對環機分的貢獻是 **不一樣** 的。

那接下來一個問題就是，為什麼一個不對稱的電場可以被產生呢？因為在這個系統中，可以產生電場的機制不只有磁場變化，還有存在導體中的靜電荷！

### 面電荷電場貢獻

我們一般在解電路的時候，都會把電壓、電流、電阻抽象化變成單一電路元件的物理量，但是實際上在討論電流怎麼在導線中移動的時候，我們必須要討論導線上的面電荷怎麼分佈可以使導線中的電場極小，怎麼使迴路中的電場分佈集中在電阻附近。如果我們堅持要解每一個迴路線段的電動勢貢獻的話，那我們必須解完整的方程式，包含面電荷密度對電場的貢獻。這邊要小心，法拉第定律意或是麥克司威定律只對 **總** 電場/磁場的適用，所以當我們系統中存在可以任意分佈的自由電荷時，微分解會便得非常的困難。[這個連結][surfacechargesol]裡面提供了一些簡單迴路的面電荷解。

但是積分解：(總)電場環積分等於磁通量變化，一樣是正確的，但是在這個系統裡面他反而是簡單的解。那就是為什麼我們用最陽春的計算得到的解反而會比我們嘗試去解片段電動勢貢獻還要簡單，也比較容易得到接近「正確的答案」。

[surfacechargesol]: https://www.glowscript.org/#/user/matterandinteractions/folder/matterandinteractions/program/18-SurfaceCharge

### 兩點測量不同測量值

如此說來，我們最開始解的電流答案 $I=\frac{1}{R_1+R_2}\frac{d\Phi_B}{dt}$ 確實是正確的，而 BC 之間的電場大小是可以忽略的，那確時好像是 $V_1$ 電壓計和 $V_2$ 電壓計的測試不一樣的，那我們取極限量 EF 兩點電壓計可以量到不一樣的「電壓值」要怎麼解釋？

事實上：因為電路和磁場之間的幾何關係， $V_1$ 和 $V_2$ 不是等價的測量！我們沒有辦法在不更動磁場也不更動電線連結下把 $V_1$ 換到 $V_2$ 的位置！考慮我們兩個個量值 $V_1$ 和 $V_2$ 都連結在 EF 我們空間上把 $V_1$ 搬到 $V_2$，$V_1$ 的迴路一定需要經過有磁場區間！在一個電場不是保守場的環境中，我們經過一個有磁場變化的區間，電壓計兩端的電位會有改變也便得不是一個很怪的結論了。

## 評什麼我說我的解釋正確的？

說了這麼多，物理還是一個自然實驗科學，我們實際上去架設一個這樣的裝置，我們到底會量到什麼？如果有機會的話，這是一個簡單得實驗，很值得大家實際去測試看看的這結果。

這邊就只能附上一個 paper [連結][paper] 說對！你用電壓計同時量 EF 兩點的「電位差」，會因為你電壓計放在電路拓樸中的位置不一樣有不一樣的解果！這個問題也不是第一次被提出作為討論核心題目：這個結論首先被 MIT 的 Walter Lewin 教授大力[倡導][youtube1]，在課堂上[實驗證明][youtube3]，也被不少其他的電子學的教育者[討論][youtube2].

[paper]: https://aapt.scitation.org/doi/10.1119/1.12923
[youtube1]: https://www.youtube.com/watch?app=desktop&v=LzT_YZ0xCFY
[youtube2]: https://www.youtube.com/watch?v=0TTEFF0D8SA
[youtube3]: https://youtu.be/nGQbA2jwkWI?t=2990

# Some closing thoughts

This is my favorite sort of question: it takes what you think you are very
familiar with, and gives it just enough of a twist to make you question deeply
about what our written laws of nature is trying to say, and lead to fascinating
results that feel too counterintuitive be a real description of reality when it
actually is. Alas, this question, however deep the implementations might go, was
given simply as a multiple choice question in a standard test, leaving much of
the "interesting" debate out, and most people will be left with just a standard
answer. This question can be used to go into very deep topics: surface charge
solution to circuits, importance of proper definition of field operations, and
even touching on why we are about topology in physical systems. And even if my
answer is incomplete or unsatisfactory to some, one can hope that because of the
debate that this has induces some more interest in how this topic can be used
for more discussion.
