document.addEventListener("DOMContentLoaded", function () {

    init_universities_table();

});

function init_universities_table() {
    let container = document.getElementById('departments_container');
    container.classList.add('loading');
    axios.get(`/hierarchy/departments/search?parent_department_id=null`)
        .then((response) => {
            let universities = response.data['departments'];
            for (let u of universities) {
               container.innerHTML += `
                    <div class="item" style="cursor: pointer">
                        <img class="ui avatar image" src="${u['logo']}" alt="logo">
                        <div class="content">
                          <div class="header">${u['name']}</div>
                          <div class="description">${u['link']}</div>
                        </div>
                    </div>
               `;
            }

        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

