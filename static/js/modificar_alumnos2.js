var mostrandoComparacion;







//**************************FUNCIONES COMUNES PARA ALUMNOS INDEPENDIENTES Y DEPENDIENTES**************************************
//para fecha
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

//para busqueda
$( function() {
    $( "#buscarEncargado" ).autocomplete({
        source: displayEncargados,
        minLength: 3,
        close: function( event, ui ) {
            var posicion = displayEncargados.indexOf(document.getElementById('buscarEncargado').value);
            if (posicion != -1){
                document.getElementById('codEncargadoNuevo').value = codigosEncargados[posicion];
                document.getElementById('nombreEncNuevo').value = nombresEncargados[posicion];
                document.getElementById('apellidoEncNuevo').value = apellidosEncargados[posicion];
                document.getElementById('direccionEncNuevo').innerHTML = direccionEncargados[posicion];
            }
            else{
                limpiarDetalleEncargado();
            }
        }
    });
} );

function limpiarDetalleEncargado(){
    document.getElementById('codEncargadoNuevo').value = "";
    document.getElementById('nombreEncNuevo').value = "";
    document.getElementById('apellidoEncNuevo').value = "";
    document.getElementById('direccionEncNuevo').value = "";
}

function desplazoArriba(){
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

window.onload = function () {
    mostrandoComparacion = false;

    //quitando evento escritura en fecha
    var fechaNac = document.getElementById('txtFechaNacAlumno');
    fechaNac.onkeydown = function(e){
        e.preventDefault();
    };

    llenadoEncargados(); //declaracion en html
};


//validaciones
function isEmail(email) {
    if(email == ""){
        return true;
    }
    else{
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }
}

function validarDUI(dui){
    if(dui == ""){
        return true;}
    else{
        var regex = /\d{8}-\d{1}/;
        return regex.test(dui);
    }
}

function validaciones(nombre, apellido, direccion, correo, dui){
    var estado = false;
    estado = (nombre != "" && apellido != "" && direccion != "" && validarDUI(dui) && isEmail(correo))
    return estado;
}

function validarAlumno(){
    var nombre = document.getElementById('txtNombreAlumno').value;
    var apellido = document.getElementById('txtApellidoAlumno').value;
    var direccion = document.getElementById('txtDireccionAlumno').value;
    var fechaNac = document.getElementById('txtFechaNacAlumno').value;
    var correo = document.getElementById('txtCorreoAlumno').value;
    var dui = document.getElementById('txtDuiAlumno').value;
    if (!isEmail(correo)){
        document.getElementById('txtCorreoAlumno').className = "form-control is-invalid";
    }
    else{
        document.getElementById('txtCorreoAlumno').className = "form-control";
    }
    var esValido = validaciones(nombre, apellido, direccion, correo, dui) && fechaNac != "";
    document.getElementById('btnGuardarAlumDep').disabled = !esValido;
}

//**************************FUNCIONES PARA DEPENDIENTES**************************************

function cambiarEncargado(){
    if (cantidadEncargados <= 1){   //si no hay suficientes encargados para hacer un cambio
        var m = $('#mensajeEmergente');
        m.children('strong').html('Solo hay un encargado, cree otro para cambiarlo');
        m.css('display','block');
        m.css('opacity',1);
        m.removeClass();
        m.addClass('alerta accionPeligrosa');
        desplazoArriba();
    }
    else{
        if(mostrandoComparacion){
            document.getElementById('linkCambiar').innerText = "Cambiar";
            document.getElementById('tableBusquedaEnc').hidden = true;
            document.getElementById('cambiarEncargado').hidden = true;
            document.getElementById('datosEncargado').hidden = false;

            document.getElementById('buscarEncargado').value = "";
            document.getElementById('codEncargadoNuevo').value = "";
            document.getElementById('nombreEncNuevo').value = "";
            document.getElementById('apellidoEncNuevo').value = "";
            document.getElementById('direccionEncNuevo').innerHTML = "";

            document.getElementById('chbCambiarEncargado').checked = false;

            mostrandoComparacion = false;
        }
        else {
            document.getElementById('linkCambiar').innerText = "Deshacer";
            document.getElementById('tableBusquedaEnc').hidden = false;
            document.getElementById('cambiarEncargado').hidden = false;
            document.getElementById('datosEncargado').hidden = true;

            document.getElementById('chbCambiarEncargado').checked = true;

            mostrandoComparacion = true;
        }
    }
}

function hacerIndependiente(){
    var estadoChb = document.getElementById('hacerIndependiente').checked;
    var titulo = $('#tituloEnc');
    var btnCambiar = document.getElementById('linkCambiar');
    var divBuscarEncargado = $('#tableBusquedaEnc');
    var buscarEncargado = $('#buscarEncargado');
    var datosEncargado = $('#datosEncargado');
    var divCambiarEncargado = $('#cambiarEncargado');
    var msjIndependiente = $('#msjIndependiente');
    if(estadoChb){
        titulo.addClass('text-muted');
        datosEncargado.addClass('text-muted');
        divBuscarEncargado.addClass('text-muted');
        divCambiarEncargado.addClass('text-muted');

        buscarEncargado.prop("disabled", true);
        btnCambiar.disabled = true;

        msjIndependiente.prop("hidden", false);
    }
    else{
        titulo.removeClass();
        titulo.addClass('text-primary');
        datosEncargado.removeClass();
        datosEncargado.addClass('text-primary');
        divBuscarEncargado.removeClass();
        divBuscarEncargado.addClass('text-primary');
        divCambiarEncargado.removeClass();
        divCambiarEncargado.addClass('text-primary');

        buscarEncargado.prop("disabled", false);
        btnCambiar.disabled = false;

        msjIndependiente.prop("hidden", true);
    }
}


$(document).on('submit', '#guardarAlDep', function (a) {
    a.preventDefault();
    $('#btnGuardarAlumDep').attr('disabled', true);
    $('#espereI').css('display', 'inline');

    $.ajax({
        type: 'POST',
        url: '/alumnos/guardarAlDep/',
        data: {
            codigo:$('#txtCodigoAlumno').val(),
            nombre:$('#txtNombreAlumno').val(),
            apellido:$('#txtApellidoAlumno').val(),
            direccion:$('#txtDireccionAlumno').val(),
            correo:$('#txtCorreoAlumno').val(),
            fechaNacimiento:$('#txtFechaNacAlumno').val(),
            dui:$('#txtDuiAlumno').val(),
            hacerIndep:$('#hacerIndependiente').is(":checked"),
            cambiarEncargado:$('#chbCambiarEncargado').is(":checked"),
            codNuevoEncargado:$('#codEncargadoNuevo').val(),
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarAlumDep').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html("Cambios Realizados!");
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarAlumDep').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html("Error");
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});



//**************************FUNCIONES PARA ALUMNOS INDEPENDIENTES**************************************
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





/*$(document).on('submit', '#frmCambiarEncargado', function (a) {
    a.preventDefault();
    if (cantidadEncargados > 1){
        $('#linkCambiar').attr('disabled', true);
        $('#espereG').css('display', 'inline');
        $.ajax({
            type: 'POST',
            url: '/alumnos/registrarEncargado/',
            data: {
                yaConsultados: $('#yaConsultados').val(),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            },
            dataType: "json",
            success: function (response) {
                $('#btnGuardarEncargado').attr('disabled', false);
                $('#espereG').css('display', 'none');
                desplazoArriba();
            },
            error: function (response) {
                  $('#btnGuardarEncargado').attr('disabled'. false);
                  $('#espereG').css('display', 'none');
            }
        })
    }
    else{
        var m = $('#mensajeEmergente');
        m.children('strong').html('Solo hay un encargado, cree otro para cambiarlo');
        m.css('display','block');
        m.css('opacity',1);
        m.removeClass();
        m.addClass('alerta accionPeligrosa');
        desplazoArriba();
    }

});*/