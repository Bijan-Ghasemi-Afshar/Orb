import 'bootstrap';
import 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import './home.css';



// Set content height
function setContHeight(){

	var windowHeight = $(window).height();
	$("#content-area").height(windowHeight);	

}


// User input submission handling
function userInputSub(){

	$("#send-input").on('click', function(){

		var userInput = $("#user-input").val();		
		$("#user-input").val("");
		saveUserChat(userInput);
		sendRequest(userInput);
		$(".chat-area").animate({ scrollTop: $(".chat-area")[0].scrollHeight }, "slow");

	});


	$("#send-voice-input").on('click', function(){

		sendUserSpeech()
		$(".chat-area").animate({ scrollTop: $(".chat-area")[0].scrollHeight }, "slow");

	});

}

function sendUserSpeech(){
	$.ajax({
		url: '/speechInput',
		type: 'GET',
		dataType: 'text',
	})
	.done(function(data) {		
		saveUserChat(data)
		getChatSpeechResponse(data)
	})
	.fail(function() {
		console.log("error");
	});
}

function getChatSpeechResponse(data){
	$.ajax({
		url: '/speechResponse',
		type: 'GET',
		dataType: 'text',
		data: {"user_input": data},
	})
	.done(function(data) {
		saveBotChat(data);
		$(".chat-area").animate({ scrollTop: $(".chat-area")[0].scrollHeight }, "slow");
		sendSpeechRequest(data)
	})
	.fail(function() {
		console.log("error");
	});
}

// Send AJAX request to process chat
function sendRequest(userInput){

	$.ajax({
		url: '/process',
		type: 'GET',
		dataType: 'text',
		data: {"user_input": userInput},
	})
	.done(function(data) {		
		saveBotChat(data);
		$(".chat-area").animate({ scrollTop: $(".chat-area")[0].scrollHeight }, "slow");
		sendSpeechRequest(data)
	})
	.fail(function() {
		console.log("error");
	});
	

}

// Send AJAX request to speek results
function sendSpeechRequest(data){
	$.ajax({
		url: '/speek',
		type: 'GET',
		dataType: 'text',
		data: {"user_input": data},
	})
	.done(function(data) {
	})
	.fail(function() {
		console.log("error");
	});
}

// Put user input into the chat area
function saveUserChat(input){

	$(".chat-area").append(`<div class="chat-text-container"><div class="user-chat bg-info text-white">${input}</div></div><br/>`)

}

// Put bot response into the chat area
function saveBotChat(input){
	input = input.replace(/\n/g, "<br />");
	$(".chat-area").append(`<div class="chat-text-container"><div class="bot-chat bg-warning">${input}</div></div><br/>`)

}


// Main function
function run(){

	setContHeight();

	userInputSub();

}


$(document).ready(run());