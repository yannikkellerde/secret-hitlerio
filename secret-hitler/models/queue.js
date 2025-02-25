const mongoose = require('mongoose');
const { Schema } = mongoose;
const Queue = new Schema({
    uid: String,
    userName: String,
    socketId: String,
    gameId: String | null
});

module.exports = mongoose.model('Queue', Queue);
