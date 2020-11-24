---
layout: post
title: Sennheiser Momentum 3 - A 1 year reflection
description: My thoughts on my new head phones.
tags: [hardware, thoughts]
modified: 2020-11-24
---

So I have daily driven the Sennheiser Momentum 3 for nearly 1 year now, do my
initial impressions hold up? Will I recommend this product? Here are some
additional thoughts that I have collected since I got this pair of headphones.

## The Good

First up is, of course, how does the headphone sound. After 1 year, I can only
say that I have not complaints with audio quality of the Momentum 3. I'm in no
way and audio setup professional, but from my experience, audio quality is
something that slowly creeps up on you the longer you use a better setup. For a
short session, I was switching between the Sennheiser and my old headset when
debugging audio sharing issues between my two machines, and the difference
immediate, the amount of bass, the richness of the vocals, how open the audio
environment feels (I believe this is technically called “wideness of sound
stages”? But I maybe wrong.) One of the biggest difference that would be
objectively beneficial is that I notice I no longer need to crank up the
headphone volume when listening to dialogs when watching movies, the audio
details is just presented much better by the Sennheiser. How good the Sennheiser
is at the price point of nearly $400 at the date of purchase, I cannot comment
on, but for the sake of enjoying music and other multimedia, I would say the
investment in these headphones is worthwhile.

Next up is active noise-cancelling function of the Sennheiser. My impression have
not changed from initial impressions since the beginning of this year: it's not
stellar, but serviceable. If perfect external silence is what you are after, then
this is definitely not the product for you. What it has done for me is
suppressing most common home office noises to an easily ignorable level. You will
still immediately notice when the AC system turns on and when construction work
starts outside, but the noise level is low enough to the point that I don't
immediate reach for the volume nob. This same story holds true for when I was on
an airplane at the beginning of the year, with only a small adjustment to the
overall volume required. For the sake of auditory hygiene, my original goal for
finding a nice set of noise-cancelling headphones, this product serves nicely.

## The Bad

The Sennheiser is not without problem. The long-standing problem of a strange
buzzing noise in the left ear was a long struggle to get rid of. It is usually
very faint, but is mainly exacerbated by the fact that the buzzing only occurs in
one ear (audio imbalance is an annoying thing). Though the cause is now known to me:
ground contamination, getting rid of this turned out to be such a difficult
endeavor that I feel has some fault with the design of the Momentum 3.

The immediate culprit is the power line networking equipment that I have for my
home network setup, which works by injecting high frequency network signals into
the copper used for power delivery and grounding. Testing was done simply by
artificially maxing out the network usage of devices in my room (either by the
speedtest website or the `iperf` command). Since power lines as not designed to
carry high frequency signals, suppression of such noises can be achieved
relatively simply by moving the power line network unit to the opposite end of my
room.

But then the more sinister side of this issue began to show. I notice that the
buzz doesn't entirely go away, even after these fixes. As soon as I start my
desktop, the buzzing appears, as long as my headphone has some sort of electrical
connection to the any electrical outlet: either via the ground shield of the 3.5
mm headphone jack, or by the USB power cable connected to a 5.0V power adaptor.
In particular, the existence of a humming with no audio connection, seems to
indicate that this isn't a typical [ground loop][groundloop] issue that most
high-end audio forums seems to suggest. So this is either an issue of my desktop
power supply having lack-luster back-propagation mitigation circuits, or the left
side of the headphone having inadequate power ripple suppressing circuitry.
Another hint as to one of these two being the issue is that the humming doesn't
appear to occur at 60Hz, but at 120Hz, suggesting that this noise is coming from
some rectifier circuit, and not a simple ground displacement.

Of course, there is an obvious solution: use the headphone in wireless mode:
Bluetooth for passing audio signal, and disconnect the USB power cord when using
the headphone. I guess I'm more old-fashioned in this sense: I prefer my
connections to be wired to reduce the possibility of random disconnects and deep
discharge of the battery in case I forget to replug the power cord. If I insist
on wired operation, then I would need to either find a “better” power supply for
my desktop, or a power isolating power strip for the various components. But even
then, it wouldn't guarantee that the issue will go away, or maybe introduce more
issues of their own. If ground loop was to occur, the use of an
[unbalanced][balanced_audio] 3.5mm audio jack for the wired inputs means that
options for eliminating ground loops via ground lifting would be limited. There
are adaptors, of course, but that will take up even more desk space, something
that I am already lacking.

I've managed to arrange all the cables on my desk to make this issues as
negligible as possible. Right now, as long as something is playing in my left
ear, I would need to be actively looking out for the buzz to be able to hear it,
but it is not entirely solved.

## My final thought for this year

For all its faults, I greatly enjoyed daily driving the Momentum 3 over the past
year. What it does well, it does great, and event the annoying fault has been
largely resolved, even if not perfectly. Plus, it gave me a reason to read about
all sorts of fun audio engineering stuff. Hopefully I will be able to find a more
complete solution in the future.

[groundloop]: https://en.wikipedia.org/wiki/Ground_loop_(electricity)
[balanced_audio]: https://en.wikipedia.org/wiki/Balanced_audio