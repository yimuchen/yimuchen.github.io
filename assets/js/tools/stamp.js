function StampCalculate() {
  var denominations = GetDenominations();
  var target = parseInt(document.getElementById("stamp-target-input").value)
  if (!target || target <= 0) {
    alert("函件資費必須為大於零的整數");
  } else if (target > 10000) {
    alert("請不要輸入不合理的郵資")
  } else {
    var ans = OptimalChange(target, denominations);
    AppendResults(target, ans);
  }
}

function StampClear() {
  document.getElementById("stamp-ans").innerHTML = "";
  document.getElementById("stamp-debug").innerHTML = "";
  document.getElementById("stamp-additional-types").value = "";
  document.getElementById("stamp-target-input").value = "";
}

function GetDenominations() {
  denominations = []

  // Getting predefined stamp types
  var idquerylist = document.querySelectorAll('[id^=stampvalue]');
  for (var i = 0; i < idquerylist.length; i++) {
    var idresult = idquerylist[i].id;
    var idvalue = parseInt(idresult.replace('stampvalue', ''));
    if (document.getElementById(idresult).checked) {
      denominations.push(idvalue);
    }
  }

  // Getting user inputs
  var inputlist = document.getElementById("stamp-additional-types").value.split(" ")
  for (var i = 0; i < inputlist.length; i++) {
    inputint = parseInt(inputlist[i]);
    if (inputint && inputint > 0) {
      denominations.push(inputint)
    }
  }

  // Stripping to unique and sorting
  denominations = denominations.filter(function(item, pos) {
    return denominations.indexOf(item) == pos;
  });

  denominations.sort(function(a, b) {
    return a - b;
  });
  return denominations;
}

/**
 * Main DP algorithm for determining optimal stamp configuration to use.
 * Returns answer as associative array with stamp type as key and value as number of stamps to use.
 * @param       {integer} amount        Total amount wished for make
 * @param       {array} denominations Types of stamps available
 * @constructor
 */
function OptimalChange(amount, denominations) {
  // Initializing dynamic programming array
  var number_of_coins = [];
  var previous_amount = [];
  for (var i = 0; i <= amount; i++) {
    number_of_coins[i] = 2147483647;
    previous_amount[i] = -1;
  }
  // Starting point at 0, no coins required, no previous amount.
  number_of_coins[0] = 0;
  previous_amount[0] = 0;

  // Dynamic programming of amount array
  for (var present_amount = 0; present_amount <= amount; present_amount++) {
    // First loop iterates over the sub-sum array.
    for (var j = 0; j < denominations.length; j++) {
      // second loop iterates over all possible coins, calculate possible next values
      var coin_val = denominations[j];
      var next_amount = present_amount + coin_val;
      if (next_amount > amount) {
        continue;
      } // Skipping overflow cases.
      if (number_of_coins[next_amount] > number_of_coins[present_amount] + 1) {
        number_of_coins[next_amount] = number_of_coins[present_amount] + 1;
        previous_amount[next_amount] = present_amount
      }
    }
  }

  // Storing the results in associative array
  var ans = {}
  for (var i = 0; i < denominations.length; i++) {
    ans[denominations[i]] = 0;
  }

  var remainer = amount;
  while (remainer > 0 && previous_amount[remainer] != -1) {
    var used_value = remainer - previous_amount[remainer];
    ans[used_value] = ans[used_value] + 1;
    remainer = previous_amount[remainer];
  }

  for (var i = 0; i < denominations.length; i++) {
    if (ans[denominations[i]] == 0) {
      delete ans[denominations[i]]
    }
  }
  return ans;
}

function AppendResults(target, answer) {
  var ansstr = "<b>總計：" + target + "元</b>　";

  // special case for empty solution
  if (Object.keys(answer).length == 0) {
    ansstr += "(找不到答案)"
  }

  for (var key in answer) {
    var coin_count = answer[key]
    ansstr += key + "元(" + coin_count + "張)　"
  }
  document.getElementById("stamp-ans").innerHTML += ansstr + "<br>";
}


// function GenerateDefinedList() {
//   var debugstr = "";
//   for ( var i = 0 ; i < fixed_denominations.length ; i++ ) {
//     var typestr = "";
//     var stamptype = fixed_denominations[i]
//     typestr += "<li>"
//     typestr += "<input type=\"checkbox\" id=\"stamp-value" + stamptype.value + "\"" ;
//     if( stamptype.default ){
//       typestr += " checked ";
//     }
//     typestr += " />"
//     typestr += "<label for=\"stamp-value" + stamptype.value + "\">"
//     typestr += "<span>" + stamptype.value + " 元</span>"
//     typestr += "<img src=\"" + stamptype.image + " \" />"
//     typestr += "</label>"
//     typestr += "</li>"

//     //alert( typestr );
//     document.getElementById("predefined-stamps").innerHTML += typestr;
//   }
// }
// GenerateDefinedList(
