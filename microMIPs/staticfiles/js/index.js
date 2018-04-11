$(document).ready( function(){

    $('#myform').on("submit", function (event) {
        event.preventDefault();
        var data = new FormData(this);

        $.ajax({
            url: "/inputcode/",
            method: "POST",
            data: data,
            async: false,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            success: function (response) {}
        });
    });
    $("body").on("click", "a", function() {
        $('#myform').submit();
    });

});


