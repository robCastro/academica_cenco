$('#cbxGrupos').change(function () {
    $('#cbxAlumnos').prop('disabled', true);
    $('#txtCantidadSemanas').prop('disabled', true);
    $('#btnGuardar').prop('disabled', true);
    $('#espereG').css('display', 'inline');
    $.ajax({
        type: 'get',
        url: url_filtro,
        data:{
            cbxGrupos : $('#cbxGrupos').val(),
        },
        datatype: 'json',
        success: function(response){
            console.log(response);
            $('#cbxAlumnos').prop('disabled', false);
            $('#txtCantidadSemanas').prop('disabled', false);
            //$('#btnGuardar').prop('disabled', false);
            $('#txtCantidadSemanas').val('');
            localCodAlumnos = response.codigosAlumnos;
            localNomAlumnos = response.nombresAlumnos;
            localApeAlumnos = response.apellidosAlumnos;
            localCodColegiaturas = response.codigosColegiaturas;
            localTiposPago = response.tiposPago;
            localCuotas = response.cuotas;
            localDescuentos = response.descuentos;
            $('#codAlumno').html(response.codigosAlumnos[0]);
            $('#nomAlumno').html(response.nombresAlumnos[0] + " " + response.apellidosAlumnos[0]);
            $('#codColegiatura').html(response.codigosColegiaturas[0]);
            $('#tipoPago').html(response.tiposPago[0]);
            $('#cuota').html("$" + response.cuotas[0]);
            cuota = parseFloat(response.cuotas[0]);
            if (response.descuentos[0]){
                $('#descuento').html('$0');
                descuento = 0.9;
            }
            else{
                $('#descuento').html('No aplica');
                descuento = 0.0;
            }
            $('#monto').html('$0');
            $('#cbxAlumnos').empty();
            var i = 0;
            var cbxAlumnos = document.getElementById('cbxAlumnos');
            for (i; i < response.codigosAlumnos.length; i++){
                var opcion = document.createElement("option");
                opcion.text = response.nombresAlumnos[i] + " " + response.apellidosAlumnos[i];
                opcion.value = response.codigosAlumnos[i];
                cbxAlumnos.add(opcion);
            }
            $('#espereG').css('display', 'none');
        },
        error: function (response) {
            console.log(response);
            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al consultar Base de Datos, refrescar pagina');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            $('#espereG').css('display', 'none');
        }
    });
});

$("#cbxAlumnos").change(function () {
    $("#txtCantidadSemanas").val("");
    let i = $("#cbxAlumnos").prop("selectedIndex");
    $('#codAlumno').html(localCodAlumnos[i]);
    $('#nomAlumno').html(localNomAlumnos[i] + " " + localApeAlumnos[i]);
    $('#codColegiatura').html(localCodColegiaturas[i]);
    $('#tipoPago').html(localTiposPago[i]);
    $('#cuota').html("$" + localCuotas[i]);
    cuota = parseFloat(localCuotas[i]);
    if (localDescuentos[i]){
        $('#descuento').html('$0');
        descuento = 0.9;
    }
    else{
        $('#descuento').html('No aplica');
        descuento = 0.0;
    }
    $('#monto').html('$0');
});

function validarCantidadSemanas(){
    let regex = /^\d+$/;
    let txtCantidad = document.getElementById('txtCantidadSemanas');
    let i = $("#cbxAlumnos").prop("selectedIndex");
    let m = $('#mensajeEmergente');
    console.log(txtCantidad.value, i, regex.test(txtCantidad.value));
    if (regex.test(txtCantidad.value)){
        var montoAux = 0;
        if (localDescuentos[i]){
            montoAux = parseInt(txtCantidad.value) * localCuotas[i] * 0.9;
            let descuentoAux = parseInt(txtCantidad.value) * localCuotas[i] * 0.1;
            $("#descuento").html("$" + descuentoAux.toString());
        }
        else{
            montoAux = parseInt(txtCantidad.value) * localCuotas[i];
        }
        $("#monto").html("$" + montoAux.toString());
        $("#btnGuardar").prop("disabled", false);
        m.css('display','none');
    }
    else{
        console.log('Error en regex');
        $("#btnGuardar").prop("disabled", true);
        m.children('strong').html("Cantidad invalida, revisar");
        m.css('display','block');
        m.css('opacity',1);
        m.removeClass();
        m.addClass('alerta accionPeligrosa');
    }

}

$(document).on("submit", "#frmIngresarPago", function(e){
    e.preventDefault();
    $("#cbxGrupos").prop('disabled', true);
    $('#cbxAlumnos').prop('disabled', true);
    $('#txtCantidadSemanas').prop('disabled', true);
    $('#btnGuardar').prop('disabled', true);
    $('#espereG').css('display', 'inline');
    $.ajax({
        type: 'POST',
        url : url_guardar,
        data: {
            codColegiatura : localCodColegiaturas[$("#cbxAlumnos").prop("selectedIndex")],
            cantidadSemanas : $("#txtCantidadSemanas").val(),
            aplicarDescuento : localDescuentos[$("#cbxAlumnos").prop("selectedIndex")],
            csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success : function(response){
            console.log(response);
            var m = $('#mensajeEmergente');
            m.children('strong').html(response);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            $('#espereG').css('display', 'none');
            $("#cbxGrupos").prop('disabled', false);
            $('#cbxAlumnos').prop('disabled', false);
            $('#txtCantidadSemanas').prop('disabled', false);
            $('#btnGuardar').prop('disabled', false);
            desplazoArriba();
        },
        error : function(response){
            console.log(response);
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.responseText);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            $('#espereG').css('display', 'none');
            $("#cbxGrupos").prop('disabled', false);
            $('#cbxAlumnos').prop('disabled', false);
            $('#txtCantidadSemanas').prop('disabled', false);
            $('#btnGuardar').prop('disabled', false);
            desplazoArriba();
        },
    });
});

function desplazoArriba(){
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

