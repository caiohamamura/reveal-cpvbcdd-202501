/*****************************************************************
** Author: Asvin Goel, goel@telematique.eu
**
** A plugin for reveal.js adding instant polls within an
** online seminar.
**
** Version: 0.1.1 (patched: per-user vote tracking, allow re-voting)
**
** License: MIT license (see LICENSE.md)
**
******************************************************************/

window.RevealPoll = window.RevealPoll || {
    id: 'RevealPoll',
    init: function(deck) {
        initPoll(deck);
    },
};


const initPoll = function(Reveal){
	var config = Reveal.getConfig().poll;

	var polls = [];

	// Get poll index
	function getPollIndex(id) {
		return polls.findIndex(poll => poll.id === id);
	}

	function initializePolls() {
		var pollElements = document.querySelectorAll(".poll");
		for (var i = 0; i < pollElements.length; i++ ){
			var id = pollElements[i].getAttribute('data-poll')
			var votes = {};
			var buttons = pollElements[i].querySelectorAll("button");
			for (var j = 0; j < buttons.length; j++ ){
				// initialize number of votes for button
				votes[buttons[j].getAttribute('data-value')] = 0;

				// make button clickable
				buttons[j].addEventListener('click', function(evt){
					if ( !RevealSeminar.connected() ) {
						alert("You are currently not connected to the live poll. Your vote is ignored.");
						return;
					}
					const button = evt.target;
					const pollEl = button.parentElement;
					// Clear previous selection — allow re-voting
					var siblings = pollEl.querySelectorAll("button");
					for (var k = 0; k < siblings.length; k++ ){
						siblings[k].classList.remove("selected");
					}
					vote( pollEl.getAttribute('data-poll'), button.getAttribute('data-value') );
					button.classList.add("selected");
					button.blur();
				});
			}
			// userVotes tracks each user's last choice: { userId: 'choice' }
			polls.push( { id, voters: 0, votes, userVotes: {} } );
		}

	}

	function vote( poll, choice ) {
		// send to vote to chair
		var message = new CustomEvent('send');
		message.content = { sender: 'poll-plugin', recipient: true, type: 'vote', poll, choice };
		document.dispatchEvent( message );
	}

	document.addEventListener( 'received', function ( message ) {
		if ( message.content && message.content.sender == 'poll-plugin' ) {
			if ( message.content.type == 'vote' ) {
				const voteData = message.content;
				const poll = polls[getPollIndex(voteData.poll)];
				// Identify user by sender.id from seminar plugin
				const userId = message.sender ? message.sender.id : null;
				if ( !userId || !poll ) return;

				const prevChoice = poll.userVotes[userId];

				if ( prevChoice === voteData.choice ) {
					// Same vote, ignore
					return;
				}

				if ( prevChoice ) {
					// Changing vote: decrement old choice
					poll.votes[prevChoice]--;
				} else {
					// New voter
					poll.voters++;
				}

				// Store this user's choice
				poll.userVotes[userId] = voteData.choice;

				// Increment new choice
				poll.votes[voteData.choice]++;

				var broadcastVoters = new CustomEvent('broadcast');
				broadcastVoters.content = { sender: 'poll-plugin', copy: true, type: 'voters', poll: poll.id, voters: poll.voters };
				document.dispatchEvent( broadcastVoters );

				var broadcastResults = new CustomEvent('broadcast');
				broadcastResults.content = { sender: 'poll-plugin', copy: true, type: 'results', poll: poll.id, votes: poll.votes };
				document.dispatchEvent( broadcastResults );
			}
			else if ( message.content.type == 'voters' ) {
				var voters = document.querySelectorAll('.voters[data-poll="' + message.content.poll + '"]');
				for (var j = 0; j < voters.length; j++ ){
					voters[j].innerHTML = message.content.voters;
				}

			}
			else if ( message.content.type == 'results' ) {
				// update result elements
				var results = document.querySelectorAll('.results[data-poll="' + message.content.poll + '"]');
				for (var i = 0; i < results.length; i++ ) {
					for (var choice in message.content.votes) {
						var elements = results[i].querySelectorAll('[data-value="' + choice + '"]');
						for (var j = 0; j < elements.length; j++ ) {
							elements[j].innerHTML = message.content.votes[choice];
						}
					}
				}

				// update result charts
				if ( typeof RevealChart !== 'undefined' && RevealChart ) {
					var charts = document.querySelectorAll('canvas[data-chart][data-poll="' + message.content.poll + '"]');
					var data = [];
					for (var choice in message.content.votes) {
						data.push(message.content.votes[choice]);
					}
					for (var i = 0; i < charts.length; i++ ) {
						RevealChart.update( charts[i], 0, data );
					}
				}
			}
		}
	});

	Reveal.addEventListener('ready', function(){
		initializePolls();
	});

	return this;
};
