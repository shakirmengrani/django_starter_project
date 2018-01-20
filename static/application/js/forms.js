$(document).ready(function () {
    $('.selectpicker').selectpicker();
});

// $(document).ready(function () {
  
    // // Select
    // $('.selectpicker').autocomplete().ajaxautocomplete({
    //     ajax: {
    //         method: 'GET',
    //         url: '/application/artist/?search=Shaan', 
    //         dataType: 'jsonp',
    //         success: function(data){
                
    //         }
    //     },
    //     locale: { emptyTitle: 'Select and Begin Typing' },
    //     preprocessData: function (data) {
    //         var i, l = data.length, arr = [];
    //         if (l) {
    //             for (i = 0; i < l; i++) {
    //                 if (data[i].Name.toLowerCase().indexOf(this.plugin.query) != -1 ||
    //                     data[i].Email.toLowerCase().indexOf(this.plugin.query) != -1) {
    //                     arr.push($.extend(true, data[i], { text: data[i].name, value: data[i].id, data: { subtext: data[i].name } }));
    //                 }
    //             }
    //         }
    //         return arr;
    //     }
    // });
//   $( '.selectpicker' ).autocomplete({
    
//     });
//   } );
   // $('.selectpicker').selectpicker('refresh');
    // Tags
    // $("#tags").tags({
    //   suggestions: ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india"],
    //   tagData: ["juliett", "kilo"]
    // });

    // // Editable
    // $('.editable').editable();

    // // Wizard
    // $('#rootwizard').bootstrapWizard();

    // // Mask
    // if ($('[data-mask]')
    //     .length) {
    //     $('[data-mask]')
    //         .each(function () {

    //             $this = $(this);
    //             var mask = $this.attr('data-mask') || 'error...',
    //                 mask_placeholder = $this.attr('data-mask-placeholder') || 'X';

    //             $this.mask(mask, {
    //                 placeholder: mask_placeholder
    //             });
    //         })
    // }
// });