//------histogramme: repartition du nombre de resultat/pays------------construction

//coloration de l'histogramme
//Echelle de coloration vert -> rouge en fonction de la valeur
function getScaleColor(perc) {
	var r, g, b = 0;
	if(perc < 50) {
		g = 255;
		r = Math.round(5.1 * perc);
	}
	else {
		r = 255;
		g = Math.round(510 - 5.10 * perc);
	}
	var h = r * 0x10000 + g * 0x100 + b * 0x1;
	return '#' + ('000000' + h.toString(16)).slice(-6);
}

//Couleur aléatoire
function getRandomColor() {
    var length = 6;
    var chars = '0123456789ABCDEF';
    var hex = '#';
    while (length--) hex += chars[(Math.random() * 16) | 0];
    return hex;
}

//Déssine l'histogramme de la repartition des tweet par pays et colore les pays dans la carte
function draw_hist(origin) {
    var l = document.getElementById('histo').offsetWidth;
    console.log(l)

    var nombre_bar = Object.keys(origin).length+2;
        console.log(l / nombre_bar)
    var largeur_bar = l / nombre_bar;
    var longueur_max_bar = 500;
    var legend = '<div style="width:'+largeur_bar+'px;display: inline-block"></div>';
    var max = 0
    for (cle in origin) {
        valeur = origin[cle]
        if (max < valeur) {
            max = valeur;
        }
    }

    var histo = document.getElementById("histo");
    histo.style.borderBottom = "2px solid black"

    //Creer l'echelle
    var legend_detail = 10
    var bar_step = longueur_max_bar / legend_detail;
    var value_step = max / legend_detail;
    var scale_leg = document.createElement('div');
    scale_leg.style.cssFloat = "left";
    scale_leg.style.width = largeur_bar+"px";
    scale_leg.style.borderRight = "2px solid black"
    for(var i = legend_detail-1; i >= 0 ; i--){
        var div = document.createElement('div');
        div.style.height = bar_step+"px";
        div.style.textAlign = "right";
        div.style.lineHeight = bar_step+"px";
        div.style.padding = "auto";
        div.style.color = getScaleColor(Math.round((((i*value_step)+value_step/2)/max)*100));
        caret = document.createElement('s');
        caret.innerText = " - ";
        text = document.createTextNode(Math.round((i*value_step)+value_step/2)+" ");
        div.appendChild(text);
        div.appendChild(caret)
        scale_leg.appendChild(div)
    }
    histo.appendChild(scale_leg);

    var graph = document.createElement('div');
    graph.style.display = "inline-block";

    //Creer Les bar et les legendes en dessous d'elles
    for (var k in origin) {
        var pct = origin[k] / max;
        var color = getScaleColor(Math.round(pct*100));
        //Creer la Barre
        var cv = document.createElement('canvas');
        cv.id =  k + "hi";
        cv.width = largeur_bar;
        cv.height = pct * longueur_max_bar;
        cv.style = 'border:1px solid #000000;';
        cv.style.backgroundColor = color;
        graph.appendChild(cv);
        //Creer la Legende
        leg = "<div id=\"" + k + "hi_leg" + "\" width=\"" + largeur_bar + "\" height= 50 style=\"width: "+largeur_bar+"px;display: inline-block; font-weight: bold;color: "+color+"\">"+k+"<\/div>"
        legend = legend + leg
        //Colorie le pays correspondant
        var pays_carte = document.getElementById(k.toLowerCase()).children;
        for (var i = 0; i < pays_carte.length; i++) {
            pays_carte[i].style.fill = color
        }
    }

    histo.appendChild(graph);
    document.getElementById("plus_info").innerHTML = legend;
}



//coloration de l'histogramme
function color_hist(ori) {
    for (var k in ori) {
        // var color = getRandomColor();
        var color = getScaleColor()
        var pays_histo = document.getElementById(k + "hi");
        var pays_histo_leg = document.getElementById(k + "hi_leg");

        var pays_carte_parent = document.getElementById(k.toLowerCase());
        var pays_carte = document.getElementById(k.toLowerCase()).children;

        for (var i = 0; i < pays_carte.length; i++) {
            pays_carte[i].style.fill = color

        }
        pays_histo_leg.style.color = color;
        pays_histo.style.backgroundColor = color;

    }
}