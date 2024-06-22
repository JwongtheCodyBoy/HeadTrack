const express = require('express');
const app = express();
const port = 8080;

app.use( express.json())
let dataStore = [];

// Define a GET endpoint
app.get('/data', (req, res) => {
    res.status(200).json(dataStore);
});


// Define a route for receiving data from Python
app.post('/data', (req, res) => {
    const aimX = req.body['aimX'];
    const aimY = req.body['aimY'];
    console.log(`Received data - X: ${aimX}, Y: ${aimY}`);

    // Store the received data
    dataStore.push({ aimX: aimX, aimY: aimY, timestamp: new Date() });

    res.send(`Data Received (${aimX}, ${aimY})`);
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});