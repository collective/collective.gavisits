var url = window.location.href + '/@@update-visits-counter';

jQuery.ajax({type: 'POST',
             url: url,
             async : true,
             success: function(results){
                var new_val = results * 1;
                var old_val = $(".visits-counter > .visits-number").html() * 1;
                // * 1 is to make sure values are ints.

                if (new_val > old_val){
                    // Only update if returned value is bigger than existing one.
                    $(".visits-counter > .visits-number").html(new_val);   
                }

             }
});
