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
ws.onopen = function () {
    const msg = createMessage(0, "setName", "Puck");
    ws.send(msg);
};

let firstClickDone = false

let lastAdvertising = {};

function onDeviceChanged(address, data) {
    ws.send(createMessage(4, "remote", "clicked"));
}

function onDiscovery(peripheral) {

    name = peripheral.advertisement.localName

    if (name !== undefined && name.includes("Puck.js 170f")) {

        let data = peripheral.advertisement.manufacturerData.slice(2);

        if (JSON.stringify(lastAdvertising[peripheral.address]) !== JSON.stringify(data)) {
            if (!firstClickDone) {
                firstClickDone = true
            } else {
                onDeviceChanged(peripheral.address, data)
            }

        }

        lastAdvertising[peripheral.address] = data;

    }

}

noble.on('stateChange', function (state) {
    if (state !== "poweredOn") {
        return
    }
    noble.startScanning([], true)
});

noble.on('discover', onDiscovery);
