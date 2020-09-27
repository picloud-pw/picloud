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
            let data = [];
            for (let post of response[0].data) {
                data.push([
                    'Post',
                    post['title'],
                    '',
                ]);
            }
            for (let department of response[1].data) {
                data.push([
                    'Department',
                    `[${department['type']['name']}] ${department['name']}`,
                    '',
                ]);
            }
            for (let subject of response[2].data) {
                data.push([
                    'Subject',
                    subject['name'],
                    '',
                ]);
            }

            let table_id = random_ID();
            container.innerHTML = `<table class="ui selectable celled table" id="${table_id}"></table>`;
            let table = $(`#${table_id}`).DataTable({
                responsive: true,
                bAutoWidth: false,
                paging: false,
                info: false,
                data: data,
                columns: [
                    {title: "Type", width: "20%"},
                    {title: "Title", width: "60%"},
                    {title: "Action", width: "20%"},
                ]
            });
            table.order([1, 'desc']).draw();
        })
        .finally(() => {
            container.classList.remove('loading');
        });
}
