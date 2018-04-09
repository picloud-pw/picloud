let converter = new showdown.Converter();

function updateMarkdownPreview() {
    document.getElementById('markdownLive').innerHTML =
        converter.makeHtml(document.getElementById('id_text').value);
}

ready(updateMarkdownPreview);
document.getElementById('id_text').addEventListener('input', updateMarkdownPreview);
