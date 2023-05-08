/* globals activateChoropleth, deactivateChoropleth */

const layerSwitches = document.querySelectorAll(".form-check-input");

layerSwitches.forEach(layerSwitch => {
  layerSwitch.addEventListener("change", function() {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, layerSwitch.value);
    if (this.checked) {
      activateChoropleth(null, layerSwitch.id);
    } else {
      deactivateChoropleth(null, layerSwitch.id);
    }
  });
});
