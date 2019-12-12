var resistor_string = ""
var resistor_set = [];
var solution_list = [];
var target = 5;
var tolerance = 0.05;
var total_solutions = 0;
var sum_type = parallel;

function abs(x) {
  if (x > 0) { return x; }
  else { return -x; }
}

function error(val) {
  return abs(val - target) / target;
}

function series(input, length) {
  var ans = 0;
  for (var i = 0; i < length; ++i) {
    ans += input[i];
  }
  return ans;
}

function parallel(input, length) {
  var ans = 0;
  for (var i = 0; i < length; ++i) {
    if (input[i] > 0)
      ans += 1 / input[i];
  }
  return 1 / ans;
}

function run_combination(input, current_idx) {
  if (current_idx == input.length) {
    if (error(sum_type(input, input.length)) < tolerance) {
      total_solutions += 1;
      solution_list.push(input.slice()); // passing a copy of the input
      update_results();
    }
  }
  else {
    var direction = sum_type == parallel ? +1 : -1;
    var start_idx = sum_type == parallel ? 0 : resistor_set.length - 1;
    if (current_idx > 0) {
      start_idx = resistor_set.indexOf(input[current_idx - 1]);
    }
    for (var i = start_idx; i < resistor_set.length && i >= 0; i += direction) {
      input[current_idx] = resistor_set[i];
      if (
        ((sum_type == parallel) &&
          sum_type(input, current_idx + 1) < target * (1 - tolerance)) ||
        ((sum_type == series) &&
          sum_type(input, current_idx + 1) > target * (1 + tolerance))
      ) { continue; }
      run_combination(input, current_idx + 1);
    }
  }
}

function make_resistance_string(input) {
  mult = input < 1e-9 ? 1e-12 :
         input < 1e-6 ? 1e-9 :
         input < 1e-3 ? 1e-6 :
         input < 1 ? 1e-3 :
         input < 1e3 ? 1 :
         input < 1e6 ? 1e3 :
         input < 1e9 ? 1e6 : 1e9;
  postfix = input < 1e-9 ? 'p' :
            input < 1e-6 ? 'n' :
            input < 1e-3 ? 'u' :
            input < 1e0 ? 'm' :
            input < 1e3 ? ' ' :
            input < 1e6 ? 'k' :
            input < 1e9 ? 'M' : 'G';
  return (input / mult) + postfix;

}

function resistance_from_string(input) {
  const multipler_postfix = 'pnumkKMG';
  var mult = input.charAt(input.length - 1)
  if (multipler_postfix.includes(mult)) {
    input = input.substring(0, input.length - 1)
  }
  mult = mult == 'p' ? 1e-12 :
         mult == 'n' ? 1e-9 :
         mult == 'u' ? 1e-6 :
         mult == 'm' ? 1e-3 :
         mult == 'k' ? 1e3 :
         mult == 'K' ? 1e3 :
         mult == 'M' ? 1e6 :
         mult == 'G' ? 1e9 : 1;

  return temp = Number(input) * mult;
}

function update_results() {
  // Sorting the solution list.
  solution_list.sort(function (a, b) {
    // Comparing error first
    var error_diff = error(sum_type(a, a.length)) - error(sum_type(b, b.length));
    if (error_diff != 0) {
      return error_diff;
    }

    // Then comparing the number of elements.
    var len_diff = a.length - b.length;
    if (len_diff != 0) {
      return len_diff;
    }

    // Finally comparing the number of unique components
    var a_unique = a.filter((v, i, a) => a.indexOf(v) === i);
    var b_unique = b.filter((v, i, a) => a.indexOf(v) === i);
    return a_unique.length - b_unique.length;
  });

  // Keeping only the first 100 solutions
  solution_list.slice(0, 100);

  var html = `
  <style>
  .solution_container {
    text-align : center;
    max-height: 500px;
    min-height: 300px;
    overflow: scroll
  }
  .solution_box {
    text-align : left;
    display: inline-block;
  }

  .solution_combo {
    text-align:right;
    width: 15em;
    display: inline-block;
    padding: 5px;
  }
  .solution_total {
    text-align: right;
    width: 5em;
    display: inline-block;
    padding: 10px
  }
  .solution_error {
    text-align: left;
    width: 5em;
    display: inline-block;
    padding: 5px;
  }

  </style>
  `

  html += 'Total number of solutions: ' + total_solutions;
  if (total_solutions > 100) {
    html += '(Showing closest 100 solutions)';
  }

  html += '<div class=solution_container>';
  html += '<div class=solution_box>'
  for (var i = 0; i < solution_list.length; ++i) {
    var val = sum_type(solution_list[i], solution_list[i].length)

    html += '<div class="solution_combo">'
    for (var j = 0; j < solution_list[i].length; ++j) {
      if (j != 0) {
        if (sum_type == parallel) { html += ' || '; }
        else { html += ' + '; }
      }
      html += make_resistance_string(solution_list[i][j]);
    }
    html += '</div>';

    html += '<div class="solution_total">'
      + val.toFixed(2)
      + '</div>';

    html += '<div class="solution_error">'
      + (error(val) * 100).toFixed(1)
      + '% </div>'
    html += '<br/>';
  }
  html += '</div>'
  html += '</div>'

  document.getElementById('results').innerHTML = html;
}

