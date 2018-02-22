const mongoose = require('mongoose');
const deviceSchema = new mongoose.Schema({
    deviceID: { type: String },
    platform: { type: Number },
});

deviceSchema.index({ deviceID: 1 }, { unique: 1 });

module.exports = mongoose.model('Device', deviceSchema);
