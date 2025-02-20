const Queue = require('../../../models/queue');
const {handleAddNewGame} = require('../user-events');

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

        await checkIfThereAreSevenPlayers(socket, passport)
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

const checkIfThereAreSevenPlayers = async (socket, passport) => {
    console.log("inside checkIfThereAreSevenPlayers")
    const userInQueue = await Queue.find({})
    if (userInQueue.length>=7){
        console.log('checkIfThereAreSevenPlayers : there are 7 players we can start a new game.')
        await startANewGame(socket, passport)
    }
}

const startANewGame = async (socket, passport) =>{
    console.log("inside startANewGame")

    // select 7 players
    const sevenPlayers = await Queue.find({}).limit(7)
    // delete players from queue
    for (let player of sevenPlayers){
        await Queue.deleteMany({userName: player.userName})
    }
    // create a new game 
    const gameDefaultSetup = {
        gameName: `defaultsetup-${Date.now()}`,
        gameType: 'ranked',
        flag: 'none',
        minPlayersCount: 7,
        excludedPlayerCount: [ 5, 6, 8, 9, 10 ],
        maxPlayersCount: 7,
        experiencedMode: true,
        playerChats: 'enabled',
        disableObserverLobby: false,
        disableObserver: false,
        isTourny: false,
        isVerifiedOnly: false,
        disableGamechat: false,
        blindMode: false,
        flappyMode: false,
        flappyOnlyMode: false,
        timedMode: false,
        rebalance6p: false,
        rebalance7p: false,
        rebalance9p2f: false,
        eloSliderValue: null,
        xpSliderValue: null,
        unlistedGame: false,
        privatePassword: false,
        privateAnonymousRemakes: false,
        noTopdecking: 0,
        allowBots: true
    }
    
    await handleAddNewGame(socket, passport, gameDefaultSetup)
    // assign players to the game

    // transfer players to the game
}

module.exports = {
    handleAddToQueue,
    getQueue,
    handleRemoveFromQueue
};
