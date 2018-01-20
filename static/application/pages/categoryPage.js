var categoryPage = {
    base_url: '/application/category/',
    fields: { id: 0, name: "", feature: 0, type: 1 },
    setFields: function() {
        $("[name='name']").val(categoryPage.fields.name);
        $("[name='type']").val(categoryPage.fields.type);
        if (categoryPage.fields.feature) {
            $("[name='feature']").prop("checked", true);
        } else {
            $("[name='feature']").prop("checked", false);
        }
    },

    resetFields: function() {
        categoryPage.fields = { id: 0, name: "", feature: 0, type: 1 };
        categoryPage.setFields();
    },

    getData: function(id) {
        viewer.sendRequest({
            url: categoryPage.base_url,
            method: 'GET',
            data: { id: id },
            success: function(resp) {
                categoryPage.fields = {
                    id: resp.data.id,
                    name: resp.data.name,
                    feature: resp.data.feature,
                    type: resp.data.type
                };
                categoryPage.setFields();
            },
            error: function(errResp) {

            }
        });
    },

    save: function() {
        var method = "post";
        if (categoryPage.fields.id > 0) {
            method = "put"
        }
        viewer.sendRequest({
            url: categoryPage.base_url,
            method: method,
            data: categoryPage.fields,
            success: function(resp) {
                viewer.alert(resp.message, "success");
                categoryPage.fields = { id: 0, name: "", feature: 0, type: 1 };
                categoryPage.setFields();
            },
            error: function(errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },
    delete: function(id) {
        viewer.sendRequest({
            url: categoryPage.base_url,
            method: "delete",
            data: { id: id },
            success: function(resp) {
                viewer.alert(resp.message, "success");
                categoryPage.fields = { id: 0, name: "", feature: 0 };
                categoryPage.setFields();
            },
            error: function(errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },

    getType: function(){
        var types = [{id: 1, name: "Album"},{id: 2, name: "Track"},{id: 3, name: "Video"}]
        types.forEach(function(item){
            var option = "<option value='" + item.id + "'>" + item.name + "</option>";
            $("[name='type']").append(option);
        });
    }
};

$(document).ready(function() {
    categoryPage.getType();
    $("[name='btn_reset']").on('click', function() { categoryPage.resetFields(); });

    $("[name='btn_save']").on('click', function() {
        categoryPage.fields = {
            id: categoryPage.fields.id > 0 ? categoryPage.fields.id : 0,
            name: $("[name='name']").val(),
            type: $("[name='type']").val(),
            feature: ($("[name='feature']:checked").val() ? 1 : 0)
        }
        categoryPage.save();
    });

    $("[name='btn_edit']").on('click', function() {
        var id = $(this).data("id");
        categoryPage.getData(id);
    });

    $("[name='btn_delete']").on('click', function() {
        var id = $(this).data("id");
        categoryPage.delete(id);
    });
});