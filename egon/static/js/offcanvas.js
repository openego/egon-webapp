const mapView = document.getElementById("mapView");
const newOffcanvasDocumentation = new bootstrap.Offcanvas(document.getElementById('offcanvasDocumentation'));
const newOffcanvasResults = new bootstrap.Offcanvas(document.getElementById('offcanvasResults'));
const newOffcanvasSources = new bootstrap.Offcanvas(document.getElementById('offcanvasSources'));
const newOffcanvasContact = new bootstrap.Offcanvas(document.getElementById('offcanvasContact'));
const offcanvasDocumentation = document.getElementById('offcanvasDocumentation');
const offcanvasResults = document.getElementById('offcanvasResults');
const offcanvassSources = document.getElementById('offcanvasSources');
const offcanvasContact = document.getElementById('offcanvasContact');

mapView.onclick = function() {
  newOffcanvasDocumentation.hide(offcanvasDocumentation);
  newOffcanvasSources.hide(offcanvassSources);
  newOffcanvasContact.hide(offcanvasContact);
  newOffcanvasResults.hide(offcanvasResults);
};