function update_set() {
  var raw_set = resistor_string.split(/[\s,]+/)
  var multipler_postfix = 'pnumkKMG';
  resistor_set = []
  for (var i = 0; i < raw_set.length; ++i) {
    var temp = resistance_from_string(raw_set[i]);
    if (temp == temp && temp > 0) { // NaN and positive check
      resistor_set.push(temp);
    }
  }
  resistor_set = resistor_set.filter((v, i, a) => a.indexOf(v) === i);
  resistor_set.sort(function (a, b) { return a - b; })
  print_resistor_set();
}

function print_resistor_set() {
  // Inlining the print style
  var html = `
  <style>
  .resistor_value {
    width:3em;
    max-width:3em;
    display: inline-block;
    text-align: right;
  }
  .resistor-container {
    text-align:center;
    padding-bottom: 2em;
  }
  .resistor-box {
    display: inline-block;
    max-width : 100%;
    text-align: left;
  }
  </style>
  <div class="resistor-container">
  <div class="resistor-box">
  `;

  var line_min = 1e-12;
  var line_max = 1e-11;
  while (line_max < 1e10) {
    var line_set = resistor_set.filter(function (v, i, a) {
      return (line_min <= v && v < line_max);
    })
    var line = '';
    for (var i = 0; i < line_set.length; ++i) {
      line += '<div class="resistor_value">'
        + make_resistance_string(line_set[i])
        + '</div>';
    }
    line += '<br/>'
    if (line_set.length > 0) {
      html += line;
    }

    line_min *= 10;
    line_max *= 10;
  }
  html += '</div></div>'
  document.getElementById('resistors').innerHTML = html;
}

function calculate() {
  solution_list = [];
  target = resistance_from_string(document.getElementById("target").value);
  tolerance = document.getElementById("tolerance").value;
  sum_type = document.getElementById("invsum").checked ? parallel : series;

  var input_list = [];
  total_solutions = 0;
  var num = document.getElementById("num").value;
  for (var i = 0; i < num; ++i) {
    input_list.push(0);
    run_combination(input_list, 0);
  }

  update_results();
}

function add_resistance() {
  resistor_string += ' ' + document.getElementById('resistance').value;
  update_set();
}

function load_E12() {
  resistor_string = '\
  1 10.0 100.0 1.K  10K 100K \
1.2 12.0 120.0 1.2K 12K 120K \
1.5 15.0 150.0 1.5K 15K 150K \
1.8 18.0 180.0 1.8K 18K 180K \
2.2 22.0 220.0 2.2K 22K 220K \
2.7 27.0 270.0 2.7K 27K 270K \
3.3 33.0 330.0 3.3K 33K 330K \
3.9 39.0 390.0 3.9K 39K 390K \
4.7 47.0 470.0 4.7K 47K 470K \
5.6 56.0 560.0 5.6K 56K 560K \
6.8 68.0 680.0 6.8K 68K 680K \
8.2 82.0 820.0 8.2K 82K 820K'
  update_set();
  document.getElementById('tolerance').value = 0.05
}

function load_E24() {
  resistor_string = '\
1.  10.0 100.0 1.0K 10K 100K \
1.1 11.0 110.0 1.1K 11K 110K \
1.2 12.0 120.0 1.2K 12K 120K \
1.3 13.0 130.0 1.3K 13K 130K \
1.5 15.0 150.0 1.5K 15K 150K \
1.6 16.0 160.0 1.6K 16K 160K \
1.8 18.0 180.0 1.8K 18K 180K \
2.0 20.0 200.0 2.0K 20K 200K \
2.2 22.0 220.0 2.2K 22K 220K \
2.4 24.0 240.0 2.4K 24K 240K \
2.7 27.0 270.0 2.7K 27K 270K \
3.0 30.0 300.0 3.0K 30K 300K \
3.3 33.0 330.0 3.3K 33K 330K \
3.6 36.0 360.0 3.6K 36K 360K \
3.9 39.0 390.0 3.9K 39K 390K \
4.3 43.0 430.0 4.3K 43K 430K \
4.7 47.0 470.0 4.7K 47K 470K \
5.1 51.0 510.0 5.1K 51K 510K \
5.6 56.0 560.0 5.6K 56K 560K \
6.2 62.0 620.0 6.2K 62K 620K \
6.8 68.0 680.0 6.8K 68K 680K \
7.5 75.0 750.0 7.5K 75K 750K \
8.2 82.0 820.0 8.2K 82K 820K \
9.1 91.0 910.0 9.1K 91K 910K'
  update_set();
  document.getElementById('tolerance').value = 0.01
}

function load_UMD0603_resistor() {
  resistor_string = "\
1.0K 1.40K 3.32K 4.75K \
4.7 10 20 24.9 39 49.9 75 \
100 120 165 200 300 620 \
16.2K 34K 49.9K \
100K 150K \
"
  update_set();
  document.getElementById('invsum').checked = true;
}

function clear_resistors() {
  resistor_string = ''
  update_set();
}

document.addEventListener('DOMContentLoaded', function () {
  load_UMD0603_resistor();
  // document.getElementById('invsum').checked = false;
}, false);