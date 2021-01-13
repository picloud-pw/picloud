function header(post_id, order){
    let textarea = document.getElementById(`${post_id}_textarea`);
    if (order < 1) order = 1;
    if (order > 6) order = 6;

    let template = "\n" + "#".repeat(order) + " ";

    let startPos = textarea.selectionStart;
    let endPos = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, startPos)
            + template
            + textarea.value.substring(endPos, textarea.value.length);

    textarea.focus();
    textarea.selectionEnd = startPos + template.length;
}

function outline(post_id, type){
    let textarea = document.getElementById(`${post_id}_textarea`);

    let template = "";
    if (type === "bold") template = "**";
    if (type === "italic") template = "*";

    let startPos = textarea.selectionStart;
    let endPos = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, startPos)
            + template + textarea.value.substring(startPos, endPos) + template
            + textarea.value.substring(endPos, textarea.value.length);

    textarea.focus();
    textarea.selectionEnd = startPos + template.length;
}

function code_block(post_id, language){
    let textarea = document.getElementById(`${post_id}_textarea`);

    let template = "```";
    if (language === undefined)
        language = "";

    let startPos = textarea.selectionStart;
    let endPos = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, startPos)
            + "\n" + template + "\n" + language
            + textarea.value.substring(startPos, endPos)
            + "\n" + template + "\n"
            + textarea.value.substring(endPos, textarea.value.length);

    textarea.focus();
    textarea.selectionEnd = startPos + template.length + 2;

}

function list_item(post_id) {
    let textarea = document.getElementById(`${post_id}_textarea`);
    let template = "\n * List item";

    let startPos = textarea.selectionStart;
    let endPos = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, startPos)
            + template
            + textarea.value.substring(endPos, textarea.value.length);

    textarea.focus();
    textarea.selectionEnd = startPos + template.length;
}

function link_template(post_id, type){
    let textarea = document.getElementById(`${post_id}_textarea`);

    let prefix = "\n[Link](";
    if (type === 'image')
        prefix = "\n![Image](";

    let link = "https://google.com) \n";

    let startPos = textarea.selectionStart;
    let endPos = textarea.selectionEnd;
    if (startPos === endPos)
        textarea.value = textarea.value.substring(0, startPos) + prefix + link
                + textarea.value.substring(endPos, textarea.value.length);
    else
        textarea.value = textarea.value.substring(0, startPos)
                + prefix + textarea.value.substring(startPos, endPos) + ") \n"
                + textarea.value.substring(endPos, textarea.value.length);

    textarea.focus();
    textarea.selectionEnd = startPos + prefix.length + link.length - 1;
}

