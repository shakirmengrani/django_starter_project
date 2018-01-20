var videoPage = {
    base_url: '/application/video/',
    fields: { id: 0, name: "", isMpd: true },
    setFields: function() {
        $("[name='name']").val(videoPage.fields.name);
        $("[name='cover_image']").val(null);
        $("[name='isMpd']").prop("checked", videoPage.fields.isMpd);
        $("[name='mp4_url']").val(null);
    },
    resetFields: function() {
        videoPage.fields = { id: 0, name: "", isMpd: true };
        videoPage.setFields();
    },
    getData: function(id) {
        viewer.sendRequest({
            url: videoPage.base_url,
            method: 'GET',
            data: { id: id },
            success: function(resp) {
                videoPage.fields = { id: resp.data.id, name: resp.data.name, isMpd: true };
                videoPage.setFields();
            },
            error: function(errResp) { console.log(errResp); }
        });
    },
    save: function() {
        var method = "POST";
        if (videoPage.fields.id > 0) { method = "PUT" }
        $("[name='btn_save']").data("loading-text", "saving.....");
        if (viewer.fileValidator([$("[name='mp4_url']"), $("[name='cover_image']")])) {
            viewer.sendRequest({
                url: videoPage.base_url,
                method: method,
                data: videoPage.fields,
                success: function(resp) {
                    if ($("[name='mp4_url']")[0].files[0] || $("[name='cover_image']")[0].files[0]) {
                        fd = new FormData();
                        fd.append("id", parseInt(resp.data));
                        if ($("[name='mp4_url']")[0].files[0]) {
                            fd.append("mp4_url", $("[name='mp4_url']")[0].files[0]);
                        }
                        fd.append("isMpd", $("[name='isMpd']").prop("checked"));
                        if ($("[name='cover_image']")[0].files[0]) {
                            fd.append("cover_image", $("[name='cover_image']")[0].files[0]);
                        }
                        $("[name='btn_save']").data("loading-text", "uploading.....");
                        viewer.uploadFile({
                            url: videoPage.base_url,
                            data: fd,
                            progress: function(evt) { console.log(evt); },
                            success: function() {
                                viewer.alert(resp.message, "success");
                                videoPage.resetFields();
                            },
                            error: function(errResp) {
                                viewer.alert(errResp.responseJSON, "error");
                                videoPage.resetFields();
                            }
                        });
                    } else {
                        viewer.alert(resp.message, "success");
                        videoPage.resetFields();
                    }
                },
                error: function(errResp) { viewer.alert(errResp.responseJSON, "error"); }
            });
        }
    },
    delete: function(id) {
        viewer.sendRequest({
            url: videoPage.base_url,
            method: "DELETE",
            data: { id: id },
            success: function(resp) {
                viewer.alert(resp.message, "success");
                videoPage.fields = { id: 0, name: "" };
                videoPage.setFields();
            },
            error: function(errResp) { viewer.alert(errResp.responseJSON, "error"); }
        });
    }
};

$(document).ready(function() {
    $("[name='btn_save']").on('click', function() {
        videoPage.fields = {
            id: videoPage.fields.id > 0 ? videoPage.fields.id : 0,
            name: $("[name='name']").val(),
            isMpd: $("[name='isMpd']").prop("checked") 
        };
        videoPage.save();
    });
});