class TimeCoord {
  constructor(lerpPoint, currentMS) {
		this.lerpPoint = lerpPoint;
		this.currentMS = currentMS;
	}
}

function Particle(deviceID, name, playerNumber, teamId) {
	this.tagID = deviceID;
	this.name = name;
	this.playerNumber = playerNumber;
	this.teamId = teamId;



	this.history = [];//for tail
	this.interpolateFunctionX = new interpolate();
	this.interpolateFunctionY = new interpolate();


	//to update coordinates
	this.update = function (lerpXY, currentMS) {
		//randomised movement
		this.lerpPoint = createVector(lerpXY.x, lerpXY.y);
		//var v = createVector(this.lerpPoint.x,this.lerpPoint.y);
		this.history.push(new TimeCoord(this.lerpPoint, currentMS));
		if ((currentMS - this.history[0].currentMS) > 5000) {
			this.history.splice(0, 1);
		}
	}

	//to show point
	this.show = function () {
		//draw the point
		stroke(0);
		if (this.playerNumber >= 0 && this.playerNumber < 8) {
			fill(0, 0, 255);
		}
		if (this.playerNumber >= 8 && this.playerNumber < 15) {
			fill(102,51,0);
		}

		var mapX = map(this.lerpPoint.x, 0, 7770, 0, $('#defaultCanvas0').width());
		var mapY = map(this.lerpPoint.y, 0, 6000, 0, $('#defaultCanvas0').height());
		ellipse(mapX, mapY, 20, 20);//image
		txt = this.playerNumber;
		console.log(this.playerNumber)
		fill(255);
		text(txt, mapX - textWidth(txt) / 2, mapY + 2);
		console.log("mapX: " + mapX)
		console.log("mapY: " + mapY)

		//loop through history
		noFill();
		beginShape();
		for (var i = 0; i < this.history.length; i++) {
			var pos = this.history[i].lerpPoint;
			var mapHX = map(pos.x, 0, 7770, 0, $('#defaultCanvas0').width());
			var mapHY = map(pos.y, 0, 6000, 0, $('#defaultCanvas0').height());
			curveVertex(mapHX, mapHY);

			if (i == 0)
				curveVertex(mapHX, mapHY);
			if (i == history.length - 1)
				curveVertex(mapHX, mapHY);
		}
		endShape();
		//history of points for display of tail

	}

	this.clearHistory = function() {
		this.history.splice(0, this.history.length)
	}

	this.getTotalDistanceWalked = function() {
		var distance = 0;
		for (var i = 0; i < (this.interpolateFunctionX._x.length - 1); i++){
			distance += dist(this.interpolateFunctionX._y[i], this.interpolateFunctionY._y[i], this.interpolateFunctionX._y[i+1], this.interpolateFunctionY._y[i+1]);
		}

		console.log("total distance for tag " + this.playerNumber + " = " + distance);

		return distance;
	}

}
