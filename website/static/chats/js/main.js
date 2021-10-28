document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

function restore_state() {
    init_chat_lists_segment();
    init_chat_content_segment();
    init_chat_bar_segment();
}

function init_chat_lists_segment() {
    load_chat_lists();
    document.getElementById('chat_list').innerHTML = `
        <div class="ui top segment"></div>
    `;
}

function init_chat_content_segment() {
    document.getElementById('chat_content').innerHTML = `
        <div class="ui top segment"></div>
        <div class="ui bottom segment"></div>
    `;
}

function init_chat_bar_segment() {
    document.getElementById('chat_bar').innerHTML = `
        <div class="ui top segment"></div>
    `;
}

function load_chat_lists() {

}
