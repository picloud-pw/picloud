

export class Subjects {

    get_subjects_list() {
        return axios.get('/hierarchy/subjects/list');
    }

    create_subject(title) {
        let data = new FormData();
        data.append("title", title);
        return axios.post('/hierarchy/subjects/create', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}});
    }

    display_new_subject_modal(created_callback) {
        let modal_id = random_ID();
        let modal = $.modal({
            title: `Create new Subject`,
            closeIcon: true,
            class: 'mini',
            content: `
                <div id="${modal_id}">
                    <form class="ui form">
                        <div class="fluid field">
                            <label>Title</label>
                            <input type="text" id="${modal_id}_title" placeholder="New subject title...">
                        </div>
                    </form>
                </div>
            `,
            actions: [
                {
                    text: 'Create',
                    click: () => {
                        let title = document.getElementById(`${modal_id}_title`).value;
                        this.create_subject(title).then(response => {
                            created_callback(response);
                        }).catch((error) => {
                            show_alert('warning', error.response.data.error);
                        });
                    }
                },
            ],
        });
        modal.modal('show');
    }

}