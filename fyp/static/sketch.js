var particles = [];
var img;  
var tags = [];

function preload() {
  // load image
  img = loadImage("https://preview.ibb.co/m7fWyo/bb_court.png");
  tags = loadImage("https://image.ibb.co/f1cy39/1.png");
  

} 

function setup() {
    var canvas = createCanvas(650, 400);
    canvas.parent('sports-court');
    //particle = new Particle(300, 300);   
    transformData();
   
}

// function mousePressed() {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
//     particles.push(new Particle(mouseX, mouseY, tags));
//     //var b = new Tagsa(mouseX, mouseY, tags);
//    // particles.push(b);
// }
  
function draw() {
  background(255);
   // Displays the image at its actual size at point (0,0)
   image(img, 0, 0); 
  
   tags.resize(0, 20);

   for (var i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].show();
    
}
   //image(tag4, 0, 0);
 
   //particle.update();
   //particle.show();
  
//     for (var i = 0; i < particles.length; i++) {
   
//        particles[i].update();
//        particles[i].show();
       
//    }
}
//data creation method
function transformData(){
	var pointDataX = -6699;
  var pointDataY = 4683;
  var startTime = 1540105543000;//original timestamp to miliseconds)
	dataset	= [];
  var tagID =1;
	var previousTS=1540105543000;
  //timeD = time difference
  var timeD = 0;
  
  for(var y = 0; y<10000; y++) //rows.length
  {         
    timeD = startTime - previousTS;
    //round(random) is so that no decimal points is added, only whole numbers)
    pointDataX += round(random(-50,100));
    //mapping to smaller canvas
    pointDataX= map(pointDataX, 0,4500, 0,600);
    pointDataY += round(random(-50,100));
    //mapping to smaller canvas
    pointDataY= map(pointDataY, 0,4500, 0,600);
   	var vectorPoint= createVector(pointDataX,pointDataY)
    //for each data point, crea)te a object with timestamp, and x+y)
    var point = {
    'points' : vectorPoint,
    'startTime': startTime,
    'timeD' : timeD,
    'tagID' : tagID
    }
    dataset.push(point);
      
    previousTS= startTime;
    
    //add a random amount of miliseconds that "passed" since last movement
    startTime += round(random(0,50));
    //update the tagID randomly, 1 of 10 tags
    tagID += round(random(0,10));
  }
console.log(dataset);
  
}

  // display image (img, x, y)
