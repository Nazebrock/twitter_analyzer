// function nuage(ht) {
//
//     h = "<br>"
//     var nbre_mots = Object.keys(ht).length
//     max = 0; //maximum d'occurences du hashtag
//     for (var [cle, valeur] of Object.entries(ht)) {
//         if (max < valeur) {
//             max = valeur;
//         }
//     }
//     var compteur = 0;
//     for (var k in ht) {
//         compteur = compteur + 1;
//         var saut = ""
//         var pct = ht[k] / max;
//         couleur = "black";
//         if (pct >= 0.2) {
//             couleur = getRandomColor();
//         }
//         if (compteur % 10 == 0) {
//             saut = saut + "<br>"
//         }
//
//         cv = "<font id=\""+k+"\" color=" + couleur + " style=\"font-size:" + (pct + 1) * 100 + "%;\">" + k + "<\/font>" + saut
//         if (pct < 0.01) {
//             cv = "";
//         }
//
//         h = h + cv;
//     }
//
//     return h;
// }
//
// //réaction au boutton affichage des hashtags
// var clicks = 0;
// function print_hasht(hashtags) {
//
//     var onglet = document.getElementById("plus_info")
//     //var cloud = nuage(reponse_objet1.hashtags)
//     if (clicks % 2 == 0) {
//         onglet.innerHTML = cloud
//     }
//     else {
//         onglet.innerHTML = ""
//     }
//     clicks += 1
//
// }

//------histogramme: repartition du nombre de resultat/pays------------construction

function draw_hist(origin) {
    var h = "";

    var nombre_bar = Object.keys(origin).length;
    var largeur_bar = 600 / nombre_bar;

    var max = 0
    for (cle in origin) {
        valeur = origin[cle]
        if (max < valeur) {
            max = valeur;
        }
    }

    var hauteur_bar = 100;
    var couleur = true;
    for (var k in origin) {
        var pct = origin[k] / max;
        cv = "<canvas id=\"" + k + "hi" + "\" width=\"" + largeur_bar + "\" height=\"" + pct * 500 + "\"style=\"border:1px solid #000000;\"><\/canvas>";
        h = h + cv;
    }

    document.getElementById("histo").innerHTML = h;
}

//coloration de l'histogramme
function getRandomColor() {
    var length = 6;
    var chars = '0123456789ABCDEF';
    var hex = '#';
    while (length--) hex += chars[(Math.random() * 16) | 0];
    return hex;
}

//affichage du nombre de reponses du pays clické
function alerter() {
    window.alert(reponse_objet1.places[("" + this.id).toUpperCase()] + " match en " + this.id)
}
function alerter0() {
    window.alert(this.id.substring(0, 2))
}

//coloration de l'histogramme
function color_hist(ori) {
    for (var k in ori) {
        var color = getRandomColor();
        var pays_histo = document.getElementById(k + "hi");

        var pays_carte_parent = document.getElementById(k.toLowerCase());
        var pays_carte = document.getElementById(k.toLowerCase()).children;
        pays_carte_parent.onclick = alerter;
        pays_histo.onclick = alerter0;

        for (var i = 0; i < pays_carte.length; i++) {
            pays_carte[i].style.fill = color

        }
        pays_histo.style += "color:" + color;
        pays_histo.style.border = "10px solid" + color;

    }
}