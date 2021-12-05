function format_subjects(container, subjects) {
    let subjects_list_id = random_ID()
    container.innerHTML = `
        <div class="ui divided relaxed list" id="${subjects_list_id}"></div>
    `;
    container = document.getElementById(subjects_list_id);
    for (let subject of subjects) {
        container.innerHTML += `
            <a class="item" style="cursor: pointer" href="/subjects?id=${subject['id']}">
                <i class="large bookmark outline middle aligned icon"></i>
                <div class="middle aligned content">
                  <div class="header">${subject['name']}</div>
                  <div class="description">
                    <i class="sticky note outline icon"></i> Posts - ${subject['posts']}
                  </div>
                </div>
            </a>
       `;
    }
}

function department_subjects_list(container, department_id) {
    container.innerHTML = `<div class="ui segment">${render_loader()}</div>`;
    axios.get(`/hierarchy/subjects/search?department_id=${department_id}`)
        .then((response) => {
            let subjects = response.data['subjects'];
            container.innerHTML = subjects.length ? '' : `
                <div class="ui segment">
                    ${render_placeholder(
                        'bookmark outline', 
                        'Looks like there is no subject on this level...'
                    )}
                </div>
            `;
            let semesters = {};
            for (let subject of subjects) {
                if (!semesters[subject['semester']]) {
                    semesters[subject['semester']] = [];
                }
                semesters[subject['semester']].push(subject);
            }
            for (let semester in semesters) {
                const container_id = random_ID();
                let subjects = semesters[semester];
                container.innerHTML += `
                    <div class="ui segment">
                        <div class="ui dividing header">Subjects – Semester ${semester}</div>
                        <div id="${container_id}"></div>
                    </div>
                `;
                format_subjects(document.getElementById(container_id), subjects);
            }
        })
}