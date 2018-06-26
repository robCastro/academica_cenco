  var indexSelected;

    // Se deshabilitan los botones que dependen de la seleccion al cargar.
    window.onload = function(){
        $('#btnEliminarHorario').prop('disabled', true);
        $('#btnEditarHorario').prop('disabled', true);
      };
        //Esta funcion recoge valores de la fila seleccionada en la tabla
       $(function() {
            selectFilas();
        });

       function selectFilas(){
            var tr = $('#tabla_horarios').find('tr');
            tr.bind('click', function(event) {
                tr.removeClass('row-highlight');
                indexSelected = tr.index($(this));
                var tds = $(this).addClass('row-highlight').find('td');
                    values = tds[1].innerHTML+ " de "+ tds[2].innerHTML+" a "+tds[3].innerHTML;

                //Habilitar botones de eliminacion y edicion
                $('#btnEliminarHorario').prop('disabled', false);
                $('#btnEditarHorario').prop('disabled', false);

                // Asignacion a formulario para editar.
                $('#id_horario_a_editar').html(tds[0].innerHTML);
                $('#id_dias_asignadosEd').val(tds[1].innerHTML);
                $('#id_hora_inicioEd').val(tds[2].innerHTML);
                $('#id_hora_finEd').val(tds[3].innerHTML);

                //Asignacion de id para eliminar.
                $('#eliminar').html(tds[0].innerHTML);
                $('#eliminarElemento').html(values);
            });
       }

        $(document).on('submit', '#EliminarHorarioForm', function (a) {
        a.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/horarios/eliminar/',
                data: {
                    id: $('#eliminar').html(),
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function (response) {
                  $('#EliminarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Horario eliminado con exito');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta cuidado');
                  document.getElementById("tabla_horarios").deleteRow(indexSelected);


                },
                error: function (response) {
                  $('#EliminarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Error al eliminar. Seleccione un horario d&oacute;nde no asista ning&uacute;n estudiante.');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta accionPeligrosa');
                }
            })
        });

        $(document).on('submit', '#nuevoHorarioForm', function (a) {
        a.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/horarios/crear/',
                data: {
                    dias_asignados: $('#id_dias_asignados').val(),
                    hora_inicio: $('#id_hora_inicio').val(),
                    hora_fin: $('#id_hora_fin').val(),
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function (response) {
                  $('#AgregarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Horario agregado con exito.');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta exito');
                  var fila = response.split(',');
                  var table = document.getElementById("tabla_horarios");
                  var row = table.insertRow(-1);
                  var cell1 = row.insertCell(0);
                  var cell2 = row.insertCell(1);
                  var cell3 = row.insertCell(2);
                  var cell4 = row.insertCell(3);
                  var cell5 = row.insertCell(4);
                  cell1.innerHTML = fila[0];
                  cell2.innerHTML = fila[1];
                  cell3.innerHTML = fila[2];
                  cell4.innerHTML = fila[3];
                  cell5.innerHTML = fila[4];
                   selectFilas();
                  },
                error: function (response) {
                  $('#AgregarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Ocurri&oacute; un error al guardar. Verifique que no choquen los horarios y las horas sean correctas');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta accionPeligrosa');
                }
            })
        });

       $(document).on('submit', '#editarHorarioForm', function (a) {
        a.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/horarios/editar/',
                data: {
                    id: $('#id_horario_a_editar').html(),
                    dias_asignados: $('#id_dias_asignadosEd').val(),
                    hora_inicio: $('#id_hora_inicioEd').val(),
                    hora_fin: $('#id_hora_finEd').val(),
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function (response) {
                  $('#EditarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Horario modificado con exito.');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta exito');
                  var fila = response.split(',');
                  var table = document.getElementById("tabla_horarios");
                  table.deleteRow(indexSelected);
                  var row = table.insertRow(indexSelected);
                  var cell1 = row.insertCell(0);
                  var cell2 = row.insertCell(1);
                  var cell3 = row.insertCell(2);
                  var cell4 = row.insertCell(3);
                  var cell5 = row.insertCell(4);
                  cell1.innerHTML = fila[0];
                  cell2.innerHTML = fila[1];
                  cell3.innerHTML = fila[2];
                  cell4.innerHTML = fila[3];
                  cell5.innerHTML = fila[4];
                  selectFilas();
                },
                error: function (response) {
                  $('#EditarHorario').modal('hide');
                  var m = $('#mensajeEmergente');
                  m.children('strong').html('Ocurri&oacute; un error al editar. Verifique que no choquen los horarios y las horas sean correctas');
                  m.css('display','block');
                  m.css('opacity',1);
                  m.removeClass();
                  m.addClass('alerta accionPeligrosa');
                }
            })
        });
