let converter = new showdown.Converter();

$(document).ready(function () {
   update_markdown();
});

function update_markdown() {
     $(".post-text").each(function () {
        let text = $(this).text().replace(/^\s+|\s+$/g, '');
        $(this).html(converter.makeHtml(text));
    });
}

$("#markdownLive").html(converter.makeHtml($("textarea").val()));
$("textarea").bind('input propertychange', function() {
        $("#markdownLive").html(converter.makeHtml($("textarea").val()));
});
