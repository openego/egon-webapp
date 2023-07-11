// Get references to the buttons
var button2035 = document.getElementById("2035");
var button100RE = document.getElementById("100RE");
var description_2035 = document.getElementById("scenario-description-egon2035");
var description_100RE = document.getElementById("scenario-description-100RE");

// Add click event listeners
button2035.addEventListener("click", function () {
    button100RE.classList.remove("active");
    button2035.classList.add("active");
    toggleLayers("2035"); // Show layers for 2035 scenario
    description_100RE.style.display = "none";
    description_2035.style.display = "";
});

button100RE.addEventListener("click", function () {
    button2035.classList.remove("active");
    button100RE.classList.add("active");
    toggleLayers("100RE"); // Show layers for 100RE scenario
    description_2035.style.display = "none";
    description_100RE.style.display = "";
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
