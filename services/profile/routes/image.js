const qrcode = require('qrcode');

const {
    findHackerByURL
} = require('../util/hacker.js');

module.exports = async function (req, res) {
    const url = req.params.url;

    let hacker = await findHackerByURL(url);

    if (hacker === null) {
        res.sendStatus(404);

    }
    else {
        try {
            qrcode.toFileStream(res, hacker.hexCode);
        }
        catch (err) {
            console.log(err);
            res.sendStatus(500);
        }
    }

}
