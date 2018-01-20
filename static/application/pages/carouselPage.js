var carouselPage = {
    base_url: '/application/carousel/',
    album_url: '/application/album/',
    category_url: '/application/category/',
    fields: { album_id: 0, carousel: [], m_order: 0 },
    setFields: function () { $("[name='album']").selectpicker('val', carouselPage.fields.album_id); $("[name='carousel']").selectpicker('val', carouselPage.fields.carousel); },
    resetFields: function () { carouselPage.fields = { album_id: 0, carousel: [], m_order: 0 }; carouselPage.setFields(); },

    save: function () {
        viewer.sendRequest({
            url: carouselPage.base_url,
            method: "POST",
            data: carouselPage.fields,
            success: function (resp) {
                viewer.alert(resp.message, "success");
                carouselPage.resetFields();
            },
            error: function () {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },

    change_order: function () {
        viewer.sendRequest({
            url: carouselPage.base_url,
            method: "PUT",
            data: carouselPage.fields,
            success: function (resp) {
                viewer.alert(resp.message, "success");
                carouselPage.resetFields();
            },
            error: function () {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },

    delete: function () {

    },

    getCarousel: function (type) {
        viewer.sendRequest({
            url: carouselPage.category_url,
            method: "GET",
            data: { carousal: 1, type: type },
            success: function (resp) {
                resp.data.forEach(function (item) {
                    var option = "<option value='" + item.id + "'>" + item.name + "</option>";
                    $("[name='carousel']").append(option);
                });
                $("[name='carousel']").selectpicker();
            },
            error: function (errResp) {
                console.log(errResp);
            }
        });
    },

    getAlbum: function () {
        viewer.sendRequest({
            url: carouselPage.album_url,
            method: "GET",
            success: function (resp) {
                resp.data.forEach(function (item) {
                    var option = "<option value='" + item.id + "'>" + item.name + "</option>";
                    $("[name='album']").append(option);
                });
                $("[name='album']").selectpicker();
            }
        });
    }
};

$(document).ready(function () {
    $("[name='btn_album']").on("click", function () {
        $(".bs-example-modal-lg-mAlbum").modal({ show: true });
    });
    $("[name='btn_track']").on("click", function () {
        $(".bs-example-modal-lg-mTrack").modal({ show: true });
    });
    $("[name='btn_video']").on("click", function () {
        $(".bs-example-modal-lg-mVideo").modal({ show: true });
    });
});