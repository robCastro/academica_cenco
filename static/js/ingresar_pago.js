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
            $('#btnGuardar').prop('disabled', false);
            $('#txtCantidadSemanas').val('');
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