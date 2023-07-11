const mapView = document.getElementById("mapView");
const offcanvasAbout = document.getElementById('offcanvasAbout');
const offcanvasResults = document.getElementById('offcanvasResults');
const offcanvasPrivacy = document.getElementById('offcanvasPrivacy');
const offcanvasImprint = document.getElementById('offcanvasImprint');

const offcanvasInstances = {
  about: new bootstrap.Offcanvas(offcanvasAbout),
  results: new bootstrap.Offcanvas(offcanvasResults),
  privacy: new bootstrap.Offcanvas(offcanvasPrivacy),
  imprint: new bootstrap.Offcanvas(offcanvasImprint)
};

mapView.onclick = function() {
  Object.values(offcanvasInstances).forEach(function(offcanvas) {
    offcanvas.hide();
  });
};
