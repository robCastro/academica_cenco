var mostrandoComparacion;

$( function() {
    $( "#txtFechaNacAlumno" ).datepicker({
        dateFormat: "dd/mm/yy",     //display de la fecha
        altFormat: "yy-mm-dd",      //manejo para backend (NO FUNCIONA), se manda como dateFormat
        minDate: "-90Y",
        yearRange: "-90:+1",
        monthNames: [ "Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
        monthNamesShort: [ "Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
        dayNamesMin: [ "Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa" ],
        changeMonth: true,
        changeYear: true,
    });
} );

function cambiarEncargado(){
    if(mostrandoComparacion){
        document.getElementById('linkCambiar').innerText = "Cambiar";
        document.getElementById('tableBusquedaEnc').hidden = true;
        document.getElementById('cambiarEncargado').hidden = true;
        document.getElementById('datosEncargado').hidden = false;
        mostrandoComparacion = false;
    }
    else {
        document.getElementById('linkCambiar').innerText = "Deshacer";
        document.getElementById('tableBusquedaEnc').hidden = false;
        document.getElementById('cambiarEncargado').hidden = false;
        document.getElementById('datosEncargado').hidden = true;
        mostrandoComparacion = true;
    }
}

function asignarEncargado(){
    if(mostrandoComparacion){
        document.getElementById('linkAsignarEnc').innerText = "Asignar Encargado";
        document.getElementById('asignarEncargado').hidden = true;
        document.getElementById('tableBusquedaEnc').hidden = true;
        document.getElementById('datosEncargado').hidden = true;
        mostrandoComparacion = false;
    }
    else {
        document.getElementById('linkAsignarEnc').innerText = "Cancelar";
        document.getElementById('asignarEncargado').hidden = false;
        document.getElementById('tableBusquedaEnc').hidden = false;
        document.getElementById('datosEncargado').hidden = false;
        mostrandoComparacion = true;
    }
}

window.onload = function () {

    //para facilitar control de comparacion de encargados
    mostrandoComparacion = false;


    //para evitar que link desplace pantalla hacia arriba
    /*document.getElementById('linkCambiar').addEventListener("click", function (event) {
        cambiarEncargado();
        event.preventDefault();
    });*/
};