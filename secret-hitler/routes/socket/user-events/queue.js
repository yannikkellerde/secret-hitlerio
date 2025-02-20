const Queue = require('../../../models/queue');
/**
 * @param {object} socket - user socket reference.
 * @param {object} passport - socket authentication.
 * @param {object} data - from socket emit.
 */
const handleAddToQueue = async (socket, passport, data) => {
    try {
        const isUserInTheQueue = await Queue.find({userName: passport.user})
        if (isUserInTheQueue.length>0) return 

        const newUserInQueue = new Queue({
            userName: passport.user
        });
        await newUserInQueue.save();
        
        await socket.emit("userStatusInQueue", {status: true, action: "added"})
        await getQueue(socket, passport, data)

    } catch (error) {
        await socket.emit("userIsAddedToQueue", {status: false, message: error})
    }

}

const handleRemoveFromQueue = async (socket, passport, data) => {
    try {
        const isUserInTheQueue = await Queue.find({userName: passport.user})
        if (isUserInTheQueue.length==0) return 

        const result  = await Queue.deleteMany({userName: passport.user})

        await socket.emit("userStatusInQueue", {status: true, action: "removed"})
        await getQueue(socket, passport, data)

    } catch (error) {
        await socket.emit("userIsRemovedFromQueue", {status: false, message: error})
    }

}

const getQueue = async (socket, passport, data) => {
    try {
        const userInQueue = await Queue.find({})
                
        await socket.emit("setQueue", {status: true, queue: userInQueue})
    } catch (error) {
        await socket.emit("setQueue", {status: false, message: error})
    }

}

module.exports = {
    handleAddToQueue,
    getQueue,
    handleRemoveFromQueue
};
