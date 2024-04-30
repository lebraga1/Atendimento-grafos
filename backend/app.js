const express = require('express'); 
const path = require('path');
const axios = require("axios");
const bodyParser = require("body-parser");

const app = express(); 
const PORT = 3000; // Porta que o servidor vai rodar

app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true })); 
app.use(express.static(path.join(__dirname, 'public')));

app.get("/", (req, res) => { res.sendFile(__dirname + "/public/index.html") });

app.post('/map', (req, res) => { 
    let latitude = req.body.lat;
    let longitude = req.body.long;
    // let latitude = -22.007173843864205;
    // let longitude =  -47.893433403607524;
    axios.post("http://localhost:8000/drawMap",
{lat: latitude, long: longitude})
.then((response) => {
    res.set("Content-Type", "text/html");
    res.send(response.data)
}).catch(error => console.log(error))
    
})
  
app.listen(PORT, (error) =>{ 
    if(!error) 
        console.log("Server is Successfully Running, and App is listening on port "+ PORT);
    else
        console.log("Error occurred, server can't start", error); 
    }
);