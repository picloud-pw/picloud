let converter = new showdown.Converter();

$(document).ready(function () {
    $(".post-text").each(function () {
        let text = $(this).text().replace(/^\s+|\s+$/g, '');
        $(this).html(converter.makeHtml(text));
    });
});

$("#isMarkdownLive").click(function () {
    if (this.checked) {
        $("#markdownLive").html(converter.makeHtml($("textarea").val()));
        $("#markdownLive").css({'display': 'block'});
    }
    else {
        $("#markdownLive").css({'display': 'none'});
    }
});



