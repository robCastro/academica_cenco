
    $(document).on('submit', '#nuevoEncargadoForm', function (a) {
        a.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/alumnos/insertarEncargado/',
                data: {
                    nombre: $('#id_nombreE').val(),
                    apellido: $('#id_apellidoE').val(),
                    direccion: $('#id_direccionE').val(),
                    correo: $('#id_correoE').val(),
                    fechaNacimiento: $('#id_fechaNacimientoE').val(),
                    dui: $('#id_duiE').val(),
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function (response) {
                    alert("Encargado creado con exito");
                    $('#id_encargado').append(response);
                    $('#agregarEncargadoModal').modal('hide');
                }
            })
        });

    $(document).on('submit', '#ingresarAlumnoForm', function (a) {
        a.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/alumnos/insertar/',
            data: {
                nombre:$('#id_nombre').val(),
                apellido:$('#id_apellido').val(),
                direccion:$('#id_direccion').val(),
                correo:$('#id_correo').val(),
                fechaNacimiento:$('#id_fechaNacimiento').val(),
                dui:$('#id_dui').val(),
                grupo:$('#id_grupo').val(),
                encargado:$('#id_encargado').val(),
                csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
            },
            success:function () {
              alert("Alumno creado con exito");

            }
        })
    });
