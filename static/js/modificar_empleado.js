    window.onload = function () {
        validarEmpleado()
    }

    function desplazoArriba(){
        $("html, body").animate({ scrollTop: 0 }, "slow");
    }
    //validaciones
    function validarNom(nom) {
        if(nom == ""){
            return false;
        }
        else{
            var regex = /(^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$)|(^[a-zA-ZñÑáéíóúÁÉÍÓÚ]+ ?[a-zA-ZñÑáéíóúÁÉÍÓÚ]+$)/;
            return regex.test(nom);
        }
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
    function validarTelefono(telefono){
        if(telefono == ""){
            return false;}
        else{
            var regex = /(2|6|7)\d{7}/;
            return regex.test(telefono);
        }
    }
    function validarDUI(dui){
        if(dui == ""){
            return false;}
        else{
            var regex = /\d{8}-\d{1}/;
            return regex.test(dui);
        }
    }
     function validarNIT(nit){
        if(nit == ""){
            return false;}
        else{
            var regex = /\d{4}-\d{6}-\d{3}-\d{1}/;
            return regex.test(nit);
        }
    }
     function validarISSS(isss){
        if(isss == ""){
            return false;}
        else{
            var regex = /\d{9}/;
            return regex.test(isss);
        }
    }
     function validarAFP(afp){
        if(afp == ""){
            return false;}
        else{
            var regex = /\d{12}/;
            return regex.test(afp);
        }
    }
    function validaciones(nombre, apellido, direccion, correo, dui, telefono,nit,isss,afp){
        var estado = false;
        estado = (validarNom(nombre) && validarNom(apellido) && direccion != "" && validarDUI(dui) && validarTelefono(telefono) && isEmail(correo) && validarNIT(nit) && validarISSS(isss) && validarAFP(afp))
        return estado;
    }
    function validarEmpleado() {
        var nombre=document.getElementById('txtNombreEmpleado').value;
        var apellido = document.getElementById('txtApellidoEmpleado').value;
        var direccion = document.getElementById('txtDireccionEmpleado').value;
        var dui = document.getElementById('txtDuiEmpleado').value;
        var telefono = document.getElementById('txtTelefonoEmpleado').value;
        var nit = document.getElementById('txtNitEmpleado').value;
        var isss = document.getElementById('txtIsssEmpleado').value;
        var afp = document.getElementById('txtAfpEmpleado').value;
        var correo = document.getElementById('txtCorreoEmpleado').value;
        if (!validarNom(nombre)){
            document.getElementById('txtNombreEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtNombreEmpleado').className = "form-control";
        }
        if (!validarNom(apellido)){
            document.getElementById('txtApellidoEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtApellidoEmpleado').className = "form-control";
        }
        if (!isEmail(correo)){
            document.getElementById('txtCorreoEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtCorreoEmpleado').className = "form-control";
        }
        if (!validarTelefono(telefono)){
            document.getElementById('txtTelefonoEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtTelefonoEmpleado').className = "form-control";
        }
        if (!validarDUI(dui)){
            document.getElementById('txtDuiEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtDuiEmpleado').className = "form-control";
        }
        if (!validarNIT(nit)){
            document.getElementById('txtNitEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtNitEmpleado').className = "form-control";
        }
        if (!validarISSS(isss)){
            document.getElementById('txtIsssEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtIsssEmpleado').className = "form-control";
        }
        if (!validarAFP(afp)){
            document.getElementById('txtAfpEmpleado').className = "form-control is-invalid";
        }
        else{
            document.getElementById('txtAfpEmpleado').className = "form-control";
        }
        var esValido = validaciones(nombre, apellido, direccion, correo, dui, telefono,nit,isss,afp);
        document.getElementById('btnGuardarEmpleado').disabled = !esValido;
    }


$(document).on('submit', '#modificarEmpleado', function (a) {
    a.preventDefault();
    $('#btnGuardarEmpleado').attr('disabled', true);
    $('#espereM').css('display', 'inline');
    url_mod = $("#modificarEmpleado").attr('action');
    $.ajax({
        type: 'POST',
        url: url_mod,
        data: {
            nombre:$('#txtNombreEmpleado').val(),
            apellido:$('#txtApellidoEmpleado').val(),
            direccion:$('#txtDireccionEmpleado').val(),
            correo:$('#txtCorreoEmpleado').val(),
            dui:$('#txtDuiEmpleado').val(),
            nit:$('#txtNitEmpleado').val(),
            isss:$('#txtIsssEmpleado').val(),
            afp:$('#txtAfpEmpleado').val(),
            tipoEmp:$('#cbxRolEmpleado').val(),
            numeroTel:$('#txtTelefonoEmpleado').val(),
            tipoTel:$('#cbxTipoTelefonoEmpleado').val(),
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
            $('#btnGuardarEmpleado').attr('disabled', false);
            $('#espereM').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html(response.split("$")[0]);
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta exito');
            desplazoArriba();
        },
        error: function (response) {
            $('#btnGuardarEmpleado').attr('disabled', false);
            $('#espereM').css('display', 'none');
            var m = $('#mensajeEmergente');
            m.children('strong').html('Error al modificar el empleado');
            m.css('display','block');
            m.css('opacity',1);
            m.removeClass();
            m.addClass('alerta accionPeligrosa');
            desplazoArriba();
        }
    })
});