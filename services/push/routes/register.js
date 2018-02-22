const { registerDevice } = require('../util/device');

module.exports = async function (req, res) {
    let { deviceID, platform } = req.body;
    let success = await registerDevice(deviceID, platform);

    if (success) res.sendStatus(201);
    else res.sendStatus(500);
};
