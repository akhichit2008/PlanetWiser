const errorLabel = document.querySelector("label[for='error-msg']");
const latInp = document.querySelector("#latitude");
const lonInp = document.querySelector("#longitude");
const airQuality = document.querySelector(".air-quality");
const airQualityStat = document.querySelector(".air-quality-status");
const srchBtn = document.querySelector(".search-btn");
const componentsEle = document.querySelectorAll(".component-val");
const ctx = document.getElementById('pollutantChart').getContext('2d');
let chart;
let map;

// Modal script
const modal = document.getElementById("modal");
const closeBtn = document.querySelector(".close-btn");

// Show modal
window.onload = () => {
    modal.style.display = "block";
    startIntro(); 
};

// Close modal
closeBtn.onclick = () => {
    modal.style.display = "none";
};


window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// Initialize Intro.js
function startIntro() {
    const intro = introJs();
    intro.setOptions({
        steps: [
            {
                intro: "Welcome to the Air Pollution Indicator app! Let's take a quick tour."
            },
            {
                element: document.querySelector(".location-container"),
                intro: "Enter your location here to get the air quality index.",
                position: 'bottom'
            },
            {
                element: document.querySelector(".air-info"),
                intro: "Here you will see the air quality index and concentration of different pollutants.",
                position: 'top'
            },
            {
                element: document.querySelector("footer"),
                intro: "Remember, planting more trees helps in reducing air pollution!",
                position: 'top'
            },
            {
                element: document.getElementById("pollutantChart"),
                intro: "The chart below visualizes the concentration of various pollutants in a bar chart.",
                position: 'top'
            }
        ],
        showProgress: true,
        showBullets: false,
        showStepNumbers: true,
        exitOnOverlayClick: false
    });
    intro.start();
}

// Request location access and get user coordinates
const getUserLocation = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onPositionGathered, onPositionGatherError);
    } else {
        onPositionGatherError({ message: "Can't Access your location. Please enter your co-ordinates" });
    }
};

// Handle position data
const onPositionGathered = (pos) => {
    let lat = pos.coords.latitude.toFixed(4);
    let lon = pos.coords.longitude.toFixed(4);

    latInp.value = lat;
    lonInp.value = lon;

    // Initialize and display the map with user's location
    initializeMap(lat, lon);

    // Get data from API
    getAirPollution(lat, lon);
};

// Initialize and display the map
const initializeMap = (lat, lon) => {
    if (map) {
        map.remove(); // Remove the existing map instance if it exists
    }
    
    map = L.map('map').setView([lat, lon], 13); // Center the map on the coordinates

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([lat, lon]).addTo(map)
        .bindPopup('You are here!')
        .openPopup();
};

// Validate coordinates
const isValidCoord = (lat, lon) => {
    return lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180;
};

// Fetch air pollution data
const getAirPollution = async (lat, lon) => {
    const res = await fetch(`https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=10d3cd4d30e5866b837fe22bc832a605`);
    return await res.json();
};

// Set air components and create chart
const setComponentsOfAir = (airData) => {
    let components = {...airData.list[0].components};
    componentsEle.forEach(ele => {
        const attr = ele.getAttribute('data-comp');
        ele.innerText = components[attr] + " μg/m³";
    });
    createChart(components); 
};

// Create chart with pollutant data
const createChart = (components) => {
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(components),
            datasets: [{
                label: 'Pollutant Concentration (μg/m³)',
                data: Object.values(components),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            return `${context.label}: ${context.raw} μg/m³`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => {
                            return `${value} μg/m³`;
                        }
                    }
                }
            }
        }
    });
};

// Handle position gather error
const onPositionGatherError = (e) => {
    errorLabel.innerText = e.message;
};

// Search button event listener
srchBtn.addEventListener("click", () => {
    errorLabel.innerText = "";

    const lat = parseFloat(latInp.value);
    const lon = parseFloat(lonInp.value);

    if (!isValidCoord(lat, lon)) {
        errorLabel.innerText = "Invalid coordinates.";
        return;
    }

    // Initialize and display the map with the provided coordinates
    initializeMap(lat, lon);

    getAirPollution(lat, lon).then(res => {
        airQuality.innerText = res.list[0].main.aqi;
        airQualityStat.innerText = ["Good", "Fair", "Moderate", "Poor", "Very Poor"][res.list[0].main.aqi - 1];
        setComponentsOfAir(res);
    }).catch(err => {
        console.error(err);
        errorLabel.innerText = "Unable to fetch data.";
    });
});

// Automatically request location access on page load
window.onload = () => {
    getUserLocation();
    startIntro(); // Start Intro.js tour on page load
};

alert(Welcome)