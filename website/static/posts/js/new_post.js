document.addEventListener("DOMContentLoaded", function () {

    load_post_types();
    init_page();

});

function init_page() {
    init_departments_search((result, response) => {
            $("input[name='department_id']").val(result['department_id']);
            display_department_hierarchy(
                document.getElementById('search_department_hierarchy'),
                result['department_id']
            );
        })
    display_department_hierarchy(container, department_id)
}

function load_post_types() {
    let select = document.getElementById('post_type');
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

