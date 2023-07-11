const mapView = document.getElementById("mapView");
const offcanvasDocumentation = document.getElementById('offcanvasDocumentation');
const offcanvasResults = document.getElementById('offcanvasResults');
const offcanvasSources = document.getElementById('offcanvasSources');
const offcanvasContact = document.getElementById('offcanvasContact');

const offcanvasInstances = {
  documentation: new bootstrap.Offcanvas(offcanvasDocumentation),
  results: new bootstrap.Offcanvas(offcanvasResults),
  sources: new bootstrap.Offcanvas(offcanvasSources),
  contact: new bootstrap.Offcanvas(offcanvasContact)
};

mapView.onclick = function() {
  Object.values(offcanvasInstances).forEach(function(offcanvas) {
    offcanvas.hide();
  });
};
