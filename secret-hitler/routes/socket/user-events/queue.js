const Queue = require('../../../models/queue');
/**
 * @param {object} socket - user socket reference.
 * @param {object} passport - socket authentication.
 * @param {object} data - from socket emit.
 */
module.exports.handleAddToQueue = async (socket, passport, data) => {
    try {
        const newUserInQueue = new Queue({
            userName: passport.user
        });
        await newUserInQueue.save();
        
        await socket.emit("userIsAddedToQueue", {status: true})
    } catch (error) {
        await socket.emit("userIsAddedToQueue", {status: false, message: error})
    }

}