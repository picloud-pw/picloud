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
            for (let post of response[0].data['posts']) {
                data.push([ 'Post', `<a href="/posts?id=${post['id']}" target="_blank">${post['title']}</a>`, `
                    <div class="ui basic mini button" onclick="do_action(this, 'posts', 'approve', ${post['id']})">approve</div>
                    <div class="ui basic mini button" onclick="do_action(this, 'posts', 'delete', ${post['id']})">delete</div>
                `,]);
            }
            for (let department of response[1].data['departments']) {
                data.push([ 'Department', `[${department['type']['name']}] ${department['name']}`, `
                    <div class="ui basic mini button" onclick="do_action(this, 'hierarchy/departments', 'approve', ${department['id']})">approve</div>
                    <div class="ui basic mini button" onclick="do_action(this, 'hierarchy/departments', 'delete', ${department['id']})">delete</div>
                `]);
            }
            for (let subject of response[2].data['subjects']) {
                data.push(['Subject', subject['name'], `
                    <div class="ui basic mini button" onclick="do_action(this, 'hierarchy/subjects', 'approve', ${subject['id']})">approve</div>
                    <div class="ui basic mini button" onclick="do_action(this, 'hierarchy/subjects', 'delete', ${subject['id']})">delete</div>
                `,]);
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

function do_action(btn, model, action, id) {
    btn.classList.add('loading');
    let data = new FormData();
    data.append("id", id);
    axios.post(`/${model}/${action}`, data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            btn.parentElement.parentElement.remove();
        })
        .catch((error) => {
            show_alert('warning', error.response.data)
        })
}
