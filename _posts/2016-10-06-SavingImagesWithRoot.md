---
layout: post
title: Saving images with ROOT
description: A complaint about using root to produce figures
tags: [root, c++, latex]
modified: 2016-10-16
image:
  feature: thoughts.jpg
  credit: ensc
---

Despite [ROOT](root.cern.ch) being a core programing library in high energy physics, it is so full of little undesirable "features" that makes it very frustrating to use. This is another one of those complaints.

## Lack of file formats
For comparison, it will be using the format that is most commonly used for displaying images on websites([cite](https://w3techs.com/blog/entry/the_png_image_file_format_is_now_more_popular_than_gif)): [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics). For the majority of times, ROOT outputing images as png works fine, but since root is aimed at scientific computing, the images one would want to use in their final works would be vector images rather than raster images. ROOT is very limited at producing vector graphics. On the [`TPad::SaveAs`](https://root.cern.ch/doc/master/classTPad.html#abb7a40ea658c348cdc8f6925eb671314) method reference, we could see the list of all the vector image formats supported by root:

* [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics)
* [PS](https://en.wikipedia.org/wiki/PostScript)
* [EPS](https://en.wikipedia.org/wiki/Encapsulated_PostScript)
* [PDF](https://en.wikipedia.org/wiki/Portable_Document_Format)

This might look well, but the actual results of these outputs all have major flaws

### SVG
Though SVG is a common image only vector graphics format, the output of ROOT for svg looks plain awful, and looks nothing like the PNG output.

### PS, EPS
Due to the so-called "ROOT flavoured latex", text rendering with latex symbol looks very inconsistent.

### PDF
Looks OK, but again, there are small differences of where the
