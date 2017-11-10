---
layout: post
title: Introduction to CMS Software
description: A step-by-step introduction to writing analysis coding the CMSSW
tags: [c++, python, cmssw]
modified: 2016-08-13
image:
  feature: code_head_1.png
  credit: ensc
---



## Disclaimer

I do not own any of the contents of [CMSSW](https://github.com/cms-sw/cmssw), nor indeed participated in any [development of CMSSW](http://cms-sw.github.io/tutorial-collaborating-with-peers.html). I am just trying to share my experience in developing my analysis code using the tool provided. If any developer does not wish the contents of these pages to be hosted here, notify me and I will take them down immediately!

## Contents

  1. [The compiling environment and `Hello world`!]({{ site.url }}/ItoCMSSW01HelloWorld)
  2. Meeting the Event Data Model(EDM) file format
  3. First look at full CMSSW
  4. Altering the contents of EDM files
  5. Saving your own C++ formats

## Prerequisites

In these pages I will assume that that you are already familiar with:

 * Navigating a UNIX system with the command line
 * Have access to a working CMSSW evironment
 * Familiar with C++ development:
   * Has rudimentary knowledge of writing multi-file C++ projects.
   * Shared object files.
   * Include path, link path, paths in general.
 * Understand python syntax
   * Even if you don't, python syntax is very easy to pick up if you know other programming languages.
   * You do not need to know the python feature, just basic control flow and object declaration.

First, lets unify the software version we will be using throughout this tutorial by setting up the CMSSW environment

```bash
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_0_16
cd CMSSW_8_0_16/src
cmsenv
```

This should give you a directory as that looks something like:

```
└── CMSSW_8_0_16
    ├── biglib
    ├── bin
    ├── cfipython
    ├── config
    ├── doc
    ├── external
    ├── include
    ├── lib
    ├── logs
    ├── objs
    ├── python
    ├── src
    ├── test
    └── tmp
```

We will be working mainly in the `CMSSW_8_0_16/src` directory, where all of your source code goes, looking a bit at the other directories when it is needed. Also note that the majority of the tutorial would be version independent, and version dependent snippets will (hopefully) be spelled out explicitly.

## Why I am writing this

>> 工欲善其事，必先利其器 - 《論語·魏靈公》

There are two equally important aspects of writing code: writing such that computers could understand what you want; and writing such that humans could understand what you are trying to do. Unfortunately, when there is a demand for immediate results, the writing of analysis code typically begins slipping into the unfortunate mindset of "write once, run once, read never". This practice I believe is damaging for the analysis in the long run, with advances in analysis techniques and commonly used subroutines constantly being lost in heaps of unreadable code, and excessive man power being wasted on reinventing wheels that have been used multiple times already.

The CMS Software frameworks actually provides a very nice structure for organizing code, as well as a powerful specialized library for event based data storage; both aspects of which is highly under-appreciated by the majority of people performing analysis work. Yes, the learning curve might be steep, but as the scale required for analysis grows larger, I think it is worth it to learn C++ development tools to allow for you works to grow independently of who is still working on a project. CMSSW already provides a simplified and easily-readable version so that one does not have to learn the even-harder [`make`](https://www.gnu.org/software/make/manual/make.html) or [`cmake`](https://cmake.org/) workflows.

A part of why the learning curve is so steep for a supposedly simplified system lays with the documentation, which, though being detailed, is spread-out through many disconnected pages in the [CERN wiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookAnalysisOverviewIntroduction), and fails to give a comfortable starting point for an beginner to start reading and learning. This is what I what I intend to provide here: if you are familiar enough with C++, hopefully you would find these pages helpful!
