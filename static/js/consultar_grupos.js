
window.onload = function(){
          filterSelection('all')
      };

function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("divGrupo");
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

$(document).on('submit', '#nuevoGrupoForm', function (a) {
    a.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/grupos/consultar/',
        data: {
            fechaInicio:$('#id_fechaInicio').val(),
            horario:$('#id_horario').val(),
            profesor:$('#id_profesor').val(),
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        },
        success:function (response) {
          alert("Grupo creado con exito");
          $('#dinamicos').append(response);
          filterSelection('all');
          $('#agregarGrupoModal').modal('hide');
        }
    })
})