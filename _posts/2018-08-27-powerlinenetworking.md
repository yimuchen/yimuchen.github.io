---
layout: post
title: Powerline networking
description: A nice solution for people having issues with Wifi networking in their house
tags: [computing, networking]
modified: 2018-05-19
image:
  feature: code_head_1.png
  credit: ensc
---

Having just moved to my apartment in the US, one of the most difficult things to
get used to coming from Taiwan was the scale of distance scale everything. Be it
commuting to school, grabbing groceries, even the size of the rooms in the
apartment for getting stuff in your own living space. While a large room is
generally a good thing, one important utility is heavily impacted by this merit:
Networking.

The typical Wifi router given by the service provider does a well enough job of
covering the apartment space. But for rooms further away from the router,
networking qualities suffers immensely from random packet drops, both downing
the networking speed to less than one-twentieth of what was being paid for,
makes video playbacks prone to random buffering, and incredibly stressful
moments when the internet decides to drop midway through filling an online form.

While my flatmate had previously bought a Wifi extender, the thing was a cheap
model, prone to overheating after prolong uses. While it recovered the speed to
one-tenth of the supposed speed, drops still occur on a regular, changing the
infrequent network dropage to a stable 30 minute dropage cycle. Since I
massively rely on networking for both work and entertainment, looking for a more
permanent solution was quite the priority.

Getting a "better" Wifi extender is an obvious solution, but not one I am very
fond of. Despite the many outlets that we have in our rooms, there wasn't one in
the long hallway that is the main reason for a long transmission distance, so
adding a Wifi extended would mean running a long power-extender along the
hallway (the inelegant solution that was previously being used with the cheap wifi
extender). Also, I am still of the opinion that a good signal requires a
physical wire, regardless of how far wireless technology has developed, but at
the same time. I also don't want to be fixing some 20+ meters of CAT6 cable
around the apartment, as I wasn't confident with my understanding of my lease
statements on wall/floor fixations, and neither was I confident with my
handywork at keeping such a long cable neat and functional.

The solution that I finally decided on taking up relied on the plentitude of
good wiring that already existed in the apartment: [Powerline
networking][powerline] kits, essentially using the powerline in your living
space as a massive ethernet signal transmission media, with the adapter machines
placed on outlets. For me, choosing the model to buy was rather more demanding
than I had thought:

* Must have wired connection to outside device: It would be nice to have wired
  connections for more network critical tasks such as access to remote machines
  and online-gaming.

* Must have wireess connections to outside devices: I have a phone, and also
  would be handing if I immediately need the network for someone in my room.

* Must of outlet by-pass. Nice to not have to give up a good power outlet just
  for a relatively low-power device.

The first two actually limits my choices to rather high-end devices that costs
around 130USD on amazon, but you can look for starter kits for around 35-50USD,
depending on the manufacturer if you are willing to give up a few functions. I
don't regret getting a rather overkill solution, as such supporting speeds also
future-proofs any potential services upgrades in the future.

Basic set up the device was easy, simple connect the adapter and extender end of
the kit into neighboring outlets, and and connect the adapter to the router, and
we are all set to go! Moved the extender to my bedroom, and yep! Getting nearly
the max outgoing networking speed all the way in my room at the end of the hall,
a near 30-50 times improvement!

There is still things that I haven't taken care of yet: The connection in the
wall is still not passward protected, so I cannot (yet) protect against
neighbors that manage to find out that we are potentially paying for their
network. But for the time being, I'm happy that I am able to have a quality and
reliable to the internet!

[powerline]: https://en.wikipedia.org/wiki/Power-line_communication
