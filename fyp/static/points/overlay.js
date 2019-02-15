class Overlay {
    constructor(name, xorig, yorig, width, height, color) {
        // Store the overlays as a percentage relative to the size of the canvas
        this.name = name;
        this.xorig = xorig;
        this.yorig = yorig;
        this.width = width;
        this.height = height;
        this.color = color;
        this.isVisible = true;
        this.playerTimeInOverlay = []
    }

    // Draw overlay in replay and overlay page
    draw(width, height) {
        fill(this.color);
        rect((this.xorig * width), (this.yorig * height), (this.width * width), (this.height * height));
    }

    // Parameters: Player's x and y coordinates and width and height of the canvas in replay.html
    isPlayerInOverlay(x, y, width, height) {

        if (this.width > 0){
            var xorig = this.xorig
            var x1 = this.xorig + this.width;
        } else {
            var xorig = this.xorig + this.width;
            var x1 = this.xorig;
        }

        if (this.height > 0){
            var yorig = this.yorig
            var y1 = this.yorig + this.height;
        } else {
            var yorig = this.yorig + this.height;
            var y1 = this.yorig;
        }

        var calX = x / width;
        var calY = y / height;

        if (xorig < calX && calX < x1 && yorig < calY && calY < y1){
            return true
        } else {
            return false
        }
    }

    // For the statistics page
    addPlayerIntoOverlayArray(particle, timeInOverlay, color) {
        var obj = { label: particle.playerNumber + " - " + particle.name, y: (timeInOverlay / 1000), color: color }

        this.playerTimeInOverlay.push(obj)
    }
}

function hexToRgbA(hex) {
    var c;
    if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
        c = hex.substring(1).split('');
        if (c.length == 3) {
            c = [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x' + c.join('');
        return 'rgba(' + [(c >> 16) & 255, (c >> 8) & 255, c & 255].join(',') + ', 0.25)';
    }
    throw new Error('Bad Hex');
}

function rgbToHex(rgb) {
    rgb = rgb.match(/^rgba?[\s+]?\([\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?,[\s+]?(\d+)[\s+]?/i);
    return (rgb && rgb.length === 4) ? "#" +
     ("0" + parseInt(rgb[1],10).toString(16)).slice(-2) +
     ("0" + parseInt(rgb[2],10).toString(16)).slice(-2) +
     ("0" + parseInt(rgb[3],10).toString(16)).slice(-2) : '';
}
   

function decodeHTML(html) {
    var txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
}