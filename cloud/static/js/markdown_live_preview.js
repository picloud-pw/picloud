let converter = new showdown.Converter();

$("#markdownLive").html(converter.makeHtml($("textarea").val()));
$("textarea").bind('input propertychange', function () {
    $("#markdownLive").html(converter.makeHtml($("textarea").val()));
});
