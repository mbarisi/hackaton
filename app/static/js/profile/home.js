$(document).ready(function() {
    setInterval("ajaxd()",50000); // call every 10 seconds
});

function ajaxd() {
  //reload result into element with id "sysStatus"
  $("#sysStatus").reset();
  window.load("/home_user", function() {  });

}