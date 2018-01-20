var AlbumPage = {
    base_url: '/application/album/',
    category_url: '/application/category/',
    artist_url: '/application/artist/',
    video_url: '/application/video/',
    fields: {
        id: 0,
        name: "",
        release_date: "",
        category: -1,
        carousal: -1,
        artist: [],
        video_id: [],
        cover_image: undefined
    },
    setFields: function () {
        $("[name='name']").val(AlbumPage.fields.name);
        $("[name='release_date']").val(AlbumPage.fields.release_date);
        $("[name='category']").val(AlbumPage.fields.category);
        $("[name='carousal']").val(AlbumPage.fields.carousal);
        $("[name='artist']").next().html("");
        if (AlbumPage.fields.artist.length > 0){
            AlbumPage.fields.artist.forEach(function(item){
                var elem = "<span class='alert alert-info' data-id='" + item.id + "'>" + item.name + "<a href='#' name='term_remove'>&nbsp;&times;</a></span>";
                $("[name='artist']").next().append(elem);
                $("[name='term_remove']").on('click', function(){ $(this).parent().remove(); }); 
            });
        }
        
        
        $("[name='cover_image']").val(AlbumPage.fields.cover_image);
        $("[name='trailer_lst']").html("");
        AlbumPage.fields.video_id.forEach(function (item) {
            var li = "<li>" + item.name + " | <button class='btn btn-small btn-danger' onclick='AlbumPage.removeVideo(" + AlbumPage.fields.id + ", " + item.id + ")'>&times;</button></li>";
            $("[name='trailer_lst']").append(li);
        });
    },

    resetFields: function () {
        AlbumPage.fields = {
            id: 0,
            name: "",
            release_date: "",
            category: -1,
            carousal: -1,
            artist: [],
            video_id: [],
            cover_image: undefined
        };
        AlbumPage.setFields();
    },

    getData: function (id) {
        viewer.sendRequest({
            url: AlbumPage.base_url,
            method: 'GET',
            data: {
                id: id
            },
            success: function (resp) {
                var category = 0;
                var carousal = 0;
                var artist = [];
                var videos = [];
                resp.data.category.forEach(function (item) {
                    if (item.carousal) {
                        carousal = item.id;
                    } else {
                        category = item.id;
                    }
                });
                resp.data.artist.forEach(function (item) { artist.push({id: item.id, name: item.name}); });
                AlbumPage.fields = {
                    id: resp.data.id,
                    name: resp.data.name,
                    release_date: resp.data.release_date,
                    category: category,
                    carousal: carousal,
                    artist: artist,
                    video_id: resp.data.video,
                    cover_image: resp.data.cover_image,
                };
                AlbumPage.setFields();
            },
            error: function (errResp) {
                console.log(errResp)
            }
        });
    },

    save: function () {
        var method = "POST";
        if (AlbumPage.fields.id > 0) {
            method = "PUT"
        }
        $("[name='btn_save']").data("loading-text", "saving.....");
        if (viewer.fileValidator([$("[name='cover_image']")])) {
            viewer.sendRequest({
                url: AlbumPage.base_url,
                method: method,
                data: AlbumPage.fields,
                success: function (resp) {
                    if ($("[name='cover_image']")[0].files[0]) {
                        fd = new FormData();
                        fd.append("id", parseInt(resp.data));
                        fd.append("cover_image", $("[name='cover_image']")[0].files[0]);
                        $("[name='btn_save']").data("loading-text", "uploading.....");
                        viewer.uploadFile({
                            url: AlbumPage.base_url,
                            data: fd,
                            progress: function (evt) {
                                console.log(evt);
                            },
                            success: function () {
                                viewer.alert(resp.message, "success");
                                AlbumPage.resetFields();
                            },
                            error: function (errResp) {
                                viewer.alert(errResp.responseJSON, "error");
                                AlbumPage.resetFields();
                            }
                        })
                    } else {
                        viewer.alert(resp.message, "success");
                        AlbumPage.resetFields();
                    }
                },
                error: function (errResp) {
                    viewer.alert(errResp.responseJSON, "error");
                }
            });
        }
    },

    getVideos: function (videos) {
        viewer.sendRequest({
            method: "GET",
            url: AlbumPage.video_url,
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

    addVideo: function (album_id, video_id) {
        viewer.sendRequest({
            method: "POST",
            url: AlbumPage.base_url,
            data: {
                id: album_id,
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

    removeVideo: function (album_id, video_id) {
        viewer.sendRequest({
            method: "REMOVE",
            url: AlbumPage.base_url,
            data: {
                id: album_id,
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

    delete: function (id) {
        viewer.sendRequest({
            url: AlbumPage.base_url,
            method: "DELETE",
            data: {
                id: id
            },
            success: function (resp) {
                viewer.alert(resp.message, "success");
                AlbumPage.fields = {
                    id: 0,
                    name: ""
                };
                AlbumPage.setFields();
            },
            error: function (errResp) {
                viewer.alert(errResp.responseJSON, "error");
            }
        });
    },

    getCategory: function () {
        viewer.sendRequest({
            url: AlbumPage.category_url,
            method: "GET",
            data: {
                carousal: 0,
                type: 1
            },
            success: function (resp) {
                $("[name='category']").append("<option value='-1'> Select Category </option>");
                resp.data.forEach(function (item) {
                    var option = "<option value='" + item.id + "'>" + item.name + "</option>";
                    $("[name='category']").append(option);
                });
            },
            error: function (errResp) {
                console.log(errResp);
            }
        });
    },

    getCarousal: function () {
        viewer.sendRequest({
            url: AlbumPage.category_url,
            method: "GET",
            data: {
                carousal: 1,
                type: 1
            },
            success: function (resp) {
                $("[name='carousal']").append("<option value='-1'> Select Carousal </option>");
                resp.data.forEach(function (item) {
                    var option = "<option value='" + item.id + "'>" + item.name + "</option>";
                    $("[name='carousal']").append(option);
                });
            },
            error: function (errResp) {
                console.log(errResp);
            }
        });
    }
};


$(document).ready(function () {
    AlbumPage.getCategory();
    AlbumPage.getCarousal();
    // AlbumPage.getArtist();
    $("[name='artist']").search({ url: AlbumPage.artist_url });
    $("[name='btn_reset']").on('click', function () { AlbumPage.resetFields(); });
    $("[name='btn_save']").on('click', function () {
        AlbumPage.fields = {
            id: AlbumPage.fields.id > 0 ? AlbumPage.fields.id : 0,
            name: $("[name='name']").val(),
            release_date: $("[name='release_date']").val(),
            category: $("[name='category']").val(),
            carousal: $("[name='carousal']").val(),
            artist: $("[name='artist']").next().children(),
            cover_image: $("[name='cover_image']").val()
        };
        if (AlbumPage.fields.artist.length > 0) {
            artistIds = "|";
            $.each(AlbumPage.fields.artist, function(index, item){
                artistIds += "," + $(item).data("id");
            });
            AlbumPage.fields.artist = artistIds.replace("|,", "");
        }else{
            AlbumPage.fields.artist = "";
        }
        AlbumPage.save();
    });
      $("[name='btn_edit']").on('click', function() {
        var id = $(this).data("id");
        AlbumPage.getData(id);
    });

    $("[name='btn_delete']").on('click', function() {
        var id = $(this).data("id");
        AlbumPage.delete(id);
    });

    $("[name='btn_add_video']").on('click', function () {
        var video_id = $("[name='video']").val();
        AlbumPage.addVideo(AlbumPage.fields.id, video_id);
    });

    $("[name='btn_video']").on("click", function () {
        $(".bs-example-modal-lg-mVideo").modal({
            show: true
        });
        AlbumPage.getVideos();
    });
});