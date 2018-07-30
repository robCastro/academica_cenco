    window.onload = function () {
        validarCorreo()
    }

    function desplazoArriba(){
        $("html, body").animate({ scrollTop: 0 }, "slow");
    }

    function isEmail(email) {
        if(email == ""){
            return true;
        }
        else{
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            return regex.test(email);
        }
    }
    function validarCorreo() {
        var correo = document.getElementById('correoModal3').value;
        if (!isEmail(correo)){
            document.getElementById('correoModal3').className = "form-control is-invalid";
        }
        else{
            document.getElementById('correoModal3').className = "form-control";
        }
    }

    function contraseniasIguales() {
            var contrasenia = document.getElementById('contraseniaNueva');
            var repContrasenia = document.getElementById('contraseniaRepetir');

            if(  contrasenia.value != repContrasenia.value ){
                contrasenia.className = "form-control is-invalid";
                repContrasenia.className = "form-control is-invalid";
            }
            else {
                contrasenia.className = "form-control is-valid";
                repContrasenia.className = "form-control is-valid";
            }
        }

    $(document).on('submit', '#cambiarNombreForm', function (a) {
    a.preventDefault();
    $('#btnGuardarModal1').attr('disabled', true);
    $('#espere').css('display', 'inline');
    $.ajax({
        type: 'POST',
        url: '/empleados/director_datos/',
        data: {
            nombre:$('#nombreModal1').val(),
            apellido:$('#apellidoModal1').val(),
            contrasenia1:$('#contraseniaModal1').val(),

            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarModal1').attr('disabled', false);

            $('#cambiarNombreModal').modal('hide');
            $('#espere').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split(",")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');

            var celda2 = response.split(",")[1];
            var row = document.getElementById("row1");
            row.deleteCell(1);
            var cell2=row.insertCell(1);
            cell2.innerHTML = celda2;

            $('#nombreModal1').val(response.split(",")[1].split(" ")[0]);
            $('#apellidoModal1').val(response.split(",")[1].split(" ")[1]);
            $('#contraseniaModal1').val('');

            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarModal1').attr('disabled', false);

            $('#cambiarNombreModal').modal('hide');
            $('#espere').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al guardar los datos. Verifique que la contraseña sea la correcta.');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});

$(document).on('submit', '#cambiarUsuarioForm', function (a) {
    a.preventDefault();
    $('#btnGuardarModal2').attr('disabled', true);
    $('#espereM2').css('display', 'inline');
    $.ajax({
        type: 'POST',
        url: '/empleados/director_datos_usuario/',
        data: {
            usuario:$('#usuarioModal2').val(),
            contrasenia2:$('#contraseniaModal2').val(),

            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarModal2').attr('disabled', false);

            $('#cambiarUsuarioModal').modal('hide');
            $('#espereM2').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split(",")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');

            var celda2 = response.split(",")[1];
            var row = document.getElementById("row2");
            row.deleteCell(1);
            var cell2=row.insertCell(1);
            cell2.innerHTML = celda2;

            $('#usuarioModal2').val(response.split(",")[1].split(" ")[0]);
            $('#contraseniaModal2').val('');

            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarModal2').attr('disabled', false);

            $('#cambiarUsuarioModal').modal('hide');
            $('#espereM2').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al guardar los datos. Verifique que la contraseña sea la correcta.');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});


$(document).on('submit', '#cambiarCorreoForm', function (a) {
    a.preventDefault();
    $('#btnGuardarModal3').attr('disabled', true);
    $('#espereM3').css('display', 'inline');
    $.ajax({
        type: 'POST',
        url: '/empleados/director_datos_correo/',
        data: {
            correo:$('#correoModal3').val(),
            contrasenia3:$('#contraseniaModal3').val(),

            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarModal3').attr('disabled', false);

            $('#cambiarCorreoModal').modal('hide');
            $('#espereM3').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split(",")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');

            var celda2 = response.split(",")[1];
            var row = document.getElementById("row3");
            row.deleteCell(1);
            var cell2=row.insertCell(1);
            cell2.innerHTML = celda2;

            $('#usuarioModal3').val(response.split(",")[1].split(" ")[0]);
            $('#contraseniaModal3').val('');

            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarModal3').attr('disabled', false);

            $('#cambiarCorreoModal').modal('hide');
            $('#espereM3     ').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al guardar los datos. Verifique que la contraseña sea la correcta.');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});


$(document).on('submit', '#cambiarContraseniaForm', function (a) {
    a.preventDefault();
    $('#btnGuardarModal4').attr('disabled', true);
    $('#espereM4').css('display', 'inline');
    $.ajax({
        type: 'POST',
        url: '/empleados/director_datos_contrasenia/',
        data: {
            contrasenia4:$('#contraseniaModal4').val(),
            contraseniaNueva:$('#contraseniaNueva').val(),

            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarModal4').attr('disabled', false);

            $('#cambiarContraseniaModal').modal('hide');
            $('#espereM4').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split("$")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');

            location.reload();

            $('#contraseniaModal4').val('');
            $('#contraseniaNueva').val('')
            $('#contraseniaRepetir').val('');

            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarModal4').attr('disabled', false);

            $('#cambiarContraseniaModal').modal('hide');
            $('#espereM4').css('display', 'none');

            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al guardar los datos. Verifique que la contraseña actual sea la correcta.');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});