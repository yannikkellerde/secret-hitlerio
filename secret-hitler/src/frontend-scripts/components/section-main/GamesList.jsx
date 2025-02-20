import React, { useEffect, useState } from 'react'; // eslint-disable-line
import DisplayLobbies from './DisplayLobbies.jsx';
import PropTypes from 'prop-types';
import { Checkbox } from 'semantic-ui-react';
import moment from 'moment';
import { CURRENTSEASONNUMBER } from '../../constants';
import { Message } from 'semantic-ui-react';
import { processEmotes } from '../../emotes';

const GamesList = (props)=> {
	const state = {
		filtersVisible: false
	};

	const toggleFilter = value => {
		const { gameFilter, changeGameFilter } = props;

		gameFilter[value] = !gameFilter[value];
		changeGameFilter(gameFilter);
	};

	const toggleNotify = () => {
		const { notify, socket } = props;
		socket.emit('updateGameSettings', {
			notifyForNewLobby: !notify
		});
	};

	const renderSticky = () => {
		if (props.stickyEnabled && props.generalChats && props.generalChats.sticky) {
			return (
				<Message
					onDismiss={() => {
						props.setStickyEnabled(false);
					}}
					color="blue"
				>
					{processEmotes(props.generalChats.sticky, true, props.allEmotes)}
				</Message>
			);
		}
	};

	const renderFilters = () => {
		const { gameFilter, notify } = props;

		return (
			<div className="browser-filters ui grid">
				<div className="one wide column">
					<h4 className="ui header">Public</h4>
					<Checkbox
						toggle
						checked={!gameFilter.pub}
						onChange={() => {
							toggleFilter('pub');
						}}
					/>
				</div>
				<div className="one wide column">
					<h4 className="ui header">Private</h4>
					<Checkbox
						toggle
						checked={!gameFilter.priv}
						onChange={() => {
							toggleFilter('priv');
						}}
					/>
				</div>
				<div className="one wide column">
					<h4 className="ui header">Unstarted</h4>
					<Checkbox
						toggle
						checked={!gameFilter.unstarted}
						onChange={() => {
							toggleFilter('unstarted');
						}}
					/>
				</div>
				<div className="one wide column">
					<h4 className="ui header">Progress</h4>
					<Checkbox
						toggle
						checked={!gameFilter.inprogress}
						onChange={() => {
							toggleFilter('inprogress');
						}}
					/>
				</div>
				<div className="one wide column">
					<h4 className="ui header">Completed</h4>
					<Checkbox
						toggle
						checked={!gameFilter.completed}
						onChange={() => {
							toggleFilter('completed');
						}}
					/>
				</div>
				<div className="one wide column">
					<i title="Filter by casual games" className="handshake icon" />
					<Checkbox
						toggle
						checked={!gameFilter.casualgame}
						onChange={() => {
							toggleFilter('casualgame');
						}}
					/>
				</div>
				<div className="one wide column">
					<i title="Filter by custom games" className="setting icon" />
					<Checkbox
						toggle
						checked={!gameFilter.customgame}
						onChange={() => {
							toggleFilter('customgame');
						}}
					/>
				</div>
				<div className="one wide column">
					<i title="Filter by timed mode games" className="hourglass half icon" />
					<Checkbox
						toggle
						checked={!gameFilter.timedMode}
						onChange={() => {
							toggleFilter('timedMode');
						}}
					/>
				</div>
				<div className="one wide column iconcolumn">
					<i title="Filter by standard games" className="standard-icon" />
					<Checkbox
						toggle
						checked={!gameFilter.standard}
						onChange={() => {
							toggleFilter('standard');
						}}
					/>
				</div>
				<div className="one wide column iconcolumn">
					<i title="Filter by experienced-player-only games" className="rainbow-icon" />
					<Checkbox
						toggle
						checked={!gameFilter.rainbow}
						onChange={() => {
							toggleFilter('rainbow');
						}}
					/>
				</div>
				<div className="one wide column">
					<i title="Get notified when new games are available" className="alarm half icon" />
					<Checkbox
						toggle
						checked={notify}
						onChange={() => {
							toggleNotify();
						}}
					/>
				</div>
			</div>
		);
	}

	const [queue, setQueue] = useState([])

	useEffect(()=>{
		props.socket.emit('getQueue', {dummy: "dummy"});

		props.socket.on("userIsAddedToQueue", (data)=>{
			console.log("user is added to queue", data)
		})

		props.socket.on("setQueue", (data)=>{
			console.log("queue is updated from backend", data)
			if( data.status == true){
				setQueue(data.queue)
			}else{
				alert("Error in updating queue")
				console.log(data)
			}
		})
	}, [])

	const addToQueue = () =>{
		console.log("inside add to queue")
		// console.log("props ", props)
		props.socket.emit('addToQueue', {dummy: "dummy"});
	}

	return (
		<section className={state.filtersVisible ? 'browser-container' : 'browser-container filters-hidden'}>
			<a href="#/changelog">
				<h5 title="A season is an optional new tier of elo that is reset every 3 months.">
					{new Date() > new Date('2023-04-23')
						? `Season ends ${moment(new Date('2024-01-05T06:00:00.000Z')).fromNow()}.`
						: `Welcome to season ${CURRENTSEASONNUMBER}!`}
				</h5>
			</a>
			<h3>Game filters</h3>
			{renderFilters()}
			<div className="browser-header">
				{(() => {
					const { userName } = props.userInfo;
					const gameBeingCreated = props.midSection === 'createGame';

					return userName && !gameBeingCreated ? (
						// <a className="fluid ui button primary create-game-button" href="#/creategame">
						// 	Create a new game
						// </a>
						<button className="fluid ui button primary create-game-button" onClick={addToQueue}>
							Add to queue
						</button>
					) : (
						<span className="disabled-create-game-button">
							<button className="fluid ui button primary disabled">{gameBeingCreated ? 'Creating a new game..' : 'Log in to join games'}</button>
						</span>
					);
				})()}
			</div>
			
			<div className="browser-body">
				{renderSticky()}
				<ol>
				{
					queue.map((row)=>{
						return <li key={row['_id']}>{row.userName}</li>
					})
				}
				</ol>
			</div>
		</section>
		
	)
}

GamesList.defaultProps = {
	gameFilter: {},
	userInfo: {},
	gameList: []
};

GamesList.propTypes = {
	userInfo: PropTypes.object,
	midSection: PropTypes.string,
	gameList: PropTypes.array,
	socket: PropTypes.object,
	userList: PropTypes.object,
	gameFilter: PropTypes.object,
	changeGameFilter: PropTypes.func,
	generalChats: PropTypes.object,
	allEmotes: PropTypes.object
};

export default GamesList;
