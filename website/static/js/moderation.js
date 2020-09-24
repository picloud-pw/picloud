document.addEventListener("DOMContentLoaded", function () {

    init_moderation_table();

});

function init_moderation_table() {
    let container = document.getElementById('moderation_container');
    container.classList.add('loading');

    axios.all([
        axios.get('/posts/search?is_approved=False'),
        axios.get('/hierarchy/departments/search?is_approved=False'),
        axios.get('/hierarchy/subjects/search?is_approved=False'),
    ])
        .then((response) => {
            console.log(response);
            let posts = response[0].data;
            let departments = response[1].data;
            let subjects = response[2].data;

            let table_id = random_ID();
            container.innerHTML = `<table class="ui celled table" id="${table_id}"></table>`;
            let table = $(`#${table_id}`).DataTable({
                responsive: true,
                bAutoWidth: false,
                paging: false,
                ordering: false,
                info: false,
                data: [],
                columns: [
                    {title: "Type"},
                    {title: "Name"},
                    {title: "Action"},
                ]
            });
            table.order([1, 'desc']).draw();
        })
        .finally(() => {
            container.classList.remove('loading');
        });
}
