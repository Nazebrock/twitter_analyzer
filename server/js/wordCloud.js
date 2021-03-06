function calcFontSize(maxFontSize, minFontSize, maxVal, minVal, val){
    var sizeStep = (maxFontSize - minFontSize)/100;
    var pourcentage = ((val-minVal)/maxVal)*100;
    return minFontSize+(pourcentage*sizeStep);
}

function reverseKeyValue(obj){
    var res = {};
    for (k in obj) {
        if (res[obj[k]] === undefined)
            res[obj[k]] = [k];
        else
            res[obj[k]].push(k);
    }
    return res;
}

function rand(min, max){
    return Math.floor(Math.random() * max) + min;
}

function wordcloud(words, n, maxFontSize, minFontSize){
    console.log('WordCloud Setup');
    var sortedWords = reverseKeyValue(words);
    var keys = Object.keys(sortedWords);
    var sortedKeys = keys.reverse();
    var minHTagVal = sortedKeys[sortedKeys.length-1];
    var maxHtagVal = sortedKeys[0];
    var wd = document.getElementById('wordcloud');
    wd.innerHTML = "Hashtags WordCloud";
    var spanArray = [];
    var wdCount = 0;
    var i = 0;
    // Create Span from words
    while(i < sortedKeys.length && wdCount < n){
        var j = 0
        var k = sortedKeys[i];
        var fontSize = calcFontSize(maxFontSize,minFontSize, maxHtagVal, minHTagVal, k);
        while(j < sortedWords[k].length && wdCount < n){
            var color = "rgb("+rand(1,100)+","+rand(1,100)+","+rand(1,100)+")";
            var p = document.createElement('span');
            p.className += 'word';
            p.style.fontSize = fontSize+"px";
            p.style.color = color;
            p.style.padding = "2px";
            var content = document.createTextNode(sortedWords[k][j]);
            p.appendChild(content);
            spanArray.push(p);
            wdCount++;
            j++;
        }
        i++;
    }
    div = document.createElement('div');
    //Randomly add span
    while(spanArray.length != 0){
        r = rand(0, spanArray.length);
        div.appendChild(spanArray[r]);
        spanArray.splice(r,1);
    }
    wd.appendChild(div);
}