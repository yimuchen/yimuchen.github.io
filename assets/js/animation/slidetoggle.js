/****************************************************
 *
 * Filename: slidetoggle.js
 * Author:   Enoch Chen
 * Description: Common settings for slidetoggle objects
 *
 ****************************************************/
$(document).ready(function() {
  $(".slidetoggle_controller").on( "click", function() {
    $(this).siblings(".slidetoggle_target").slideToggle( 500, 'swing' );
    $(this).toggleClass("shown");
  });
});
