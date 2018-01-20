var TrackPage = {
    base_url: '/application/track/',
    album_url: '/application/album/',
    video_url: '/application/video/',
    fields: {
        id: 0,
        name: "",
        album: [],
        video_id: [],
    },
    setFields: function () {
        $("[name='name']").val(TrackPage.fields.name);
        $("[name='cover_image']").val(null);
        $("[name='mp3_url']").val(null);
        $("[name='album']").selectpicker('val', TrackPage.fields.album);
        $("[name='video_lst']").html("");
        TrackPage.fields.video_id.forEach(function (item) {
            var li = "<li>" + item.name + " | <button class='btn btn-small btn-danger' onclick='TrackPage.removeVideo(" + TrackPage.fields.id + ", " + item.id + ")'>&times;</button></li>";
            $("[name='video_lst']").append(li);
        });
    },
    resetFields: function () {
        TrackPage.fields = {
            id: 0,
            name: "",
            album: [],
            video_id: [],
        };
        TrackPage.setFields();
    },
    getData: function (id) {
        viewer.sendRequest({
            url: TrackPage.base_url,
            method: 'GET',
            data: {
                id: id
            },
            success: function (resp) {
                var album = [];
                var videos = [];
                resp.data.album.forEach(function (item) {
                    album.push(item.id);
                });
                TrackPage.fields = {
                    id: resp.data.id,
                    name: resp.data.name,
                    album: album,
                    video_id: resp.data.video,
                };
                TrackPage.setFields();
            },
            error: function (errResp) {
                console.log(errResp);
            }
        });
    },
    save: function () {
        var method = "POST";
        if (TrackPage.fields.id > 0) {
            method = "PUT"
        }
        $("[name='btn_save']").data("loading-text", "saving.....");
        if (viewer.fileValidator([$("[name='mp3_url']"), $("[name='cover_image']")])) {
            viewer.sendRequest({
                url: TrackPage.base_url,
                method: method,
                data: TrackPage.fields,
                success: function (resp) {
                    if ($("[name='mp3_url']")[0].files[0] || $("[name='cover_image']")[0].files[0]) {
                        fd = new FormData();
                        fd.append("id", parseInt(resp.data));
                        if ($("[name='mp3_url']")[0].files[0]) {
                            fd.append("mp3_url", $("[name='mp3_url']")[0].files[0]);
                        }
                        if ($("[name='cover_image']")[0].files[0]) {
                            fd.append("cover_image", $("[name='cover_image']")[0].files[0]);
                        }
                        $("[name='btn_save']").data("loading-text", "uploading.....");
                        viewer.uploadFile({
                            url: TrackPage.base_url,
                            data: fd,
                            progress: function (evt) {
                                console.log(evt);
                            },
                            success: function () {
                                viewer.alert(resp.message, "success");
                                TrackPage.resetFields();
                            },
                            error: function (errResp) {
                                viewer.alert(errResp.responseJSON, "error");
                                TrackPage.resetFields();
                            }
                        });
                    } else {
                        viewer.alert(resp.message, "success");
                        TrackPage.resetFields();
                    }
                },
                error: function (errResp) {
                    viewer.alert(errResp.responseJSON, "error");
                }
            });
        }
    },
    delete: function (id) {
        viewer.sendRequest({
            url: TrackPage.base_url,
            method: "DELETE",
            data: {
                id: id
            },
            success: function (resp) {
                viewer.alert(resp.message, "success");
                TrackPage.fields = {
                    id: 0,
                    name: ""
                };
                TrackPage.setFields();
            },
            error: function (errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },
    addVideo: function (track_id, video_id) {
        viewer.sendRequest({
            method: "POST",
            url: TrackPage.base_url,
            data: {
                id: track_id,
                video_id: video_id
            },
            success: function (resp) {
                viewer.alert(resp.message, "success");
            },
            error: function (errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },

    removeVideo: function (track_id, video_id) {
        viewer.sendRequest({
            method: "REMOVE",
            url: TrackPage.base_url,
            data: {
                id: track_id,
                video_id: video_id
            },
            success: function (resp) {
                viewer.alert(resp.message, "success");
            },
            error: function (errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },
     getVideos: function (videos) {
        viewer.sendRequest({
            method: "GET",
            url: TrackPage.video_url,
            success: function (resp) {
                $("[name='video']").html("");
                resp.data.forEach(function (item) {
                    var option = "<option value='" + item.id + "'>" + item.name + "</option>";
                    $("[name='video']").append(option);
                });
            },
            error: function (errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },
};

$(document).ready(function () {
    $("[name='album']").search({
        url: TrackPage.album_url
    })
    $("[name='btn_reset']").on('click', function () {
        TrackPage.resetFields();
    });
    $("[name='btn_save']").on('click', function () {
        TrackPage.fields = {
            id: TrackPage.fields.id > 0 ? TrackPage.fields.id : 0,
            name: $("[name='name']").val(),
            album: $("[name='album']").next().children()
        };
        if (TrackPage.fields.album) {
            albumIds = "|";
            TrackPage.fields.album.forEach(function (item) {
                albumIds += "," + item;
            });
            TrackPage.fields.album = albumIds.replace("|,", "");
        }
        TrackPage.save();
    });
    $("[name='btn_edit']").on('click', function () {
        var id = $(this).data("id");
        TrackPage.getData(id);
    });

    $("[name='btn_delete']").on('click', function () {
        var id = $(this).data("id");
        TrackPage.delete(id);
    });

    $("[name='btn_add_video']").on('click', function(){
        var video_id = $("[name='video']").val();
        TrackPage.addVideo(TrackPage.fields.id, video_id);
    });

    $("[name='btn_video']").on("click", function () {
        $(".bs-example-modal-lg-mVideo").modal({
            show: true
        });
        TrackPage.getVideos();
    });
});