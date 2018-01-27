const {
    createHacker,
    findHackerById
} = require('../util/hacker.js');

module.exports = async function (req, res) {
    const id = req.params.hackerID;

    // Ideally, this function is only being called to generate
    //a hexcode and QR url for a hacker. But to play it safe,
    // we're going to try and see if they exist first.

    let hacker = await findHackerById(id);

    //  If hacker is null, we try generating a hacker but possibly
    //  fail. 201 for creation, 500 for failure. Otherwise, we already
    //  found the hacker and we return it with 200 success.

    if (hacker === null) {
        try {
            hacker = await createHacker(id);
            res.status(201).json({
                code: hacker.hexCode,
                path: hacker.qrURL
            });
        }
        catch (err) {
            console.log(err);
            res.sendStatus(500);
        }
    }
    else {
        res.status(200).json({
            code: hacker.hexCode,
            path: hacker.qrURL
        });
    }
};
