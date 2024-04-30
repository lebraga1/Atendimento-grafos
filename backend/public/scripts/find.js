let buttonEl = document.querySelector("#calcula");
let toastEl = document.querySelector('#toast-default');
let closeEl = document.querySelector('#close');



let getLocationPromise = new Promise((resolve, reject) => { // Pega a localização do usuário
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {

            latitude = position.coords.latitude;
            longitude = position.coords.longitude;

            resolve({
                lat: latitude,
                long: longitude
            })
        }, () => {}, {enableHighAccuracy: true})

    } else {
        reject("your browser doesn't support geolocation API");
    }
})

async function calcProximity() { // Envia a localização do usuário para o backend e recebe o mapa
    let coords = {}
    let location = await getLocationPromise; // Pega a localização do usuário
    coords = location; // Adiciona a localização do usuário ao objeto coords
    fetch('http://localhost:3000/map', { 
        method: "POST", 
        headers: { 
            "Content-Type": "application/json"
        },
        body: JSON.stringify(coords)
    }
    ).then(response => { // Recebe o mapa
        return response.text();
    })
    .then(html => { // Cria um link para download do mapa
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        console.log(doc);
        let linkEL = document.createElement('a');
        linkEL.setAttribute('href', 'data:text/html;charset=utf-8,' + encodeURIComponent(html));
        linkEL.setAttribute('download', 'mapa.html');
        linkEL.style.display = 'none';
        document.body.appendChild(linkEL);
        linkEL.click();
        document.body.removeChild(linkEL);

    })
    .catch(error => { 
        console.error(error);
    })
    toastEl.classList.remove('opacity-0');
    toastEl.classList.remove('pointer-events-none');
    
}

buttonEl.addEventListener('click', calcProximity);
closeEl.addEventListener('click', e => {
    toastEl.classList.add('opacity-0');
    toastEl.classList.add('pointer-events-none');
})

