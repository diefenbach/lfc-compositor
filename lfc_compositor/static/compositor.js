$(function() {

    overlay = $("#overlay").overlay({
            closeOnClick: false,
            oneInstance: false,
            api:true,
            speed:1,
            expose: {color: '#222', loadSpeed:1 }
    });

    $(".cp-width").live("change", function() {
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

    $(".cp-link").live("click", function() {
        var url = $(this).attr("href");
        $.get(url, function(data) {
            var data = JSON.parse(data);
            console.log(data)
            for (var html in data["html"])
                $(data["html"][html][0]).html(data["html"][html][1]);

            if (data["close"])
                overlay.close();

            if (data["open"])
                overlay.load();
        })
        return false;
    });

    $(".cp-button").live("click", function() {
        $(this).parents("form:first").ajaxSubmit({
            success : function(data) {
                var data = JSON.parse(data);
                for (var html in data["html"])
                    $(data["html"][html][0]).html(data["html"][html][1]);

                if (data["close"])
                    overlay.close();

                if (data["open"])
                    overlay.load();

            }
        })
        return false;
    });

    // Delete dialog
    var compositor_delete_dialog = $("#cp-yesno").overlay({ closeOnClick: false, api:true, loadSpeed: 200, top: '25%', expose: {color: '#222', loadSpeed:100 } });

    $(".cp-delete-link").live("click", function() {
        $("#cp-delete-url").html($(this).attr("href"));
        compositor_delete_dialog.load();
        return false;
    });

    var buttons = $("#cp-yesno button").live("click", function(e) {
        compositor_delete_dialog.close();
        var yes = buttons.index(this) === 0;
        var url = $("#cp-delete-url").html();
        if (yes) {
            $.get(url, function(data) {
                $("#core-data-extra").html(data);
                overlay.close();
            });
        }
    });

})