var end = 0 
var refresh = 1000; 

console.log(' file ordertime.js has been loaded....')

function displayTime(start) {
	window.start = parseFloat(start);

	if (window.start >= end) {
		mytime = setTimeout('calculateDiff()', refresh)
	}
	else {
		console.log("inside else, time is over");
		console.log(document.getElementById('showtime'));
		document.getElementById('showtime').innerHTML = "Remaining Time : Order is ready to Serve";
	}
}

function calculateDiff() {
	var minutes = Math.floor((window.start) / 60);


	var secs = Math.floor((window.start - (minutes * 60)));

	if (minutes > 0) {
		var timeleft = "Remaining Time : " + minutes + " Minutes and " + secs + " Secondes " ;
	}
	else {
		var timeleft = "Remaining Time : " + secs + " Secondes " ;
	}
	
	document.getElementById('showtime').innerHTML = timeleft;

	window.start = window.start - 1;

	dt = displayTime(window.start);
}