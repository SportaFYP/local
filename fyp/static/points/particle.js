
  function Particle(deviceID){
    this.tagID = deviceID;
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
		fill(0,150);
		ellipse(this.lerpPoint.x,this.lerpPoint.y, 20,20);//image
		
		//loop through history
		noFill();
		beginShape();
		for(var i = 0; i<this.history.length; i++)
		{
			var pos = this.history[i];
			curveVertex(pos.x,pos.y);
      
      if(i ==0)
      curveVertex(pos.x,pos.y);
      if(i==history.length-1)
      curveVertex(pos.x,pos.y);
		}
		endShape();
    //history of points for display of tail

	}	
	
}
