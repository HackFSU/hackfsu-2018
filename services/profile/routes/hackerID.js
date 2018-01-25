const randomize = require('randomatic');
const Hacker    = require('../models/hacker');

// Function to create and save a new Hacker w/ code.
const createHacker = async function (id) {
    // Create new hacker record for new id
    let code, results, unique = false;
    let counter = 0;

    // Generate a unique 6-character hex code for the hacker.
    // Makes 20 attempts to generate a unique code before failing.
    while (!unique) {
        code = randomize('?0', 6, {chars: 'abcdef'});
        results = await Hacker.find({ hexCode: code }).catch(console.log);
        if (results.length === 0) unique = true;
        else counter += 1;

        // Allow 20 tries
        if (counter > 20) {
            return null;
        }
    }

    // Attempt to save a new hacker object into database.
    const hacker = new Hacker({ hackerID: id, hexCode: code });
    try {
        hacker.save();
        return hacker;
    } catch (err) {
        console.log(err);
        return null;
    }
};


module.exports = async function (req, res) {
    const id = req.params.hackerID;
    let hacker;

    //  Search for the hacker. Potentially 3 results:
    //      1. findOne returns {hacker}
    //      2. findOne returns null.
    //      3. Promise rejection.
    //  We handle it so we either have the {hacker} or we prepare
    //  for the null case.
    try {
        hacker = await Hacker.findOne({ hackerID: id }).exec();
    }
    catch (err) {
        console.log(err);
        hacker = null;
    }

    //  If hacker is null, we try generating a hacker but possibly
    //  fail. 201 for creation, 500 for failure. Otherwise, we already
    //  found the hacker and we return it with 200 success.
    if (hacker === null) {
        try {
            hacker = await createHacker(id);
            res.status(201).json({code: hacker.hexCode});
        }
        catch (err) {
            console.log(err);
            res.status(500);
        }
    }
    else {
        res.status(200).json({code: hacker.hexCode});
    }
};
