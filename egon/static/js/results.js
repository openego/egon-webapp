/* globals activateChoropleth, deactivateChoropleth */

const layerSwitches = document.querySelectorAll(".choropleth");

layerSwitches.forEach(layerSwitch => {
  layerSwitch.addEventListener("change", function() {
    if (this.checked) {
      layerSwitches.forEach(otherSwitch => {
        if (otherSwitch.id !== layerSwitch.id) {
          otherSwitch.checked = false;
          deactivateChoropleth(null, otherSwitch.id);
          map.setLayoutProperty(otherSwitch.dataset.geomLayer, "visibility", "none");

        }
      });
      map.setLayoutProperty(layerSwitch.dataset.geomLayer, "visibility", "visible");
      activateChoropleth(null, layerSwitch.id);
    } else {
      map.setLayoutProperty(layerSwitch.dataset.geomLayer, "visibility", "none");
      deactivateChoropleth(null, layerSwitch.id);
    }
  });
});
