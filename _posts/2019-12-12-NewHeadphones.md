---
layout: post
title: Sennheiser Momentum 3 - My thoughts
description: My thoughts on my new head phones.
tags: [hardware, thoughts]
modified: 2019-12-12
---

When travelling on the plane to and from Geneva back in November, I noticed that
to combat the airplane noise when using my headset, I need to turn the volume up
to uncomfortable levels, to the point that I was warned by the media station on
the plane seat. More alarming still, I noticed that I actually got used to the
volume level after a couple of hours into a movie. As flights would likely become
more frequent in the coming years of my PhD degree, for the sake of my ears, I
thought it was time to invest in a set of new noise-cancelling headphones.

## Choosing the headphone

Noise-cancelling headphones has been on my tech-news radar for a while. I know
that bad implementations of noise-cancelling would lead to a more noisy
experience and prompt the notorious “cabin-pressure” effect. During the
thanksgiving season, I had the chance to head over to larger best-buy stores to
try out a few headsets. I ran into bad implementations (one from skull-candy had
an annoying hissing noise that is very audible above the leaked in noise), as
well as being thoroughly impressed with how good noise cancelling can be in the
Bose any Sony line up.

Noise cancelling is not the only thing to consider when a headset. How a set of
headphone sounds is arguably more important for headset. Having tested the
Sennheiser line-up as having decent/OK noise-cancelling from my trip, decided
that I liked the Sennheiser's a bit more than what Bose and Sony had to offer. To
be entirely honest, during that time I didn't try out the specific headphone that
I eventually bought (I only got to try the PXC550 and Momentum 2), but I decided
to trust the Sennheiser brand, to went for the Sennheiser Momentum 3.

## My current experience

First and fore most, I don't have the budget to tryout headphone on a regular (my
previous headset was an Audio Technica ATH-SJ33 bought over 3 years ago), so I
probably have no idea what I am talking about when it comes to critiquing the
audio quality. That being said, I really do like the way they sound. Whether it
is using the 3.5 mm line to connect to my PC/laptop, or using the USB type-C
cable to use the headphones in built DAC, they both contain significantly more
details than my previous headset. The 3.5 mm cable does make the output quieter
(the impedance quoted from the product page is 450 Ohms, so most likely the DAC
on my computer is struggling to drive them), but still within acceptable ranges.
As to how good they are compared to other headsets, I have no way of comparing,
so no more comments on sound quality.

The noise-cancelling capability is as tested: decent/OK. The loudest source of
consistent noise in my room is the AC unit of our apartment, while the Sennheiser
blocks most of the rumbling low-frequency noise very well, the higher frequency
noise still gets in as a slight hiss that slightly audible when there is audio
playing. This is still very acceptable, as previously when the AC kicks in, I'm
nearly always tempted to dial up my volume because it in the way of what I was
listening, whereas now, it is more of a brief pause when the hissing sounds up
then thinking to myself: “Oh, I guess the AC kicked in”, the moving on. So all in
all, the noise-cancelling is doing its job.

\[Update 2019-12-30\] On my plane ride back to Taiwan, the noise cancelling is very
serviceable, with the low frequency rumbling being clearly blocked out, reducing
the engine noise to a low volume, higher-pitched faint hissing that is
unobtrusive to movie viewing experiences and definitely saved ear pains due to
uncomfortably loud volumes. The office-oriented design of not being able to fold
flat of the Momentum 3 does make wearing the headphones rather unwieldy without
putting the headphones away entirely, but it didn't really matter for my using
habits.

Now for a random story. When operating in wired mode, whether USB or the 3.5 mm
audio line, there was a strange popping noise in the left ear. It took me a week
to work out, but it turns out it as a peculiar ground loop issue with my computer
and the power-line network unit that somehow only the left ear was picking up.
Moving the power-line unit to another outlet solved the issue, but I'm not sure
if this is a quirk of higher end audio gear, or just something with particular
with the Momentum 3. But that was a strange issue that I needed solving.

\[Update 2019-12-30\] Another peculiar episode occurred when attempting to
playback lossless audio files. Weird and irregular popping sounds started
appearing every 1 minute or so, which indicated to me a buffering problem. It has
since been fixed using [pulseaudio
settings](https://wiki.archlinux.org/index.php/PulseAudio/Troubleshooting#Setting_the_default_fragment_number_and_buffer_size_in_PulseAudio),
but just note that this is yet another issue that one might need to deal with.

## Open questions and closing words

\[Update 2019-12-30\] There is a strange bug that after the firmware update of in
early December, the Momentum 3 just doesn't work in USB mode with Linux, I
avoided this thanks to the second unit I got to fix the broken botton. I'm not
sure if this is fixed in future updates, as the Senheisser mobile app is now
bugged out with two Momentum devices listed in the app that both cannot be
connected. I'm happy with the headphone interface as is, so I wouldn't be
attempting to solve this anytime soon (I'm more old-fashioned when it comes media
control, and prefer to control everything manually instead of through smart
gestures or headphone interfaces).

All in all, I would say I am happy with the overall experience, but at the same
time, I have a hard time recommending this particular product, with a weird
episode of the ground loop taking over a week to diagnose, and the first unit
that I received had a broken volume down button. As a Linux user, I'm no stranger
to debugging random issues, but that doesn't make it less frustrating when
working with the product what I paid a considerable amount to buy.
