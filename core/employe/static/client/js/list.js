var tblClient;

// esta funcion obtendra el dataTable de mi modelo
function getData(){
    tblClient = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "supername"},
            {"data": "dni"},
            {"data": "birthday"},
            {"data": "sexo.name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning">Actualizar</a> ';
                    buttons += '<a href="#" rel="delete" type="button" class="btn btn-danger">Eliminar</a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}
$(function () {

    // invocamos el metodo para traer los datos
    getData()

    // evento de creación de un nuevo registro implementando un modal qu la hacer un click se abrira el modal
    $('.btnAdd').on('click', function() {
        // al evento le indicamos que tambien el identificador debe de tener el valor add
        $('input[name="action"]').val('add');
        // el formulario se va resetar con los valores por defecto del formulario, cada vez que se cierre el modal
        $('form')[0].reset()
        // el modal se pone en modo visualizacion
        $('#myModalClient').modal('show');
    });

    // actualizar registro
    // creamos un evento en la tabla data, al hacer click en el boton con etiquetado edit
    $('#data tbody').on('click', 'a[rel="edit"]', function() {
        // obtenemos la información del indice sobre la celda seleccionada
        // con diseño responsivo
        var tr = tblClient.cell($(this).closest('td, li')).index();
        // sin diseño responsivo
        var data = tblClient.row(tr.row).data();
        // cambiamos el tipo de accion que quiero realizar
        $('input[name="action"]').val('edit')
        // insertamos los valores de mi diccionario data al formulario
        $('input[name="id"]').val(data.id)
        $('input[name="name"]').val(data.name)
        $('input[name="supername"]').val(data.supername)
        $('input[name="dni"]').val(data.dni)
        $('input[name="birthday"]').val(data.birthday)
        $('input[name="address"]').val(data.address)
        $('select[name="sexo"]').val(data.sexo.id)
        // abrimos nuestro modal
        $('#myModalClient').modal('show')
    });

    // eliminar registro
    $('#data tbody').on('click', 'a[rel="delete"]', function() {
        // obtenemos la información del indice sobre la celda seleccionada
        // con diseño responsivo
        var tr = tblClient.cell($(this).closest('td, li')).index();
        // sin diseño responsivo
        var data = tblClient.row(tr.row).data();

        var parameters = new FormData();
        parameters.append('action', 'delete')
        parameters.append('id', data.id)
        submit_with_ajax(window.location.pathname, 'Alerta de Confirmación',
            '¿Estas seguro de eliminar el siguiente registro?', parameters, function () {
            // y en vez de actualizar la pantalla, solo refrescaremos el dataTable
            tblClient.ajax.reload()
        });
    });

    // sobreescribimos el evento submit, para que se tomen los posibles errores de mi
    // formulario
    $('form').on('submit', function (e) {
        e.preventDefault();

        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Alerta de Confirmación',
            '¿Estas seguro de hacer la siguiente acción?', parameters, function () {
            // cuando realice el submit y sea exitoso mi modal se cerrara
            $('#myModalClient').modal('hide');
            // y en vez de actualizar la pantalla, solo refrescaremos el dataTable
            tblClient.ajax.reload()
        });
    });
});


