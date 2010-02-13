$(function() {
    var overlay = $("#composite-dialog").overlay({ closeOnClick: false, api:true, speed:100, expose: {color: '#eee', loadSpeed:100 } });
    $("a.compositor-edit").click(function() {
        var url = $(this).attr("href");
        $.get(url, function(data) {
            $("#composite-dialog").html(data)
            overlay.load();
        })

        return false;
    });
})