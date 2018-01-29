/*************************************************************
 *
 * Filename:spec-page.js
 * Author: yimuchen
 * Description: Javascript for user interactive elements in specs page
 * Javascripts is used for handling the CSS class toggling, while the
 * CSS found in the _sass/_specs.scss actually defines the dynamic
 * behaviour.
 *
 *************************************************************/
// Class toggling for checkboxes in tools section
$(document).ready(function() {
  $('input[type="checkbox"]').on('change', function() {
    $('input[type="checkbox"]').not(this).prop('checked', false);
    var item_state = $(this).prop('checked');
    var item_change = $(this).attr('id') + '_detail';

    $('.tool_detail').each(function() {
      if ($(this).attr('id') != item_change) {
        $(this).slideUp(300, 'swing');
      } else {
        if (item_state) {
          $(this).slideDown(300, 'swing');
        } else {
          $(this).slideUp(300, 'swing');
        }
      }
    });
  });
});

// Force-clearing all checkboxes on document load.
$(document).ready(function() {
  $(':checkbox:checked').prop('checked', false);
});


// Random Facts display
function GetRandomFactId() {
  var fact_count = document.querySelectorAll('.fact_container .fact_item').length;
  var fact_display = 0;
  while (fact_display == 0) {
    fact_display = Math.floor((Math.random() * fact_count) + 1);
    if ($('[id=fact_item_' + fact_display + ']').hasClass('shown')) {
      fact_display = 0;
    }
  }
  return fact_display;
}


// Showing a random fact
function ShowRandom() {
  var new_display = GetRandomFactId();
  $('[id^=fact_item_]').each(function() {
    $(this).removeClass('shown');
  });
  $('[id^=fact_item_' + new_display + ']').addClass('shown');
}

// Showing random on startup.
$(document).ready(ShowRandom);

// Showing random every n milliseconds
window.setInterval(ShowRandom, 30 * 1000);



// Class toggle for the right navigation column.
$(document).ready(function() {
  $('.spec-nav-item').on('click', function() {
    $('.right-nav').removeClass('shown');
    $('.right-nav-button').text($('.right-nav-button]').data('text-original'));
  });
});
