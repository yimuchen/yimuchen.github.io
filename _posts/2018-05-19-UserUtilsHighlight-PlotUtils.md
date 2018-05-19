---
layout: post
title: Package Highlight, the PlotUtils library
description: A wrapper for a nicer ROOT plotting experience in CMSSW
tags: [cmssw, root, cpp, computing ]
modified: 2018-05-19
image:
  feature: code_head_1.png
  credit: ensc
---

I personally really like the CMS Software environment. It provides excellent and intuitive support for operating CMS data, and an excellent framework for organising analysis code. Yes, it has a steep learning curve (made even steeper by the face that there isn't a lot of [good tutorials on basic, user-level stuff]({site.url}/posts/ItoCMSSWHome/)), but I very well think it is worth the time. To highlight my point, I thought I would write up a collection of packages that uses the CMS framework to assist some of the generic use cases that an analyser might run up with. The full package can be found [here](https://github.com/yimuchen/UserUtils), but today I would like to highlight the package that took up the most time to write, and tackle part my gripe with [ROOT](https://root.cern.ch/) --- a "better", more intuitive ROOT-based plotting library design for analysis purpose.

# Issues with the ROOT plotting library

I have no doubt that ROOT's graphic libraries have their design purposes, but the interface feels outdated, and sometimes feels incredibly annoying to use. There are just some of the gripe that I have with it:

-   **Excessive use of unit-less/magic numbers** - When constructing a [`TCanvas`](https://root.cern.ch/doc/master/classTCanvas.html), we specify it like: `TCanvas c("c","c",600,600)`. The immediate question would be: 600... what? Pixels? Millimetres? How would this unit translate onto a published page? Would I need to scale the plot? How big would the "0.035" text be? Is it the same as the the text used in my analysis notes? Or would there be some weird size difference between the fonts? This also applies for the various styling operations in ROOT. I doubt anyone can, at a glance, understand what we are to make of the ["fill-style 3452"](https://root.cern.ch/doc/master/classTAttFill.html), or know by heart which [font face "113"](https://root.cern.ch/doc/master/classTAttText.html) is. For whatever reason, these variables are never enumerated into a more human readable format.

-   **Excessive use of 'magic strings' for plot style specification** - Using strings as function options is really scary, as it would never rise a compile time error. A wild typo might make the whole plotter do something weird and the user will never know until the plot has been completed. The specifications themselves are also really weird: [Histograms](https://root.cern.ch/doc/master/classTHistPainter.html) require the `"SAME"` to avoid objects being plotted recently from being wiped, but [Graphs](https://root.cern.ch/doc/master/classTGraphPainter.html) are different. Graphs require the `"A"` option to draw an axis frame, but the same options is used for _disabling axis drawing_ for histograms. And then there is the issue that a lot of options are not properly documented. I bet you didn't know there was an [`"NOCLEAR"` option]("https://root.cern.ch/doc/master/classTHStack.html#a6294f58bebce2f1ce5d6dced8e22bc1e") for the [THStack](https://root.cern.ch/doc/master/classTHStack.html) object to void _it_ from wipe stuff from the canvas!

-   **Bad output format** - revealing the answer that the units in the `TCanvas` declaration is in fact pixels. How are we suppose to save a OK quality raster image? For very complex diagrams, vector images might take an excessive amount of time to load on a presentation or a website. but a good resolution raster image could be loaded much faster. The "600 by 600 pixel" canvas saved to a PDF file might look fine, but produces a very bad raster image. And in fact the PDF file isn't fine, it is missing some PDF code that has issues with different rendering engines ([xelatex being one of them](http://tex.stackexchange.com/questions/66522/xelatex-rotating-my-figures-in-beamer)). While the majority of user using PDFLatex for CERN publication might think it is fine, some of use do need the simpler multi-language support for our thesis works.

-   **Difficult object usage tracking** Objects are "Drawn" after a TPad is "cd"ed to, with no indication of what object is being drawn to which pad otherwise, The axis of the pad is bound to the object used for drawing the object, and is not actively changed by the pad when new objects are added to the pad! Meaning that very often you newly added objects could be plotted way outside the frame without manual intervention. You could use new objects such as THStack and TMultigraph to "mitigate" this, but why should be need to actively create a new object for this?

Now, after saying all of this, why am I still choosing to use ROOT? why not find a new library all together? ROOT still has some niftly tricks that I have grown rather attached to: tweaking and saving plots on the fly using the TBrowser interface makes finilising the publication plots so much easier, not to mention the immense RooFit plotting functions would be incredibly difficult to re-implement. So my final decision was to write a nice wrapper class to contain these stuff, so I only need to worry about these issues once.

# General design guide for custom library

First up is a custom function for translating the units to the ROOT static datatype, so TCanvas declaration could look like `TCanvas(mm(60),mm(70))`, font changes could look like `SetTextFace/Size(face(helvetica)/pt(12))`. Next is the more interesting parts:

-   **Wrapping up the Canvas and Pad**. Canvases are exclusively used for file saving and containing pads. Instead of Draw calls, user can now user the `Pad.PlotObj` function to ensure the object is being plotted on the pad. The saving functions also call on standard UNIX tools (ghostscript and imagemagik) to fixe the image format issues we mentioned above.

-   **Pad specialisation**. Additional specialisation to Pad are made to make the generated plots more inline with the CMS plotting convention (fixed-width bins should not have x error bars... ), as well has handling the more tedious tasks of axis scaling, legend generation, and histogram stacking automatically. This is particularly fun as it could plot RooFit object and ROOT object using the same interface!

-   **Canvas specialisation** For commonly used layouts and default canvas sizes. Such as the commonly used ratio plots, and functions for generation extended plots. They also pass through the Pad functions to look as if the objects are being plotted directly on the canvas!

# Sneak Peak

The official documentation would be coming soon$^{TM}$ (I'm still wrestling with Doxygen to try and get the documentation to look nich), but if you want a quick peak, the library is now public on [Github](https://github.com/yimuchen/UserUtils/tree/master/PlotUtils)! (Expect major tweaks to the documentation structure in the near future, so don't be forking it yet). But before that, here is a quick peak at what the function could do (the code below doesn't include the various `SetStyle`, `SetColor` functions and object generation):

```cpp
// Top raw object plotting
plt::Ratio1DCanvas c;
c.PlotHist( hist3,
    plt::PlotType( plt::histstack ), plt::EntryText( "Bkg_{1}: VV" ) );
c.PlotHist( hist2,
  plt::PlotType( plt::histstack ), plt::EntryText( "Bkg_{2}: HH" ) );
c.PlotHist( hist1,
  plt::PlotType( plt::histstack ), plt::EntryText( "Bkg_{3}: TT" ) );
c.PlotHist( histsum,
  plt::PlotType( plt::histerr ),   plt::EntryText( "Bkg_{1} Unc." ) );
c.PlotHist( data,
  plt::PlotType( plt::scatter ),   plt::EntryText( "Data" ) );

// Bottom pad automatic generation
c.PlotScale( histsum, histsum,
  plt::PlotType( plt::histerr ), plt::TrackY( plt::TrackY::none ) );
c.PlotScale( data, histsum,
  plt::PlotType( plt::scatter ) );

// Other accessories
c.TopPad().SetHistAxisTitles( "M_{THTHTH}", plt::unit::GeVcc );
c.BottomPad().SetHistAxisTitles( "M_{THTHTH}", plt::unit::GeVcc );
c.BottomPad().Yaxis().SetTitle( "Data/Sim." );
c.DrawCMSLabel( "Ratio1DCanvas", "CWS" );
c.DrawLuminosity( 133.7 );
//c.SaveAsPDF( "testfig/ratio1dcanvas_test.pdf" );
c.SaveAsPNG( "testfig/ratio1dcanvas_test.png",200 ); //200DPI!
```

<figure>
  <img src="{{site.url}}/images/genimage/2018-05-19-PlotUtils/ratio1dcanvas_test.png"/>
   <figcaption>ROOT plotting, note the automatic stack generation and automatic legend generation! (The really tight margin is due to imagemagik trimming whites as well as the transparent part... I'm still searching for a solution)</figcaption>
</figure>

```cpp
plt::Ratio1DCanvas c( plt::RangeByVar(x) );

auto& fitgraph = c.PlotPdf( g,
    plt::EntryText( "Fitted Bkg." ),
    RooFit::VisualizeError( *fit, 1, false ),
    RooFit::Normalization( 500, RooAbsReal::NumEvent ) );
auto& altgraph = c.PlotPdf( gx,
    plt::EntryText( "Alt. Bkg. Model" ),
    RooFit::Normalization( 500, RooAbsReal::NumEvent ) );
auto& datgraph = c.PlotData( d, plt::EntryText("Fake Data") );

c.PlotScale( fitgraph, fitgraph,
   plt::TrackY(plt::TrackY::none), plt::PlotType(plt::fittedfunc) );
c.PlotScale( altgraph, fitgraph,
   plt::TrackY(plt::TrackY::none), plt::PlotType(plt::simplefunc) );
c.PlotScale( datgraph, fitgraph,
  plt::PlotType(plt::scatter) );
c.BottomPad().Yaxis().SetTitle("Data/Fit");
c.DrawCMSLabel( "Ratio1DCanvas", "CWS" );
c.DrawLuminosity( 133.7 );
c.SaveAsPNG("ratio1dcanvas_roofit_test.png", 100); // 100 DPI
```

<figure>
  <img src="{{site.url}}/images/genimage/2018-05-19-PlotUtils/ratio1dcanvas_roofit_test.png"/>
   <figcaption>RooFit plotting, note the similar interface and the direct use of the original RooFit plotting commands!</figcaption>
</figure>


# Small print

I'm rather burnt out of the project at the moment, so don't expected very active maintainence for a while. There is still quite a bit of tweaking of the default values that needs to be done. Most likely there will be various issues with the plotter still not behaving properly (#JustROOTThings). But for 95% of my personal use cases, this should do fine!
