---
layout: page
title: 電阻計算機 (Resistance calculator)
comments: false
modified: 2019-07-31
---

This is a tool for helping one get a reasonable resistance value given a limit
selection of resistor, by generating groups of parallel resistors. The rationale
for limiting the question to just parallel resistors/capacitors is that this is
the scenario that typically occurs in electronics experiments, particularly with
surface mount experiments: stacking components in parallel is much easier (in
most cases), than making extra space for components in series. Allowing the use
of components in both parallel and serial have the problem much too complicated
to write, so I'm limiting the use case to either just parallel or just series.

Be warned that this algorithm is currently very un-optimized, and can consume an
very large amount of memory. To help the algorithm end early, try using a smaller
tolerance or lower the maximum number of components allowed.

Since I this a tool primarily for my own use. I have loaded in some of the
components found in the UMDCMS electronics lab. All the code can be found on the
github repository of this blog.


<div html="1">

<h2>List of resistors</h2>
<div id="resistors"></div>

Add impedance values<div class="tooltip">[?] <span class="tooltiptext"> Add a
  list of impedance values, separated by spaces. The short hands like 100K, 15.6M
  can be used. The common multipliers 'p', 'n', 'u', 'm' 'k/K', 'M', 'G' may be used.</span>
</div>
<input type="text" id="resistance"/><button onclick="add_resistance()">Add</button><br/>

<button onclick="load_E12()">Load E12</button>
<button onclick="load_E24()">Load E24</button>
<button onclick="load_UMD0603_resistor()">UMD 0603 Resistor</button>
<button onclick="clear_resistors()">Clear</button>

<h2>Calculate</h2>

<table>
  <tr>
    <td>Target value</td>
    <td><input type="text" id="target"/></td>
  </tr>
  <tr>
    <td>Max number of components</td>
    <td><input type="text" id="num" value="3"/></td>
   </tr>
  <tr>
    <td>Tolerance</td>
    <td><input type="text" id="tolerance" value="0.05"/></td>
  </tr>
  <tr>
  <td>Calculation type</td>
  <td>
    <input type="radio" name="sum_type" id="sum" />Resistor Series/Capacitor Parallel<br/>
    <input type="radio" name="sum_type" id="invsum" />Resistor Parallel/Capacitor Series
  </td>
  </tr>
  <tr>
    <td></td>
    <td><button onclick="calculate()">Calculate</button></td>
  </tr>
</table>

<h2>Results</h2>
<div id="results"></div>
<div id="debug"></div>

<script src="{{site.url}}/assets/js/tools/resistor.js"></script>

</div>

------


## About the algorithm

The algorithm is basically brute forcing all possible combinations with an early
exist for when combination moves above/below the tolerance, since if calculating
resistance series, the total resistance can only go up, and there is not point in
trying more if already past the tolerance threshold (vice versa for resistance
parallel calculations). This is highly inefficient and very memory hungry, but is
easy enough to code in one afternoon, that is what I went with :/
