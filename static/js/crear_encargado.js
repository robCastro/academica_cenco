$(document).on('submit', '#nuevoEncargadoForm', function (a) {
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
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
          alert("Encargado creado con exito");
          $('#dinamicos').append(response);
          filterSelection('all');
          $('#agregarEncargadoModal').modal('hide');
        }
    })
})
