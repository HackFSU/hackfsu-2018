const request = require('request');

const { getDevicesByPlatform } = require('../util/device');

const platform = {
    ios: 1,
    android: 2
};

const generatePayload = async function (title, message) {

    return {
        notifications: [
            {
                tokens: await getDevicesByPlatform(platform.android),
                platform: platform.android,
                message: message,
                title: title
            },
            {
                tokens: await getDevicesByPlatform(platform.ios),
                platform: platform.ios,
                message: message,
                'alert': {
                    'title': title,
                    'body': message,
                }
            }
        ]
    };
};

module.exports = async function (req, res) {
    let title = req.body.title,
        message = req.body.message;
    let payload = await generatePayload(title, message);
    let gorush = process.env.GORUSH_HOST;

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
