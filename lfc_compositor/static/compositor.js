$(function() {
    
    overlay = $("#overlay").overlay({
            closeOnClick: false,
            oneInstance: false,
            api:true,
            speed:1,
            expose: {color: '#222', loadSpeed:1 }
    });
    
    $(".compositor-width").live("change", function() {
        var url = $(this).attr("data");
        var value = $(this).attr("value");
        $.post(url, { "width" : value }, function(data) {            
            $("#core-data-extra").html(data);
        });
    });
    
    $(".cp-hover").live("mouseover", function() {
        var id = $(this).attr("id");
        $("." + id).css("background-color", "#ddd");
    })

    $(".cp-hover").live("mouseout", function() {
        var id = $(this).attr("id");
        $("." + id).css("background-color", "transparent");        
    })
        
    $(".compositor-link").live("click", function() {
        var url = $(this).attr("href");
        $.post(url, function(data) {
            $("#core-data-extra").html(data);
        })        
        return false;
    });    

    $(".compositor-link-2").live("click", function() {
        var url = $(this).attr("href");
        $.get(url, function(data) {
            $("#overlay .content").html(data);
            overlay.load();
        })        
        return false;
    });    

    $(".compositor-form-button-2").live("click", function() {
        $(this).parents("form:first").ajaxSubmit({
            success : function(data) {
                $("#core-data-extra").html(data);
                overlay.close();
            }
        })
        return false;
    });    

    $(".compositor-form-button").live("click", function() {
        // show_ajax_loading();
        $(this).parents("form:first").ajaxSubmit({
            success : function(data) {
                $("#overlay .content").html(data);
                overlay.load();

                // hide_ajax_loading();
            }
        })
        return false;
    });    
    
    // Delete dialog
    var compositor_delete_dialog = $("#compositor-yesno").overlay({ closeOnClick: false, api:true, loadSpeed: 1, expose: {color: '#222', loadSpeed:1 } });

    $(".compositor-delete-link").live("click", function() {
        $("#compositor-delete-url").html($(this).attr("href"));
        compositor_delete_dialog.load();
        return false;
    });

    var buttons = $("#compositor-yesno button").live("click", function(e) {
        compositor_delete_dialog.close();
        var yes = buttons.index(this) === 0;
        var url = $("#compositor-delete-url").html();
        if (yes) {
            $.get(url, function(data) {
                $("#core-data-extra").html(data);
                overlay.close();
            });
        }
    });
    
})