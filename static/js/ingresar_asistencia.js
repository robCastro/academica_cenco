window.onload = function(){
    filterSelection('all')
};

function filterSelection(c) {
    var x, i;
    x = document.getElementsByClassName("alumnoRow");
    if(c==null) c = "all";
    for (i = 0; i < x.length; i++) {
        RemoveClass(x[i], "show");
        if (x[i].className.indexOf(c) > -1) AddClass(x[i], "show");
    }
}

function AddClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
    }
}

function RemoveClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}


function desplazoArriba(){
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

function marcarTodos(){
    console.log("Marcando Todos")
    var estado = !document.getElementById('todosMarcados').checked;
    for (var i=0; i<codigosAlumnos.length; i++){
        document.getElementById(codigosAlumnos[i]).checked = estado;
    }
    document.getElementById('todosMarcados').checked = estado;
}

/*
$(document).on('submit', '#guardarAsistencia', function (a) {
    a.preventDefault();
    $('#btnGuardarAsistencia').attr('disabled', true);
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
        dataType : "json",
        success:function (response) {
            $('#btnGuardarAlumno').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.mensaje);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            desplazoArriba();
            limpiarPantalla();
        },
        error: function (response) {
            $('#btnGuardarAlumno').attr('disabled', false);
            $('#espereI').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.mensaje);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});*/
