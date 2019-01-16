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
    }

    draw(width, height) {
        fill(this.color);
        rect((this.xorig * width), (this.yorig * height), (this.width * width), (this.height * height));
        //console.log((this.xorig * width) + " " + (this.yorig * height) + " " + (this.width * width) + " " + (this.height * height));
    }

    isPlayerInOverlay(x, y, width, height) {
        var calX = x / width;
        var calY = y / height;
        var x1 = this.xorig + this.width;
        var y1 = this.yorig + this.height;

        if (this.xorig < calX && calX < x1 && this.yorig < calY && calY < y1){
            return true
        } else {
            return false
        }
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