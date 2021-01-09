document.addEventListener("DOMContentLoaded", function () {

    load_post_types();
    init_page();

});

function init_page() {

    init_departments_search((result, response) => {
        $("input[name='department_id']").val(result['department_id']);
        display_department_hierarchy(
            document.getElementById('department_hierarchy'),
            result['department_id']
        );
        init_subjects_list(result['department_id']);
    })
}


function load_post_types() {
    let select = document.getElementById('post_type');
    select.innerText = '';
    axios.get('/posts/types/get')
        .then(response => {
            let types = response.data['types'];
            for (let type of types) {
                select.innerHTML += `
                    <option value="${type['title']}">${type['title']}</option>
                `;
            }
            $('#post_type').dropdown();
        })

}


function init_subjects_list(department_id) {
    let select = document.getElementById('subject');
    select.innerText = '';
    axios.get(`/hierarchy/subjects/search?department_id=${department_id}`)
        .then(response => {
            let subjects = response.data['subjects'];
            for (let s of subjects) {
                select.innerHTML += `
                    <option value="${s['id']}">
                        ${s['name']} (sem. ${s['semester'] ? s['semester'] : '---'})
                    </option>
                `;
            }
            $('#subject').dropdown();
        })
}


function submit_form() {

}
