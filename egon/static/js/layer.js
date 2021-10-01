// Variables

const detailLayers = Array.from(document.getElementsByClassName("static-layer"));
const layerInputClass = ".form-check-input";


// Event Handler

map.on("load", function () {
  // Layers Detail Panel
  detailLayers.map(layerForm => {
    layerForm.addEventListener("change", () => {
      PubSub.publish(eventTopics.DETAIL_LAYER_SWITCH_CLICK, {layerForm});
    });
  });
  $(".layer-setup").find(".js-range-slider").change(function() {
    const layerForm = $(this).closest("form");
    PubSub.publish(eventTopics.DETAIL_LAYER_SLIDER_CHANGE, {layerForm});
  });
  $(".layer-setup").find(".django-select2").change(function() {
    const layerForm = $(this).closest("form");
    PubSub.publish(eventTopics.DETAIL_LAYER_SELECT_CHANGE, {layerForm});
  });
});


// Subscriptions

// On Initial Load
PubSub.subscribe(eventTopics.STATES_INITIALIZED, hideDetailLayers);

// Layers Detail Panel
PubSub.subscribe(eventTopics.DETAIL_LAYER_SWITCH_CLICK, checkLayerOfGivenLayerForm);
PubSub.subscribe(eventTopics.DETAIL_LAYER_SLIDER_CHANGE, filterChanged);
PubSub.subscribe(eventTopics.DETAIL_LAYER_SELECT_CHANGE, filterChanged);

// Subscriber Functions

function hideDetailLayers(msg) {
  detailLayers.map(layer => {
    turn_off_layer(layer);
    $(layer).find(layerInputClass)[0].checked = false;
  });
  return logMessage(msg);
}

function showDetailLayers(msg) {
  for (let i = 0; i < detailLayers.length; i++) {
    $(detailLayers[i]).find(layerInputClass)[0].checked = (store.cold.staticState & 2 ** i) === 2 ** i;
    check_layer(detailLayers[i]);
  }
  return logMessage(msg);
}

function checkLayerOfGivenLayerForm(msg, {layerForm}) {
  check_layer(layerForm);
  store.cold.staticState = get_static_state();
  return logMessage(msg);
}

function setDetailLayersOnDetailLayersSwitchClick(msg) {
  detailLayers.map(layer => {
    turn_off_layer(layer);
    $(layer).find(layerInputClass)[0].checked = false;
  });
  store.cold.staticState = get_static_state();
  return logMessage(msg);
}

function filterChanged(msg, {layerForm}) {
  const layer_id = get_layer_id(layerForm);
  const filters = get_layer_filters(layerForm);
  const layers = map.getStyle().layers.filter(layer => layer["id"].startsWith(layer_id));
  $.each(layers, function (i, layer) {
    set_filters(layer["id"], filters);
  })
  return logMessage(msg);
}


// Helper Functions

function get_layer_id(layer_form) {
  return $(layer_form).find(layerInputClass)[0].id;
}

function check_layer(layer_form) {
  if ($(layer_form).find(layerInputClass)[0].checked) {
    const layer_id = get_layer_id(layer_form)
    const activated_layers = turn_on_layer(layer_form);
    const layers = map.getStyle().layers.filter(layer => layer["id"].startsWith(layer_id));
    const deactivatedLayers = layers.filter(layer => !activated_layers.includes(layer["id"]));
    const waiting = () => {
      if (!map.isStyleLoaded()) {
        requestAnimationFrame(waiting);
      } else {
        $.each(deactivatedLayers, function (i, layer) {
          map.setLayoutProperty(layer["id"], "visibility", "none");
        })
      }
    };
    waiting();
  } else {
    turn_off_layer(layer_form);
  }
}


function turn_off_layer(layer_form) {
  const layer_id = get_layer_id(layer_form);
  const layers = map.getStyle().layers.filter(layer => layer["id"].startsWith(layer_id));
  $.each(layers, function (i, layer) {
    map.setLayoutProperty(layer["id"], "visibility", "none");
  })
}

function turn_on_layer(layer_form) {
  const layer_id = get_layer_id(layer_form);
  const filters = get_layer_filters(layer_form);
  const layers = map.getStyle().layers.filter(layer => layer["id"].startsWith(layer_id));
  $.each(layers, function (i, layer) {
    map.setLayoutProperty(layer["id"], "visibility", "visible");
    set_filters(layer["id"], filters);
  })
  return layers.map(layer => layer["id"]);
}

function get_layer_filters(layer_form) {
  let filters = [];

  let sliders = $(layer_form).find(".js-range-slider");
  sliders.each(function (index, slider) {
    filter_name = slider.id.slice(3);
    result = $(slider).data("ionRangeSlider").result;
    filters.push(
      {
        type: "range",
        name: filter_name,
        from: result.from,
        to: result.to
      }
    )
  });

  let selects = $(layer_form).find(".django-select2");
  selects.each(function (index, select) {
    filter_name = select.id.split("_").slice(0, -1).join("_");  // Remove layer name from filter name
    result = $(select).val();
    if (result.length > 0) {
      filters.push(
        {
          type: "dropdown",
          name: filter_name,
          values: result
        }
      )
    }
  });
  return filters;
}

function set_filters(layer, filters) {
  let map_filters = ["all"];
  for (let i = 0; i < filters.length; i++) {
    if (filters[i].type == "range") {
      lower_bound = [">=", ["get", filters[i].name], filters[i].from];
      upper_bound = ["<=", ["get", filters[i].name], filters[i].to];
      map_filters.push(lower_bound);
      map_filters.push(upper_bound);
    }
    if (filters[i].type == "dropdown") {
      equals = ["match", ["get", filters[i].name], filters[i].values, true, false];
      map_filters.push(equals);
    }
  }
  map.setFilter(layer, map_filters);
}
