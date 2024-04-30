let buttonEl = document.querySelector("#calcula")

let getLocationPromise = new Promise((resolve, reject) => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {

            latitude = position.coords.latitude
            longitude = position.coords.longitude

            resolve({
                lat: latitude,
                long: longitude
            })
        }, () => {}, {enableHighAccuracy: true})

    } else {
        reject("your browser doesn't support geolocation API")
    }
})

async function calcProximity() {
    let coords = {}
    let location = await getLocationPromise;
    coords = location;
    let response = await fetch('http://localhost:3000/map', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(coords)
    }
    )
}

buttonEl.addEventListener('click', calcProximity);

