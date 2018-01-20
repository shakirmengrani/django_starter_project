var ArtistPage = {
    base_url: '/application/artist/',
    fields: { id: 0, name: "" },
    setFields: function() {
        $("[name='name']").val(ArtistPage.fields.name);
    },

    resetFields: function() {
        ArtistPage.fields = { id: 0, name: "" };
        ArtistPage.setFields();
    },

    getData: function(id) {
        viewer.sendRequest({
            url: ArtistPage.base_url,
            method: 'GET',
            data: { id: id },
            success: function(resp) {
                ArtistPage.fields = {
                    id: resp.data.id,
                    name: resp.data.name
                };
                ArtistPage.setFields();
            },
            error: function(errResp) {

            }
        });
    },

    save: function() {
        var method = "POST";
        if (ArtistPage.fields.id > 0) {
            method = "PUT"
        }
        viewer.sendRequest({
            url: ArtistPage.base_url,
            method: method,
            data: ArtistPage.fields,
            success: function(resp) {
                viewer.alert(resp.message, "success");
                ArtistPage.fields = { id: 0, name: "" };
                ArtistPage.setFields();
            },
            error: function(errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },
    delete: function(id) {
        viewer.sendRequest({
            url: ArtistPage.base_url,
            method: "DELETE",
            data: { id: id },
            success: function(resp) {
                viewer.alert(resp.message, "success");
                ArtistPage.fields = { id: 0, name: "" };
                ArtistPage.setFields();
            },
            error: function(errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    }
};
$(document).ready(function() {

    $("[name='btn_reset']").on('click', function() {
        ArtistPage.resetFields();
    });

    $("[name='btn_save']").on('click', function() {
        ArtistPage.fields = {
            id: ArtistPage.fields.id > 0 ? ArtistPage.fields.id : 0,
            name: $("[name='name']").val()
        }
        ArtistPage.save();
    });

    $("[name='btn_edit']").on('click', function() {
        var id = $(this).data("id");
        ArtistPage.getData(id);
    });

    $("[name='btn_delete']").on('click', function() {
        var id = $(this).data("id");
        ArtistPage.delete(id);
    });
});