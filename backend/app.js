const express = require('express'); 
const path = require('path');
const axios = require("axios");
const bodyParser = require("body-parser");

const app = express(); 
const PORT = 3000; 

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.get("/", (req, res) => { res.sendFile(__dirname + "/public/index.html") });

app.post('/map', (req, res) => {
    console.log(req.body)
    let lat = req.body.lat;
    let long = req.body.long;
    // let response = axios.post()
    res.send(req.body)
})
  
app.listen(PORT, (error) =>{ 
    if(!error) 
        console.log("Server is Successfully Running, and App is listening on port "+ PORT);
    else
        console.log("Error occurred, server can't start", error); 
    }
);