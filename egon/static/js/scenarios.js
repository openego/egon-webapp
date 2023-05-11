// Get references to the buttons
var button2035 = document.getElementById("2035");
var button100RE = document.getElementById("100RE");

// Add click event listeners
button2035.addEventListener("click", function () {
    PubSub.publish(mapEvent.SCENARIO_CHANGE, "2035");
    button100RE.classList.remove("active");
    button2035.classList.add("active");
});

button100RE.addEventListener("click", function () {
    PubSub.publish(mapEvent.SCENARIO_CHANGE, "100RE");
    button2035.classList.remove("active");
    button100RE.classList.add("active");
});
