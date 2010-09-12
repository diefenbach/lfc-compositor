$(function() {
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
})