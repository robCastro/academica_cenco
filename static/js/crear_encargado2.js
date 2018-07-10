$(document).on('submit', '#registrarEncargado', function (a) {
    a.preventDefault();
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
                //mostrando msj
                var m = $('#mensajeEmergente');
                m.children('strong').html(response.mensaje);
                m.css('display','block');
                m.css('opacity',1);
                m.removeClass();
                m.addClass('alerta exito');

                //escondiendo modal
                $('#RegistrarEncargado').modal('hide');

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

                validarAlumno();
                /* No se puede poner directamente el metodo de validacion en
                 * el text input escondido de codigo de encargado por lo que
                  * estoy poniendo la validacion en todo lugar que genere un
                  * valor para codigo y lo guarde en el textinput*/
            },
            error: function (response) {
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Error al Guardar el Encargado');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta accionPeligrosa');
                  $('#RegistrarEncargado').modal('hide');
            }
        })
    });

$(document).on('submit', '#inscribirAlumno', function (a) {
    a.preventDefault();

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
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split("$")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            //funcion para limpiar toda la pantalla quiza
        },
        error: function (response) {
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split("$")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
        }
    })
});