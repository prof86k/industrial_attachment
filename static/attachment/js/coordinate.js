
const side_nav_item = document.getElementById("side-nav");
const side_nav_close = document.getElementById("cancel");
const top_nav = document.getElementById("nav-header");
const main_content = document.getElementById("main-content");


top_nav.addEventListener("click", function () {
    
    side_nav_item.style.display = "block";
    side_nav_item.style.transition = " all 0.9s"
    side_nav_close.style.display = "block"

})
side_nav_close.addEventListener("click", function () {
    
    side_nav_item.style.display = "none";
    side_nav_item.style.transition="0.9s"
    side_nav_close.style.display = "none";

});





var exampleModal = document.getElementById('exampleModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var recipient = button.getAttribute('data-bs-whatever')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  var modalTitle = exampleModal.querySelector('.modal-title')
  var modalBodyInput = exampleModal.querySelector('.modal-body input')

  modalTitle.textContent = 'New message to ' + recipient
  modalBodyInput.value = recipient
})






const coordinates_values = document.getElementById("submit-btn");

coordinates_values.addEventListener("click", function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const latitude_pos = position.coords.altitude;
            const longitude_pos = position.coords.latitude;
            // put the coordinates somewhere
            document.getElementById("id_latitude").value = latitude_pos;
            document.getElementById("id_longitude").value = longitude_pos;
            console.log(latitude_pos + " " + longitude_pos);
        });
    } else {
        alert("Please Turn Your Location on");
    }
});
