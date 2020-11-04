$(function () {
    $('#data').DataTable({
        responsive: true,   //me permite que se ajusten los datos a medida que yo vaya cambiando el tamaño de mi pantallas
        autoWidth: false,   //respeta el ancho de las columnas que se asignaron a las tablas
        destroy: true,      //
        deferRender: true,  //trabaja con datos que superen los 50k registros
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            //coloco los nombre de los atributos de mi tabla
            {"data": "id"},
            {"data": "name"},
            {"data": "desc"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/category/edit/' + row.id + '/" class="btn btn-warning">Actualizar</a> '
                    buttons += '<a href="/erp/category/delete/' + row.id + '/" class="btn btn-danger">Eliminar</a>'
                    return buttons
                }
            }
        ],
        initComplete: function (settings, json) {

        }
    });

});
