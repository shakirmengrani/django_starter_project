var viewer = {
    requestButton: null,
    pageinate: {
        next_number: 2,
        prev_number: 1
    },
    alert: function(str, type) {
        if (typeof(str) == 'object' && str.invalid !== undefined) {
            var list = "<ul>";
            $.each(str.invalid, function(index, item) { list += "<li>" + item + "</li>"; });
            list += "</ul>";
            str = list;
        }
        var n = noty({ layout: 'topRight', theme: 'relax', text: str, type: type, maxVisible: 5 });
    },
    sendRequest: function(options) {
        $.ajax(options.url, {
            method: options.method,
            data: options.data,
            beforeSend: function(xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) { xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken')); }
                viewer.requestButton = $("[name='btn_save']").button('loading');
            },
            success: options.success,
            error: options.error,
            complete: function() {
                if (viewer.requestButton) {
                    viewer.requestButton.button('reset');
                    $("[name='btn_save']").data('loading-text', 'loading.....');
                    viewer.requestButton = null;
                }
            }
        });
    },
    fileValidator: function(files) {
        isValid = false;
        files.forEach(function(item) {
            if ($(item)[0].files.length > 0) {
                switch ($(item).attr("name")) {
                    case "mp3_url":
                        if ($(item)[0].files[0].type == "audio/mp3") {
                            isValid = true;
                        } else {
                            isValid = false;
                            viewer.alert("Invalid mp3 file!", "error");
                        }
                        break;
                    case "cover_image":
                        if ($(item)[0].files[0].type == "image/jpeg") {
                            isValid = true;
                        } else {
                            isValid = false;
                            viewer.alert("Invalid cover image!", "error");
                        }
                        break;
                    case "mpd_url":
                        if ($(item)[0].files[0].type == "video/mp4") {
                            isValid = true;
                        } else {
                            isValid = false;
                            viewer.alert("Invalid mpd file!", "error");
                        }
                        break;
                    case "mp4_url":
                        if ($(item)[0].files[0].type == "video/mp4") {
                            isValid = true;
                        } else {
                            isValid = false;
                            viewer.alert("Invalid mp4 file!", "error");
                        }
                        break;
                    default:
                        isValid = false;
                        viewer.alert("file type doesn't exists!", "error");
                        break;
                }
            }
        });
        return isValid;
    },
    uploadFile: function(options) {
        $.ajax(options.url, {
            method: "POST",
            data: options.data,
            beforeSend: function(xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
                }
                viewer.requestButton = $("[name='btn_save']").button('loading');
            },
            xhr: function() { // custom xhr
                myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) { // if upload property exists
                    myXhr.upload.addEventListener('progress', function(evt) {
                        console.log(evt);
                    }, false); // progressbar                    
                }
                return myXhr;
            },
            enctype: 'multipart/form-data',
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: options.success,
            error: options.error,
            complete: function() {
                if (viewer.requestButton) {
                    viewer.requestButton.button('reset');
                    $("[name='btn_save']").data('loading-text', 'loading.....');
                    viewer.requestButton = null;
                }
            }
        });
    },
    page: function(option){
        viewer.sendRequest({
            method: "GET",
            url: option.url,
            success: option.success,
            error: function(errResp){
                console.log(errResp);
            }
        });
    }
}