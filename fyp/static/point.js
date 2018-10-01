//var gravity = 0.1;

function Particle(x, y, tag) {
    this.x = x;
    this.y = y;
    this.tag = tag;

    //this.yspeed = 0;

    this.history = [];

    this.update = function() {
        this.x += random(-20, 20);
        this.y += random(-20, 20);
        //this.y += this.yspeed;
        //this.yspeed += gravity;
 
        //if(this.y > height){
        //    this.y = height;
        //    this.yspeed *= -0.9;
        //}
        
        for (var i = 0; i < this.history.length; i++){
            this.history[i].x += random(-2, 2);
            this.history[i].y += random(-2, 2);
        }


        var v = createVector(this.x, this.y);
        this.history.push(v);

        if (this.history.length > 100) {
            this.history.splice(0, 1);
        }
       
    }

    this.show = function() {
        //stroke(0);
        //fill(0, 50);
        //ellipse(this.x, this.y, 24, 24);

        //tag img
        image(this.tag, this.x, this.y);
        
        noFill();
        beginShape();
        for (var i = 0; i < this.history.length; i++) {
           var pos = this.history[i];
           //fill(random(255));
           //ellipse(pos.x, pos.y, i, i);
           vertex(pos.x, pos.y);
        }
        endShape();

    }
}

