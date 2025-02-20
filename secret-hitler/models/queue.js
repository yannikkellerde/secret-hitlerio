const mongoose = require('mongoose');
const { Schema } = mongoose;
const Queue = new Schema({
    uid: String,
    userName: String,
});

module.exports = mongoose.model('Queue', Queue);
