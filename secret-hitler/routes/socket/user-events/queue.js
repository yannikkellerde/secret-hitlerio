const Queue = require('../../../models/queue');
const Game = require('../../../models/game');
const {handleAddNewGame} = require('../user-events/create-game');

/**
 * @param {object} socket - user socket reference.
 * @param {object} passport - socket authentication.
 * @param {object} data - from socket emit.
 */
const handleAddToQueue = async (socket, passport, data, io) => {
    try {
        const isUserInTheQueue = await Queue.find({userName: passport.user})
        if (isUserInTheQueue.length>0) return 

        const newUserInQueue = new Queue({
            userName: passport.user,
            socketId: socket.id,
            gameId: null
        });
        await newUserInQueue.save();
        
        await socket.emit("userStatusInQueue", {status: true, action: "added"})
        await getQueue(socket, passport, data)

        await checkIfThereAreSevenPlayers(socket, passport, io)
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

const checkIfThereAreSevenPlayers = async (socket, passport, io) => {
    const userInQueue = await Queue.find({gmaeId: null})
    if (userInQueue.length>=7){
        // console.log('checkIfThereAreSevenPlayers : there are 7 players we can start a new game.')
        // this socket and passport is for the latest user joint (socket, passport)
        await startANewGame(socket, passport, io)
    }
}

const startANewGame = async (socket, passport, io) =>{    
    const gameNameId = `game_${Date.now()}`;

    // select 7 players
    const sevenPlayers = await Queue.find({gameId: null}).limit(7)
    
    // create a new game 
    var gameDefaultSetup = {
        gameName: gameNameId,
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
    
    const game_uid = await handleAddNewGame(socket, passport, gameDefaultSetup)

    // delete players from queue
    for (let player of sevenPlayers){
        if ( player.userName == passport.user ) {
            await Queue.deleteMany({userName: player.userName})

        }else{
            player.gameId = game_uid
            await player.save()
        }
    }
}
const isGameIdSet = async (socket, passport, data)=>{    
    const userDocument = await Queue.find({userName: passport.user})
    if (userDocument.length > 0){
        if ( userDocument[0].gameId ){
            await socket.emit("goToGame", {status: true, gameId: userDocument[0].gameId})
            await Queue.deleteMany({userName: userDocument[0].userName})
        }
    }
}

module.exports = {
    handleAddToQueue,
    getQueue,
    handleRemoveFromQueue,
    isGameIdSet
};
