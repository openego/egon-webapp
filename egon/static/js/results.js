/* globals activateChoropleth, deactivateChoropleth */

const layerSwitch = document.getElementById("transport_mit_demand");

layerSwitch.addEventListener("change", function() {
   PubSub.publish(mapEvent.CHOROPLETH_SELECTED, layerSwitch.value);
   if (this.checked) {
      activateChoropleth(null, "transport_mit_demand");
   }
   else {
      deactivateChoropleth(null, "transport_mit_demand");
   }
});
