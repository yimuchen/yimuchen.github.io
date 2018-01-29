
// Toggling > < section of right navigation bar.
$(document).ready(function() {
  $(".right-nav-button").on("click", function() {
    var el = $(this);
    el.text() == el.data("text-swap") ?
      el.text(el.data("text-original")) :
      el.text(el.data("text-swap"));
    el.text() == el.data("text-swap") ?
      el.siblings('.right-nav').addClass("shown") :
      el.siblings('.right-nav').removeClass("shown");
  });
});
