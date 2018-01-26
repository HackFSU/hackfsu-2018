const randomize = require('randomatic');
const Hacker    = require('../models/hacker');

// Function to create and save a new Hacker w/ code.
const createHacker = async (id) => {
    // Create new hacker record for new id
    let url, code, results, unique = false;
    let counter = 0;

    // Generate a unique 6-character hex code for the hacker.
    // Makes 100 attempts to generate a unique code before failing.
    while (!unique) {
        code = randomize('?0', 6, {chars: 'abcdef'});
        results = await Hacker.find({ hexCode: code }).catch(console.log);
        if (results.length === 0) unique = true;
        else counter += 1;

        // Allow 20 tries
        if (counter > 100) {
            return null;
        }
    }

    // Generate unique 32-character url for hacker image.
    unique = false;
    while (!unique) {
        url = randomize('aA0', 32) + '.png';
        results = await Hacker.find({ qrURL: url }).catch(console.log);
        if (results.length === 0) unique = true;
    }

    // Attempt to save a new hacker object into database.
    const hacker = new Hacker({
        hackerID: id,
        hexCode: code,
        qrURL: url
    });
    try {
        hacker.save();
        return hacker;
    } catch (err) {
        console.log(err);
        return null;
    }
};


// Function to find hacker from id (email)
const findHackerById = async (id) => {
    //  Search for the hacker. Potentially 3 results:
    //      1. findOne returns {hacker}
    //      2. findOne returns null.
    //      3. Promise rejection.
    //  We handle it so we either have the {hacker} or we prepare
    //  for the null case.
    let hacker;
    try {
        hacker = await Hacker.findOne({ hackerID: id }).exec();
    }
    catch (err) {
        console.log(err);
        hacker = null;
    }
    return hacker;
};

const findHackerByURL = async (url) => {
    let hacker;
    try {
        hacker = await Hacker.findOne({ qrURL: url }).exec();
    }
    catch (err) {
        console.log(err);
        hacker = null;
    }
    return hacker;
};



module.exports = {
    createHacker,
    findHackerById,
    findHackerByURL
};
