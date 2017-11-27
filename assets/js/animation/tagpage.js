/****************************************************
 *
 * Filename: tagpage.js
 * Author:   Enoch Chen
 * Description: Interavitve elements for tag page sections
 * 
****************************************************/
$(document).ready(function() {
   $(".main_tag_button").on("click" , function(){
      $(this).siblings(".sub_container").toggle(400);
   });

   $(".sub_tag_button").on("click", function(){
      $(this).siblings(".post_container").toggle(400);
   });
});
