jQuery.fn.search = function (options, callback) {
    var $elem = $(this[0]);
    var args = options || {};
    function split(val) { return val.split(/,\s*/); }
    function extractLast(term) { return split(term).pop(); }
    jQuery($elem).on("keydown", function (event) {
        if (event.keyCode === $.ui.keyCode.TAB &&
            $(this).autocomplete("instance").menu.active) {
            event.preventDefault();
        }
    }).autocomplete({
        source: function (request, response) {
            $.getJSON(options.url, {
                term: extractLast(request.term)
            }, function(data){
                return response(data.data);
            });
        },
        search: function () {
            var term = extractLast(this.value);
            if (term.length < 2) {
                return false;
            }
        },
        focus: function () {
            return false;
        },
        select: function (event, ui) {
            var term_elem = "<span class='alert alert-info' data-id='" + ui.item.id + "'>" + ui.item.value + "<a href='#' name='term_remove'>&nbsp;&times;</a></span>";
            $(this).next().append(term_elem);
            $("[name='term_remove']").on('click', function(){ $(this).parent().remove(); });
            this.value = "";
            return false;
        }
    });
    if (typeof callback == 'function') { callback.call(this); }
    return $elem;
};