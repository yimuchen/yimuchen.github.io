---
layout: post
title: Customize Latex Commands
description: How to make your own latex commands and manage them across multiple documentations
tags: [coding,latex,recipe]
modified: 2017-02-17
image:
  feature: thoughts.jpg
  credit: ensc
---

Have you ever complained that writing complicated equations in latex is painful, especially when you maybe writing how a equation is solved. You might think you are writing the same things over and over again, give in to the [copy and paste mentality](https://en.wikipedia.org/wiki/Don't_repeat_yourself), then find that the source you originally copied and had a small typo and you compilation of the document is an explosion of error messages. While writing custom commands will not make all of the pain go away, it does help with reducing the amount of typing, as well as help keep a consistent look in you final output.

## An example - Partial differential
To get and idea of the power of custom commands, lets start of with an example that might be commonly encountered by physics students. If you have every tried to write partial differential equations in latex, you would know it is incredibly verbose to type out, with the typical fraction form of a first order partial derivative looking something like:

```tex
\frac{\partial f}{\partial x} + \frac{\partial f}{\partial y} = \frac{\partial f}{\partial z}
```

to produce

$$
\frac{\partial f}{\partial x} + \frac{\partial f}{\partial y} = \frac{\partial f}{\partial z}
$$

which might feel very annoying to type, with far-apart braces, repeating symbols, when the only really input relevant to the final output being `f` and `x`, `y`, `z`.

Lets look at what we could do with the a custom command. In you latex file before the equation you could write:

```tex
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}}
```

and in you actual equation, we would only need to type:

```tex
\pd{f}{x} + \pd{f}{y} = \pd{f}{z}
```

To produce the same output! One obvious merit of this that the equation in the tex file is a lot easier to read and write. Another merit is that suppose one day, you realized that you don't want the fraction form of the partial derivatives but the inline form:

$$
\partial_{x} f + \partial_{y} f = \partial_{z} f
$$

All you will need to to is to change the command you have defined to be something like:

```tex
\newcommand{\pd}[2]{\frac{\partial_{#2} #1}}
```

and then every instance in you tex file where you have used the command `\pd{a}{b}` will be changed to the inline format!


## Command in details

A complete documentation of how commands are written could be found on the [Macro](https://en.wikibooks.org/wiki/LaTeX/Macros#New_commands) wiki book page. But the example given above is a rather self explanatory example of how to define you own command.

```tex
\newcommand{\<commandname>}[<number of argument>]{what to do with the argument}
```

In the final curly braces, the input of the first argument should we written as `#1` and so on.

If your are familiar with the use of [macros in C/C++](https://gcc.gnu.org/onlinedocs/cpp/Macros.html), you might have already have an idea of how the commands work: they expand the defined expression of `\pd` for every instance that looks like `\pd{f}{x}` in a file into the full `\frac{\partial f}{\partial x}` before the tex engine begins it's typesetting routine. Also similar to the macros in C/C++, macros in latex and call one another, provided that they have already been defined. For example, suppose we what to defined how anti-particle and particle-antiparticle pairs are represented in our file using macros, we could write the macros as something like:

```tex
\newcommand{\anti}[1]{\ensuremath{\bar{#1}}}
\newcommand{\pair}[1]{\ensuremath{#1\anti{#1}}}
```

The `ensuremath` makes sure to load the math typesetting environment for the code withing the curly braces. So the snippet `\pair{c}` will produce \[c\bar{c}\], regardless of where we place the `\pair{c}` code is placed in the latex `$$` braces or not.

Notice that a command can have no arguments, in which case your command is simply a shorthand for a collection of symbols. An example could be if you are constantly dealing with particle and anti-particle pairs, it might be handy to have a shorthand like:

```tex
\newcommand{\ttbar}{\pair{t}}
```

to make the `tex` file look more natural.

Considering that in the final output of

$$
\text{Consider the production of $\text{t}^{*}\bar{\text{t}}{}^{*}$ in a $\text{p}\bar{\text{p}}$ collision}\\
\text{with a center-of-mass energy of 100TeV at an integrated luminosity of 100fb$^{-1}$}
$$

With macros, the raw latex code could look something like

> Consider the production of `\tstarpair` in a `\ppbar` collision  with a center-of-mass energy of 100TeV at an integrated luminosity of 100`\fbinv`

Rather than the raw latex code that would look like:

>> Consider the production of `$\text{t}^{*}\bar{\text{t}}{}^{*}$` in a `$\text{p}\bar{\text{p}}$` collision with a center-of-mass energy of 100TeV at an integrated luminosity of 100`fb$^{-1}$`


## Simple commands sharing between files
At one point, you might want to write with the same symbols over multiple documents. For examples you are writing work relate to a course of applied mathematics would constantly use the partial differential symbol. You could, of course, copy and paste the same commands every time you begin a new file, but then you are no longer guaranteed that your all your documents share the same command once you begin to alter the files. For projects where all documents are within the same folder, say your folder looks like:

```
YourFolder
├── Assignment1.tex
├── Assignment2.tex
└── Assignment3.tex
```

Where each `Assignment*.tex` file generates a different `pdf` file. The easiest way to share command in this case, would be to write a file `mycommand.tex` containing all the command you wish to share, and then write the in the individual `Assignment.tex` files, write something like the following:

```tex
\input{mycommand.tex}

Now I can use the \pd{x}{y} command wherever I want!
```

A complete documentation of what the `\input` command works can be found on the wikibook page dedicated to [modular file structures](https://en.wikibooks.org/wiki/LaTeX/Modular_Documents). If you are familiar with the `#include` preprocess of C/C++, you might also know how this command works: It is (nearly) a naive dump of the contents of the file `mycommand.tex` to the position the the `\input` command is called before evoking the tex typesetting engine.


## Command sharing for files anywhere

Suppose that have designed a [beautiful set of equation shorthands](https://github.com/enochnotsocool/UnixConfig/blob/master/TexSettings/mathHashing.sty) that you want to use for any new project you may be writing. One method is of course putting the `mycommand.tex` file in a fixed location in your computer and always `\input` that file. But lets face it, beginning a file with

```
\input{/home/ensc/settings/texsetting/mathcommands.tex}
```

or even worse:

```
\input{../../../../settings/texsetting/mathcommands.tex}
```

doesn't feel elegant. Can you get get latex to find the file for you? The answer is yes! Rename the file `mathcommands.sty`, and put it in the directory:

```
/home/<username>/texmf/tex/latex/mathcommands.sty # Unix
C:User\<username>\tex\latex\mathhcommands.sty     # Windows
```

And in your latex file, instead of the `\input` command. Use the `\usepackage` command before the beginning of the document body:

```tex
\usepackage{mathcommand} % No extention!
\begin{document}
I can use \pd{x}{y} anywhere in the document!
\end{document}
```

Latex packages are of course more than more than a collection of custom commands, you can read about it more on the dedicated wikibook page on [packages](https://en.wikibooks.org/wiki/LaTeX/Creating_Packages). Of course if you consider a user wide `.sty` file overkill, the `.sty` file be used in a single project folder too.


## Caveats of storing file in commands.
On major problem about using file to store custom commands is that to share the latex code with someone, you can no longer just share the snippet you are using, but you have to share all the file that contains custom commands as well. Depending on the scale of you collaboration, this may or may not be a problem. With the raise of cloud editing platforms such as [sharelatex](https://www.sharelatex.com/), this pain could be reduced without needing to go all out and host a git repositoy for you tex projects.

## Examples of math short-hands

I have been using self defined short-hands for a while. Here are some that I think is good enough to help you get started on making you own. My full repository could be found on my [github repository](https://github.com/enochnotsocool/UnixConfig/blob/master/TexSettings/mathHashing.sty)

```tex
% Defining braces
\newcommand{\enc}[1]{\ensuremath{\left( #1 \right)}}
\newcommand{\encsq}[1]{\ensuremath{\left[ #1 \right] }}
\newcommand{\encbr}[1]{\ensuremath{\left\lbrace #1 \right\rbrace }}
\newcommand{\mean}[1]{\ensuremath{\left\langle #1 \right\rangle}}
\newcommand{\set}[1]{\ensuremath{\encbr{#1}}}

%% Vector operators
\newcommand{\cross}{\ensuremath{\times}}
\newcommand{\dive}{\ensuremath{\vec{\nabla}\cdot}}
\newcommand{\grad}{\ensuremath{\vec{\nabla}}}
\newcommand{\curl}{\ensuremath{ \nabla \times}}
\newcommand{\lap}{\ensuremath{\nabla^2 }}

%% Differential operators
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\pdd}[2]{\frac{\partial^2 #1}{\partial #2^2}}
\newcommand{\pdc}[3]{ \left( \frac{\partial #1}{\partial #2} \right)_{#3}}

%defining commutation relation
\newcommand{\com}[2]{\ensuremath{\left[ \, #1 \, , \, #2 \right]}}
\newcommand{\anticom}[2]{\ensuremath{\left\lbrace \, #1 \, , \, #2 \right\rbrace}}

%% Defining Dirac Notation shorthand
\newcommand{\bra}[1]{\ensuremath{\left\langle #1 \right|}}
\newcommand{\ket}[1]{\ensuremath{\left| #1 \right\rangle }}
\newcommand{\braket}[2]{\ensuremath{\left< #1 \vphantom{#2} \right| \left. #2 \vphantom{#1} \right>}}
\newcommand{\Obraket}[3]{\ensuremath{ \left< #1 \vphantom{#2} \vphantom{#3} \right| #2 \left| \vphantom{#1} \vphantom{#2} #3 \right>}}

%% contraction notation
\newcommand{\con}[2]{\ensuremath{\left< #1 \,,\, #2 \right>}}

%% Functions
\newcommand{\abs}[1]{\ensuremath{\left| #1 \right|}}
```

## List of useful documentations:

* Defining custom commands: https://en.wikibooks.org/wiki/LaTeX/Macros
* Input command: https://en.wikibooks.org/wiki/LaTeX/Modular_Documents
* Writing your own package: https://en.wikibooks.org/wiki/LaTeX/Creating_Packages
