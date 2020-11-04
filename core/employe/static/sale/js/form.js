var tblProducts;
var vents = {

    // estructura
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function (){
        var subtotal = 0.00
        var iva = $('input[name="iva"]').val()
        $.each(this.items.products, function (pos, dict) {
            console.log(pos)
            dict.subtotal = dict.cant * parseFloat(dict.pvp)
            subtotal += dict.subtotal
        })
        this.items.subtotal = subtotal
        this.items.iva = this.items.subtotal * iva
        this.items.total = this.items.subtotal + this.items.iva

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2))
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2))
        $('input[name="total"]').val(this.items.total.toFixed(2))

    },
    add: function(item) {
        this.items.products.push(item)
        this.list()
    },
    list: function () {
        this.calculate_invoice()

        tblProducts = $('#tblProducts').DataTable({
            responsive: true,   //me permite que se ajusten los datos a medida que yo vaya cambiando el tamaño de mi pantallas
            autoWidth: false,   //respeta el ancho de las columnas que se asignaron a las tablas
            destroy: true,      //
            deferRender: true,  //trabaja con datos que superen los 50k registros
            data: this.items.products,
            columns: [
                //coloco los nombre de los atributos de mi tabla
                {"data": "id"},
                {"data": "name"},
                {"data": "cate.name"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>'
                    }
                },
                {
                    targets: [-3, -1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'MXN ' + parseFloat(data).toFixed(2)
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cant+'" >'
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                // console.log(row) // Row contiene la etiqueta tr completa del datatable
                // console.log(data) // Contiene el objeto de la tabla
                // usando jquery tomaremos el row actual y utilizaremos el metodo find(buscar)
                // buscaremos dentro del row un input llamado cant
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 999,
                    stepinterval: 1
                })
            },
            initComplete: function (settings, json) {

            }
        });
    }
}



$(function () {
   $('.select2').select2({
        theme: 'bootstrap4',
        langauje: 'es'
   });

   $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        // minDate: moment().format("DD-MM-YYYY"), // Dia maximo que se puede seleccionar y los dias pasados
        // minDate: moment().format("DD-MM-YYYY"), dia minimo que se puede seleccionar en adelante
   });

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 1,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function() {
        vents.calculate_invoice()
    }).val(0.16)

    // Busqueda de productos
    $('input[name="search"]').autocomplete({
      source: function(request, response){
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_products', // le manadamos a vista una action
                'term': request.term //con la petición se obtiene con la palabra term lo que mi buscador esta escribiendo
            },
            dataType: 'json',
        }).done(function (data) {
            response(data);
            console.log(data)
            }).fail(function (jqXHR, textStatus, errorThrown) {
            // alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
      },
      delay: 300, // tiempo de carga de los datos
      minLength: 1, //numero de caracteres que el usuario puede escribir para realizar una busqueda
      select: function(event, ui){ //esta funcion cacha el elmento que se selecciono en un diccionario
        // esta sección de codigo me permite realizar un evento
        event.preventDefault()
        // console.clear()
        // Le enviamos un nuevo elemento con 1, porque el usuario sera el encargado de manipular la cantidad
        ui.item.cant = 1
        ui.item.subtotal = 0.00
        // agregamos el producto
        vents.add(ui.item)
        $(this).val('')
      }
    });

    // evento vaciar lista de detalles de productos
    $('.btnRemoveAll').on('click', function () {

        if(vents.items.products.length === 0){
            return false;
        }

        alert_action('Alerta', '¿Esta seguro de limpiar la lista de detalles?', function () {
            vents.items.products = [];
            vents.list()
        })
    })

    // evento de cantidad
    $('#tblProducts tbody')

        // evento eliminar detalle de producto
        .on('click', 'a[rel="remove"]', function () {

            // tomamos el index actual del datatable
            var tr = tblProducts.cell($(this).closest('td, li')).index();

            alert_action('Alerta', '¿Esta seguro de remover este producto?', function () {
                // la función splice remueve el elemento de la lista, tomando como parametro
                // el index del elemento actual
                vents.items.products.splice(tr.row, 1)
                // actualizamos el datatable
                vents.list()
            })


        })
        .on('change', 'input[name="cant"]', function () {
            console.clear()
            // asignamos el valor actual del formulario a la variable cant y la convertimos a entero
            var cant = parseInt($(this).val());
            // de la instancia actual se tomara el tr cuando se realice un cambio
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            // si se realizo un cambio, accedemos a la estructura y realizamos el cambio, pansadole el row de la tabla
            vents.items.products[tr.row].cant = cant;
            // volvemos a calcular el subtotal
            vents.calculate_invoice();

            // el .node me trae la etiqueta (tr) completa
            // con la jquery modificaremos el html en tiempo real
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('MXN'+vents.items.products[tr.row].subtotal.toFixed(2));
    })

    // event clearButtonSearch
    $('.btnClearSearch').on('click', function() {
        $('input[name="search"]').val('').focus()
    });


    // event submit
    $('form').on('submit', function(e) {
        // detenemos el evento de submit para poder enviar los datos mediante ajax
        e.preventDefault()

        // validamos que el usuario no registre vetas vacias
        if(vents.items.products.length === 0){
            message_error('Debe por lo menos tener un producto en venta.');
            return false;
        }

        // enviamos los datos a la factura utilizando la estructura creada
        // sin embargo cli y date_joined no ha sido ingresados.
        // Ahora mismo lo vamos a hacer
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();


        // este tipo de dato me permite obtener una coleccion de elementos tanto
        // de texto como multimedia haciendo referencia al formulario
        // con la ayuda de this
        var parameters = new FormData();

        // recuperaremos el valor del action de input(hidden) que se creo
        parameters.append('action', $('input[name="action"]').val());

        // enviamos los datos de la estructura convertida en un str
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Alerta de Confirmación', '¿Estas seguro de hacer la siguiente acción?', parameters, function () {
            location.href = '/erp/dashboard/';
        });
    })

    // mostramos el datatable vacio
    vents.list();
});
