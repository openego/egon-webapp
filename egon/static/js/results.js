/* globals activateChoropleth, deactivateChoropleth */

const layerSwitches = document.querySelectorAll(".form-check-input");

layerSwitches.forEach(layerSwitch => {
  layerSwitch.addEventListener("change", function() {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, layerSwitch.value);
    layerSwitches.forEach(otherSwitch => {
        if (otherSwitch.id !== layerSwitch.id && otherSwitch.dataset.geomLayer === layerSwitch.dataset.geomLayer) {
          otherSwitch.checked = false;
        }
      });
      map.setLayoutProperty(layerSwitch.dataset.geomLayer, "visibility", "visible");
      activateChoropleth(null, layerSwitch.id);
  });
});
