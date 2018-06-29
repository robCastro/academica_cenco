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

$(".deletebutton").on('click', function() {
  var checked = jQuery('input:checkbox:checked').map(function () {
    return this.value;
    }).get();
jQuery('input:checkbox:checked').parents("tr").remove();
});




$(function () {
    habilitarBorrar();
});

function habilitarBorrar() {
    $(".checkbox").click(function(){
        $('.delete').prop('disabled',$('input.checkbox:checked').length == 0);
    });
}



$(document).on('submit', '#nuevoTelefonoForm', function (a) {
    a.preventDefault();

    $.ajax({
        type: 'POST',
        url: $(this).attr("href"),
        data: {
            alumno:$('#id_alumno').val(),
            numero:$('#id_numero').val(),
            tipo:$('#id_tipo').val(),
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function(response) {
          alert("Número creado con exito");
          $('#dinamicos').append(response);
          filterSelection('all');
          $('#agregarTelefonoModal').modal('hide');
          habilitarBorrar();

                  }
    })
})


