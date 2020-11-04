function message_error(obj) {
    var html = ''
    if(typeof (obj) === 'object'){
        html = '<ul style="text-aling: left;">';
        $.each(obj, function(key, value) {
            html += '<li>' + value + '</li>'
        });
        html += '</ul>'
    }
    else {
        html +=  '<p>'+obj+'</p>'
    }

    // sweetAlert colocara lo concatenado de la variable html
    Swal.fire({
        title: 'Error',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
$.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,

        buttons: {
            info: {
                text: "Si, Estoy de Seguro",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false, //que no procese los datos , que los deje exactamente igual
                        contentType: false, //que no configure el tipo de dato
                    }).done(function (data) {
                        // si en post no recibe ningun elemento llamado 'error', entoces retorname a la vista url
                        if (!data.hasOwnProperty('error')) {
                            callback()
                            return false;
                        }
                        // se creo una funcion que me iterara los errores de validacion en el formulario
                        // Si hay un elemento error, la funcion cachara el data donde va el error
                        // con ayuda de la tecnologia AJAX
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-danger',
                action: function () {

                }
            },
        }
    })
}

function alert_action(title, content, callback) {
$.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-success',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-danger',
                action: function () {

                }
            },
        }
    })
}

