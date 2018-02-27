const Device = require('../models/device');

const registerDevice = async function (deviceID, platform) {

    try {
        // Check if this device ID is unique, error if not
        let device = await Device.findOne({ deviceID });
        if (device != null) return false;

        // Create and save the new device
        device = new Device({ deviceID, platform });
        device.save();
        return true;

    }
    catch (err) {
        console.error(err);
        return false;
    }

};

const getDevicesByPlatform = async function (platform) {

    try {
        let devices = await Device.find({ platform });
        return devices.map(device => device.deviceID);
    }
    catch (err) {
        console.error(err);
        return [];
    }

};

module.exports = {
    registerDevice,
    getDevicesByPlatform
};
