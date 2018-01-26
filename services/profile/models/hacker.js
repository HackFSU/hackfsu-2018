const mongoose = require('mongoose');

const hackerSchema = new mongoose.Schema({
    hackerID: { type: String },
    hexCode: { type: String },
    qrURL: { type: String }
});

hackerSchema.index({ hackerID: 1 }, { unique: 1 });
const Hacker = mongoose.model('Hacker', hackerSchema);

module.exports = Hacker;
