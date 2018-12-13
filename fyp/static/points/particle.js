
  function Particle(deviceID, name, playerNumber, teamId){
		this.tagID = deviceID;
		this.name = name;
		this.playerNumber = playerNumber;
		this.teamId = teamId;



		this.history= [];//for tail
		this.interpolateFunctionX = new interpolate();
		this.interpolateFunctionY = new interpolate();


  //to update coordinates
	this.update = function(lerpXY){
		//randomised movement
		this.lerpPoint = createVector(lerpXY.x, lerpXY.y);
    //var v = createVector(this.lerpPoint.x,this.lerpPoint.y);
		this.history.push(this.lerpPoint);
		if(this.history.length > 25)
		{
			this.history.splice(0,1);
		}
  }
 
	//to show point
	this.show = function(){
		//draw the point
		stroke(0);
		if(this.playerNumber>=0 && this.playerNumber<6){
			fill(0,0, 255);
		}
		if(this.playerNumber>=6 && this.playerNumber<10){
			fill(255,140,0);
		}

		var mapX= map(this.lerpPoint.x,0,7770, 0, 700);
		var mapY= map(this.lerpPoint.y,0,6000, 0, 540);
		ellipse(mapX,mapY, 20,20);//image
		txt = this.playerNumber+1;
		fill(255);
		text(txt, mapX- textWidth(txt)/2, mapY +2);
		console.log("mapX: "+ mapX)
		console.log("mapY: "+ mapY)
		
		//loop through history
		noFill();
		beginShape();
		for(var i = 0; i<this.history.length; i++)
		{
			var pos = this.history[i];
			var mapHX= map(pos.x,0,7770, 0, 700);
			var mapHY= map(pos.y,0,6000, 0, 540);
			curveVertex(mapHX,mapHY);
      
      if(i ==0)
      curveVertex(mapHX,mapHY);
      if(i==history.length-1)
      curveVertex(mapHX,mapHY);
		}
		endShape();
    //history of points for display of tail

	}	
	
}
