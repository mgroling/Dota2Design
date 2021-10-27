// target photoshop 

// This script should be run from within Photoshop 

String.prototype.endsWith = function( str ) {

return this.substring( this.length - str.length, this.length ) === str;

}; // PS runs EMCA3, does not know this function

var orig_ruler_units = app.preferences.rulerUnits;

app.preferences.rulerUnits = Units.PIXELS;

var cTID = function(s) { return app.charIDToTypeID(s); }; // Shorten

var doc = activeDocument;  

var docPath = doc.path;  

var output = '';  

var txtDoc = new File(doc.path + '/' + doc.name.split('.')[0]+'.json');  

doc.activeLayer = doc.layers[0];  

var extension = ".png";

var docWidth = doc.width;

var docHeight = doc.height;

var hw = docWidth/2; var hh = docHeight/2; 

var centerX = (doc.width/2);

var centerY = (doc.height/2);

var cropBounds = [(centerX-hw),(centerY-hh),(centerX+hw),(centerY+hh)];

// When layers/groups are duplicated, PS breaks their

// links and re-links to the new duplicate layer instead.

// Since there is no accurate way to determine layer bounds

// consistently for layers and sets, I need to duplicate and

// flatten layers, which will break links. As a safety, I've 

// added Paul Riggott's functions for setting/reverting history.

createNamedSnapshot("BeforeExport");

var fileLayers = listMatches (doc, extension); // Get a list of layers/sets with extension

compoundList(fileLayers); // Assemble layer info into json string

revertNamedSnapshot("BeforeExport"); // Restore doc to pre-script state

writeFile (txtDoc, output); // Write json to file

deleteNamedSnapshot("BeforeExport");

app.preferences.rulerUnits = orig_ruler_units;

function listMatches(lSet, match){  

    var coords = [];

    for(var i=0;i<lSet.layers.length;i++){  

        doc.activeLayer = lSet.layers;

if(doc.activeLayer.typename == 'LayerSet'){

if(doc.activeLayer.layers.length>0){

if(doc.activeLayer.name.endsWith(match)){

coords.push(doc.activeLayer);

}

var b = listMatches(doc.activeLayer, match);

for(var j=0; j<b.length; j++){

if(b.name.endsWith(match)){

coords.push(b);

}

}

}  

}else{

if(doc.activeLayer.name.endsWith(match)){

coords.push(doc.activeLayer);

}

} 

};//end loop

return coords;

};

function compoundList(array){

var len = array.length;

for(var i=0;i<len;i++){

var l = array;

if(typeof l !== 'undefined'){

var linked = getLayerLinks(l);

if(l.typename == 'LayerSet'){

var b = get_bounds(l);

}else{

var b = l.bounds;

}

var x0 = String(b[0]).split(" ")[0];

var y0 = String(b[1]).split(" ")[0];

var x1 = String(b[2]).split(" ")[0];

var y1 = String(b[3]).split(" ")[0];

var col = getLayerColor(l.id);

if(col == 'grain') col = 'green';

// Make a json string

output += "{";

output += '"name" : "' + l.name + '",';

output += '"x0" : ' + x0 + ',';

output += '"y0" : ' + y0 + ',';

output += '"x1" : ' + x1 + ',';

output += '"y1" : ' + y1 + ',';

output += '"linked" : ' + linked + ',';

output += '"color" : "' + col + '"';

output += "}";

if(i<len-1){

output += ",";

}

output += '\n';

}

}

}

function get_bounds(layer){

var copy = layer.duplicate();

activeDocument.activeLayer = copy;

copy.merge();

copy = activeDocument.activeLayer;

doc.crop(cropBounds);

var b = copy.bounds;

copy.remove();

activeDocument.activeLayer = layer;

return b;

}

function getLayerColor( layer ) {   

var ref = new ActionReference();   

ref.putProperty( charIDToTypeID("Prpr") ,stringIDToTypeID('color'));   

ref.putIdentifier(charIDToTypeID( "Lyr " ), layer );  

return typeIDToStringID(executeActionGet(ref).getEnumerationValue(stringIDToTypeID('color')));   

}; 

function getLayerLinks( layer ) {

var lis = layer.linkedLayers;

var linked = "[";

for(var i=0; i<lis.length; i++){

var layerName = lis.name;

if(layerName.endsWith(extension)){

linked+= '"' + layerName + '"';

if(i<lis.length-1) linked+=",";

}

}

linked += "]";

return linked;

}

// Thanks to Paul Riggott @ Adobe forums for these 2 scripts

function createNamedSnapshot(name) {  

    var desc = new ActionDescriptor();  

        var ref = new ActionReference();  

        ref.putClass( charIDToTypeID('SnpS') );  

    desc.putReference( charIDToTypeID('null'), ref );  

        var ref1 = new ActionReference();  

        ref1.putProperty( charIDToTypeID('HstS'), charIDToTypeID('CrnH') );  

    desc.putReference( cTID('From'), ref1 );  

    desc.putString( charIDToTypeID('Nm  '), name );  

    desc.putEnumerated( charIDToTypeID('Usng'), charIDToTypeID('HstS'), charIDToTypeID('FllD') );  

    executeAction( charIDToTypeID('Mk  '), desc, DialogModes.NO );  

};  

function revertNamedSnapshot(name) {  

    var desc = new ActionDescriptor();  

        var ref = new ActionReference();  

        ref.putName( charIDToTypeID('SnpS'), name );  

    desc.putReference( charIDToTypeID('null'), ref );  

    executeAction( charIDToTypeID('slct'), desc, DialogModes.NO );  

}; 

  

 function deleteNamedSnapshot(name) {  

    var desc = new ActionDescriptor();  

        var ref = new ActionReference();  

        ref.putName( charIDToTypeID('SnpS'), name );  

    desc.putReference( charIDToTypeID('null'), ref );  

    executeAction( charIDToTypeID('Dlt '), desc, DialogModes.NO );  

}; 

  

function writeFile(file, txt) {  

        file.encoding = "UTF8";  

        file.open("w", "TEXT", "????");  

        //unicode signature, this is UTF16 but will convert to UTF8 "EF BB BF"  

        file.write("\uFEFF");  

        file.lineFeed = "unix";  

var preTxt = '{ "Default" : [';

var postTxt = "]}";

file.write(preTxt);

        file.write(txt);

file.write(postTxt);  

        file.close();

alert("JSON Export Created");

    };   