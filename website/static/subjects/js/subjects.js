function department_subjects_list(container, department_id) {
    container.innerHTML = `
        <div class="ui divided relaxed list" id="subjects_list">
            ${render_loader()}
        </div>
    `;
    container = document.getElementById('subjects_list');
    axios.get(`/hierarchy/subjects/search?department_id=${department_id}`)
        .then((response) => {
            let subjects = response.data['subjects'];
            container.innerHTML = subjects.length ? '' :
                render_placeholder('bookmark outline', 'Looks like there is no subject on this level...');
            for (let s of subjects) {
                console.log(s);
                container.innerHTML += `
                    <a class="item" style="cursor: pointer" href="/subjects?id=${s['id']}">
                        <i class="large bookmark outline middle aligned icon"></i>
                        <div class="middle aligned content">
                          <div class="header">${s['name']}</div>
                          <div class="description">
                            Semester – ${s['semester'] ? s['semester'] : '---'} •  
                            <i class="sticky note outline icon"></i> ${s['posts']}
                          </div>
                        </div>
                    </a>
               `;
            }
        })
}