let TEXT_AREA = document.getElementById('id_text');

function header(order){
    if (order < 1) order = 1;
    if (order > 6) order = 6;

    let template = "\n" + "#".repeat(order) + " ";

    let startPos = TEXT_AREA.selectionStart;
    let endPos = TEXT_AREA.selectionEnd;
    TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos)
            + template
            + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);

    TEXT_AREA.focus();
    TEXT_AREA.selectionEnd = startPos + template.length;
    updateMarkdownPreview();
}

function outline(type){

    let template = "";
    if (type === "bold") template = "**";
    if (type === "italic") template = "*";

    let startPos = TEXT_AREA.selectionStart;
    let endPos = TEXT_AREA.selectionEnd;
    TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos)
            + template + TEXT_AREA.value.substring(startPos, endPos) + template
            + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);

    TEXT_AREA.focus();
    TEXT_AREA.selectionEnd = startPos + template.length;
    updateMarkdownPreview();
}

function code_block(language){

    let template = "```";
    if (language === undefined)
        language = "";

    let startPos = TEXT_AREA.selectionStart;
    let endPos = TEXT_AREA.selectionEnd;
    TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos)
            + "\n" + template + "\n" + language
            + TEXT_AREA.value.substring(startPos, endPos)
            + "\n" + template + "\n"
            + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);

    TEXT_AREA.focus();
    TEXT_AREA.selectionEnd = startPos + template.length + 2;
    updateMarkdownPreview();

}

function list_item() {
    let template = "\n * Запись";

    let startPos = TEXT_AREA.selectionStart;
    let endPos = TEXT_AREA.selectionEnd;
    TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos)
            + template
            + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);

    TEXT_AREA.focus();
    TEXT_AREA.selectionEnd = startPos + template.length;
    updateMarkdownPreview();
}

function link_template(type){

    let prefix = "\n[Ссылка](";
    if (type === 'image')
        prefix = "\n![Картинка](";

    let link = "https://google.com) \n";

    let startPos = TEXT_AREA.selectionStart;
    let endPos = TEXT_AREA.selectionEnd;
    if (startPos === endPos)
        TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos) + prefix + link
                + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);
    else
        TEXT_AREA.value = TEXT_AREA.value.substring(0, startPos)
                + prefix + TEXT_AREA.value.substring(startPos, endPos) + ") \n"
                + TEXT_AREA.value.substring(endPos, TEXT_AREA.value.length);

    TEXT_AREA.focus();
    TEXT_AREA.selectionEnd = startPos + prefix.length + link.length - 1;
    updateMarkdownPreview();
}

