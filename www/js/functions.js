/*
 * Para debug podemos printar en la consola del navegador: console.log(miVariable); 
 * ***  OJO CONVIENE NO DEJAR NINGUN console.log activo porque gasta recursos
 * ***  y la respuesta de las botoneras se verá afectada.
*/

// Función llamada por los eventos de la peich que ordenan algún cambio
function predic_cmd(cmd) {
    // console.log(cmd)

    // Envia el comando 'cmd' a PRE.DI.C a través del código PHP del server:
    // https://www.w3schools.com/js/js_ajax_http.asp
    var myREQ = new XMLHttpRequest();
    myREQ.open("GET", "php/functions.php?command=" +  cmd, true);
    myREQ.send();

    // Y actualizamos el nuevo estado en la página
    get_predic_status();
}

// Auto update que se activará al cargar la peich en el navegador
function page_auto_update() {
    // OjO aquí con parentesis y en el setInterval SIN paréntesis:
    get_predic_status();
    setTimeout( setInterval( get_predic_status, 3000 ), 500);
}

// Obtiene el estado de PRE.DIC.C hablando con el PHP del server
function get_predic_status() { 
    // https://www.w3schools.com/js/js_ajax_http.asp
       
    // Prepara una instancia HttpRequest
    var myREQ = new XMLHttpRequest();
    
    // Dispara una acción cuando se haya completado el HttpRequest,
    // nosotros actualizaremos la peich con la respuesta del server.
    myREQ.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            page_update(this.responseText);
        }
    };
    
    // Ejecuta la transacción HttpRequest
    myREQ.open(method="GET", url="php/functions.php?command=status", async=true);
    myREQ.send();
}

// Vuelca el estado de PRE.DI.C en la peich
function page_update(status) {
    
    document.getElementById("status_LEV").innerHTML = 'LEVEL: ' + status_decode(status, 'level');
    document.getElementById("status_BAL").innerHTML = 'BAL: '   + status_decode(status, 'balance');
    document.getElementById("status_XO" ).innerHTML = 'XO: '    + status_decode(status, 'XO_set');

    document.getElementById("status_DRC").innerHTML = 'DRC: '   + status_decode(status, 'DRC_set');

    document.getElementById("status_BAS").innerHTML = 'BASS: '  + status_decode(status, 'bass');
    document.getElementById("status_TRE").innerHTML = 'TREB: '  + status_decode(status, 'treble');

    document.getElementById("status_INP").innerHTML = 'INPUT: ' + status_decode(status, 'input');

    document.getElementById("buttonMono").innerHTML = OnOff( 'mono', status_decode(status, 'mono') );
    document.getElementById("buttonMute").innerHTML = OnOff( 'mute', status_decode(status, 'muted') );
    document.getElementById("buttonLoud").innerHTML = OnOff( 'loud', status_decode(status, 'loudness_track') );
}

// Averigua el valor de una de las propiedades del chorizo status de PRE.DI.C
function status_decode(status, prop) {
    //console.log(status)
    result = null
    arr = status.split("\n"); // Casa propiedad:valor vienen separados por saltos de línea
    //console.log(arr)
    for ( i in arr ) {
        //console.log(arr[i])
        if ( prop == arr[i].split(":")[0] ) {
            result = arr[i].split(":")[1]
        }
    }
    return String(result).trim();
}

// Auxiliar para rotular propiedades como por ejemplo muted:true/false ==> 'MUTE ON' / 'mute off'
function OnOff(prop, truefalse) {
    label = prop + ' off'
    if ( truefalse == 'true' ) { label = prop.toUpperCase() + ' ON'; }
    return label;
}
