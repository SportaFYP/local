var particles = [];
var img;  
var tags = [];

function preload() {
  // load image
  img = loadImage("https://preview.ibb.co/m7fWyo/bb_court.png");
  tags = loadImage("https://image.ibb.co/f1cy39/1.png");
  

} 

function setup() {
    createCanvas(650, 400);
    //particle = new Particle(300, 300);   
   
}

function mousePressed() {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    particles.push(new Particle(mouseX, mouseY, tags));
    //var b = new Tagsa(mouseX, mouseY, tags);
   // particles.push(b);
}
  
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


  // display image (img, x, y)
