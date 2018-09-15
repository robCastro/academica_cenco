$(document).on('submit', '#registrarEncargadoForm', function (a) {
    a.preventDefault();
    $('#btnGuardarEncargado').attr('disabled', true);
    $('#espereG').css('display', 'inline');
        $.ajax({
            type: 'POST',
            url: '/alumnos/registrarEncargado/',
            data: {
                nombre: $('#txtNombreEncargado').val(),
                apellido: $('#txtApellidoEncargado').val(),
                direccion: $('#txtDireccionEncargado').val(),
                correo: $('#txtCorreoEncargado').val(),
                dui: $('#txtDuiEncargado').val(),
                numero:$('#txtTelefonoEncargado').val(),
                tipo:$('#cbxTipoTelefonoEncargado').val(),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            },
            dataType: "json",
            success: function (response) {
                $('#btnGuardarEncargado').attr('disabled', false);
                $('#espereG').css('display', 'none');
                //mostrando msj
                var m = $('#mensajeEmergente');
                m.children('strong').html(response.mensaje);
                m.css('display','block');
                m.css('opacity',1);
                m.removeClass();
                m.addClass('alerta exito');

                //escondiendo modal
                $('#RegistrarEncargado').modal('hide');

                //cambiando foco a msj
                desplazoArriba();

                //agregando a lista de Encargados
                codigosEncargados.push(response.codEncargado);
                nombresEncargados.push(response.nombreEncargado);
                apellidosEncargados.push(response.apellidoEncargado);
                direccionEncargados.push(response.direccionEncargado);
                displayEncargados.push(response.codEncargado + ' | ' + response.nombreEncargado + " " + response.apellidoEncargado);

                //mostrando Detalle Encargados
                document.getElementById('detalleCodigoE').value = response.codEncargado;
                document.getElementById('detalleNombreE').value = response.nombreEncargado;
                document.getElementById('detalleApellidoE').value = response.apellidoEncargado;
                document.getElementById('detalleDireccionE').innerHTML = response.direccionEncargado;
                document.getElementById('detalleEncargado').hidden = false;
                direccionesAlumEncar(); //si alumno no tiene direccion, toma la del recien registrado
                limpiarModalEncargado();
                validarAlumno();
                /* No se puede poner directamente el metodo de validacion en
                 * el text input escondido de codigo de encargado por lo que
                  * estoy poniendo la validacion en to do lugar que genere un
                  * valor para codigo y lo guarde en el textinput*/

            },
            error: function (response) {
                  $('#btnGuardarEncargado').attr('disabled'. false);
                  $('#espereG').css('display', 'none');

                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Error al Guardar el Encargado');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta accionPeligrosa');
                  $('#RegistrarEncargado').modal('hide');
                  desplazoArriba();
            }
        })
    });

$(document).on('submit', '#inscribirAlumno', function (a) {
    a.preventDefault();
    $('#btnGuardarAlumno').attr('disabled', true);
    $('#espereI').css('display', 'inline');

    $.ajax({
        type: 'POST',
        url: '/alumnos/insertarAlum/',
        data: {
            nombre:$('#txtNombreAlumno').val(),
            apellido:$('#txtApellidoAlumno').val(),
            direccion:$('#txtDireccionAlumno').val(),
            correo:$('#txtCorreoAlumno').val(),
            fechaNacimiento:$('#txtFechaNacAlumno').val(),
            dui:$('#txtDuiAlumno').val(),
            grupo:$('#cbxGrupo').val(),
            encargado:$('#detalleCodigoE').val(),
            numero:$('#txtTelefonoAlumno').val(),
            tipo:$('#cbxTipoTelefonoAlumno').val(),
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarAlumno').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.responseText);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            desplazoArriba();
            limpiarPantalla();
            document.getElementById('txtNombreAlumno').value = response.responseText;
        },
        error: function (response) {
            $('#btnGuardarAlumno').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.responseText);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});