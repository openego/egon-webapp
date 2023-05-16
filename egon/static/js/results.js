/* globals activateChoropleth, deactivateChoropleth */

const layerSwitches = document.querySelectorAll(".form-check-input");

layerSwitches.forEach(layerSwitch => {
  layerSwitch.addEventListener("change", function() {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, layerSwitch.value);
    if (this.checked) {
      layerSwitches.forEach(otherSwitch => {
        if (otherSwitch.id !== layerSwitch.id && otherSwitch.dataset.geomLayer === layerSwitch.dataset.geomLayer) {
          otherSwitch.checked = false;
        }
      });
      map.setLayoutProperty(layerSwitch.dataset.geomLayer, "visibility", "visible");
      activateChoropleth(null, layerSwitch.id);
    } else {
      map.setLayoutProperty(layerSwitch.dataset.geomLayer, "visibility", "none");
        if (layerSwitch.id !== layerSwitch.dataset.geomLayer) {
          deactivateChoropleth(null, layerSwitch.id);
        }
        if (layerSwitch.id === "mv_grid_district_data" ) {
          deactivateChoropleth(null, layerSwitch.id);
        }
    }
  });
});
