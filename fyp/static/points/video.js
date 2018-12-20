window.onload = function() {

	// Video
	var video = document.getElementById("video");
	video.currentTime = 999999999;
	console.log("video duration =" +video.duration)
	// var onloadplay = true;
	// video.play()
	// video.currentTime = 0;
	// Buttons
	var playButton = document.getElementById("play-pause");
	var muteButton = document.getElementById("mute");
	var fullScreenButton = document.getElementById("full-screen");

	// Sliders
	var seekBar = document.getElementById("seek-bar");
	//seekBar.value=500;
	//seekBar.value=0;
	// seekBar.
	var volumeBar = document.getElementById("volume-bar");


	// Event listener for the play/pause button
	playButton.addEventListener("click", function() {
		if (video.paused == true) {

			// Play the video
			video.play();
			startPlay= true;
			
			
			percentageTime = (seekBar.value / 100);
			console.log("percentage time = " +percentageTime)
			console.log("video current time= " +video.currentTime)
			if (video.currentTime == 0){percentageTime=0}
			play();
			// Update the button icon
			playButton.innerHTML = "<i class=\"fa fa-pause fa-fw\"></i>";
		} else {
			// Pause the video
			video.pause();
			startPlay= false;
			//percentageTime = (seekBar.value / 100);
			pause();
			
			// Update the button icon
			playButton.innerHTML = "<i class=\"fa fa-play fa-fw\"></i>";
		}
	});


	// Event listener for the mute button
	muteButton.addEventListener("click", function() {
		if (video.muted == false) {
			// Mute the video
			video.muted = true;

			// Update the button icon
			muteButton.innerHTML = "<i class=\"fa fa-volume-mute fa-fw\"></i>";
		} else {
			// Unmute the video
			video.muted = false;

			// Update the button icon
			muteButton.innerHTML = "<i class=\"fa fa-volume-up fa-fw\"></i>";
		}
	});


	// Event listener for the full-screen button
	fullScreenButton.addEventListener("click", function() {
		if (video.requestFullscreen) {
			video.requestFullscreen();
		} else if (video.mozRequestFullScreen) {
			video.mozRequestFullScreen(); // Firefox
		} else if (video.webkitRequestFullscreen) {
			video.webkitRequestFullscreen(); // Chrome and Safari
		}
	});

	
	// Event listener for the seek bar
	seekBar.addEventListener("change", function() {
		// Calculate the new time
		var time = video.duration * (seekBar.value / 100);
		percentageTime = (seekBar.value / 100);
		// Update the video time
		video.currentTime = time;
	});

	
	// Update the seek bar as the video plays
	video.addEventListener("timeupdate", function() {
		// Calculate the slider value
		var value = (100 / video.duration) * video.currentTime;
		//percentageTime = (seekBar.value / 100);
		// Update the slider value
		seekBar.value = value;
	});

	// Pause the video when the seek handle is being dragged
	seekBar.addEventListener("mousedown", function() {
		video.pause();
		startPlay= false;
		pause();
	});

	// Play the video when the seek handle is dropped
	seekBar.addEventListener("mouseup", function() {
		if (playButton.innerHTML == "Play") {
		percentageTime = (seekBar.value / 100);
		play();
		pause();
		}else if(playButton.innerHTML == "Pause"){
		video.play();
		console.log("seek is dropped");
		startPlay= true;
		percentageTime = (seekBar.value / 100);
		play();
		//video.paused=false;
		}
		
	});

	// Event listener for the volume bar
	volumeBar.addEventListener("change", function() {
		// Update the video volume
		video.volume = volumeBar.value;
	});

	// document.getElementById("play-pause").click();
	// document.getElementById("play-pause").click();
	//document.getElementById("play-pause").click();
}