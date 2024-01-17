const noble = require('@abandonware/noble');
const WebSocket = require('ws');
// 6e400001b5a3f393e0a9e50e24dcca9e

let messageId = 0;

function createMessage(stepId, action, message) {
    messageId += 1;
    const timestamp = Date.now();

    const messageToSend = {
        step_id: stepId,
        id: messageId,
        timestamp: timestamp,
        action: action,
        message: message
    };
    return JSON.stringify(messageToSend);
}

const ws = new WebSocket("ws://172.20.10.14:8080");
ws.onopen = function() {
    const msg = createMessage(0, "setName", "Puck");
    ws.send(msg);
};

const devices = [
    "c7:f8:6b:2d:52:46", "c1:68:14:e8:fb:35", "c3:26:d7:38:30:25", "d9:0e:5e:8a:76:f6", "ed:0d:64:c9:a2:e5", "ef:2d:7d:bc:69:02", "e4:8d:e2:32:6a:7e", "d3:a2:fb:dc:17:0f"
];

const tabDevices = {
    "c7:f8:6b:2d:52:46": "a", // 5246
    "c1:68:14:e8:fb:35": "n", // FB35
    "c3:26:d7:38:30:25": "c", // 3025
    "d9:0e:5e:8a:76:f6": "r", // 76F6
    "ed:0d:64:c9:a2:e5": "e", // A2E5
    "ef:2d:7d:bc:69:02": "i", // 6902
    "e4:8d:e2:32:6a:7e": "l", // 6A7E
    "d3:a2:fb:dc:17:0f": "t" // 170F
}

let lastAdvertising = {};

function onDeviceChanged(address, data) {
    ws.send(createMessage(4, "remote", "clicked"));
}

function onDiscovery(peripheral) {

    name = peripheral.advertisement.localName

    if (name !== undefined) {

        if (name.includes("Puck")) {

            let data = peripheral.advertisement.manufacturerData.slice(2);
            console.log(data);
            onDeviceChanged(peripheral.address, data)
            lastAdvertising[peripheral.address] = data;

        }

    }

}

noble.on('stateChange', function (state) {
    if (state !== "poweredOn"){
        return
    }
    console.log("Starting scan...");
    noble.startScanning([], true)
});

noble.on('discover', onDiscovery);

noble.on('scanStart', function () {
    console.log("Scanning started.");
});

noble.on('scanStop', function () {
    console.log("Scanning stopped.");
});