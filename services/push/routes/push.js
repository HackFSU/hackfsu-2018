const request = require('request');

const { getDevicesByPlatform } = require('../util/device');

const platform = {
    ios: 1,
    android: 2
};

const generatePayload = async function (title, message) {

    let androidTokens = await getDevicesByPlatform(platform.android);
    return {
        notifications: [
            {
                tokens: androidTokens,
                platform: platform.android,
                message: message,
                title: title
            },
            // {
            //     tokens: await getDevicesByPlatform(platform.ios),
            //     platform: platform.ios,
            //     message: message
            // }
        ]
    };
};

module.exports = async function (req, res) {
    let title = req.body.title,
        message = req.body.message;
    let payload = await generatePayload(title, message);
    let gorush = process.env.GORUSH_HOST;

    console.log(req.body);
    console.log(title, message);
    console.log(payload);

    request.post(`${gorush}/api/push`,
        { json: payload },
        (err, resp, body) => {
            if (err) {
                console.error(err);
                res.sendStatus(500);
            }
            else res.sendStatus(resp.statusCode);
        });

};
