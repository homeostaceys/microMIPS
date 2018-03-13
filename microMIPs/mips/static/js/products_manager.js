$(document).ready( function() {

    var btnDelete = $("#btnDelete");
    var btnEdit = $("#btnEdit");
    var btnAdd = $("#btnAdd");
    var form = $("#form");

    btnDelete.on("click", function () {
        ids = get_checked();

        if (ids.length > 0) {
            $.ajax({
                url: "/prodman/delete/",
                data: { "ids[]": ids },
                success: function (response) {
                    if (response === 'Success')
                        location.reload();
                }
            })
        }
    });

    btnEdit.on("click", function () {
        id = get_checked();

        if (id.length > 0) {
            id = id[0];

            var product = $("td[data-type=name][data-id=" + id + "]").text();
            var description = $("td[data-type=description][data-id=" + id + "]").text();
            var price = $("td[data-type=price][data-id=" + id + "]").text();
            var quantity = $("td[data-type=quantity][data-id=" + id + "]").text();
            var category = $("td[data-type=category][data-id=" + id + "]").text();

            $("#name").val(product);
            $("#description").val(description);
            $("#price").val(price);
            $("#stock").val(quantity);
            $("#category").val(category);

            form.on("submit", function (event) {
                event.preventDefault();

                var data = new FormData(this);
                data.append("id", id);

                $.ajax({
                    url: "/prodman/edit/",
                    method: "POST",
                    data: data,
                    async: false,
                    cache: false,
                    contentType: false,
                    enctype: 'multipart/form-data',
                    processData: false,
                    success: function (response) {
                        if (response === "Success")
                            location.reload();
                    }
                });
            });

            $("#savemodal").modal("show");
        }
    });

    btnAdd.on("click", function (event) {
        event.preventDefault();

        $("#name").val("");
        $("#description").val("");
        $("#price").val(0);
        $("#stock").val(0);
        $("#category").val("Digital");

        form.on("submit", function (event) {
            event.preventDefault();

            var data = new FormData(this);
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

            $.ajax({
                url: "/prodman/add/",
=======
=======
>>>>>>> 8c6a508b7b6e4a51b682310a452a02429b2ebcb9
=======
>>>>>>> 8c6a508b7b6e4a51b682310a452a02429b2ebcb9
            data.append("id", id);

            $.ajax({
                url: "/prodman/edit/",
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 8c6a508b7b6e4a51b682310a452a02429b2ebcb9
=======
>>>>>>> 8c6a508b7b6e4a51b682310a452a02429b2ebcb9
=======
>>>>>>> 8c6a508b7b6e4a51b682310a452a02429b2ebcb9
                method: "POST",
                data: data,
                async: false,
                cache: false,
                contentType: false,
                enctype: 'multipart/form-data',
                processData: false,
                success: function (response) {
                    if (response === "Success")
                        location.reload();
                }
            });
        });

        $("#savemodal").modal("show");
    });

});

function get_checked () {
    var checkboxes = $("input[type=checkbox]:checked");
    var ids = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if ($(checkboxes[i]).attr("data-type") === "check_product") {
            ids.push($(checkboxes[i]).attr("data-id"));
        }
    }

    return ids;
}