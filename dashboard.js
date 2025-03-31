document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_bus_routes")  // ✅ Fetch data from Flask route instead of static file
        .then(response => response.json())
        .then(data => {
            let routeDropdown = document.getElementById("bus_route");
            let stopDropdown = document.getElementById("bus_stop");

            for (let route in data) {
                let option = document.createElement("option");
                option.value = route;
                option.textContent = route;
                routeDropdown.appendChild(option);
            }

            routeDropdown.addEventListener("change", function () {
                let selectedRoute = this.value;
                stopDropdown.innerHTML = '<option value="">Select a Stop</option>';

                if (selectedRoute && data[selectedRoute]) {
                    data[selectedRoute].forEach(stop => {
                        let option = document.createElement("option");
                        option.value = stop;
                        option.textContent = stop;
                        stopDropdown.appendChild(option);
                    });
                }
            });
        })
        .catch(error => console.error("Error loading bus routes:", error));
});
