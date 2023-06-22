// Get references to the buttons
var button2035 = document.getElementById("2035");
var button100RE = document.getElementById("100RE");

// Add click event listeners
button2035.addEventListener("click", function () {
    button100RE.classList.remove("active");
    button2035.classList.add("active");
    toggleLayers("2035"); // Show layers for 2035 scenario
});

button100RE.addEventListener("click", function () {
    button2035.classList.remove("active");
    button100RE.classList.add("active");
    toggleLayers("100RE"); // Show layers for 100RE scenario
});

function toggleLayers(scenario) {
    var layers = document.getElementsByClassName("layers__item");

    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];

        if (layer.dataset.scenario === scenario || layer.dataset.scenario === "both" ) {
            layer.style.display = ""; // Show the layer
        } else {
            layer.style.display = "none"; // Hide the layer
        }
    }
}
