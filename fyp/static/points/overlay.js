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