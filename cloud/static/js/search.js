function postToHtml(post) {
    let request = new XMLHttpRequest();
    request.open('GET', '/post/' + post.id + '/render/', false);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.send();
    let html = request.responseText;
    return new DOMParser().parseFromString(html, 'text/xml');
}

function getElementValueIfEnabled(element_id) {
    let subject_elem = document.getElementById(element_id);
    return subject_elem.disabled === false ? subject_elem.value : null;
}

function getCurrentValues() {
    let university_id = getElementValueIfEnabled('id_university');
    let department_id = getElementValueIfEnabled('id_department');
    let chair_id = getElementValueIfEnabled('id_chair');
    let program_id = getElementValueIfEnabled('id_program');
    let subject_id = getElementValueIfEnabled('id_subject');
    let type_id = getElementValueIfEnabled('id_type');
    return {
        "university_id": university_id,
        "department_id": department_id,
        "chair_id": chair_id,
        "program_id": program_id,
        "subject_id": subject_id,
        "type_id": type_id,
    };
}

function setType(id) {
    setOption('id_type', id);
    return Promise.resolve();
}

window.addEventListener('popstate', event => {
    let data = event.state;
    if (!data) return;
    Promise.resolve()
        .then(() => setUniversity(data.university_id))
        .then(() => setDepartment(data.department_id))
        .then(() => setChair(data.chair_id))
        .then(() => setProgram(data.program_id))
        .then(() => setSubject(data.subject_id));
    document.getElementById("id_type").value = data.type_id;
    newSearchRequest(data);
});

function calculateSuffix(data) {
    let components = [];
    if (data.type_id) components.push(`type_id=${data.type_id ? data.type_id : ''}`);
    if (data.subject_id) components.push(`subject_id=${data.subject_id}`);
    return components.join('&');
}

function search(subject_id = undefined, type_id = undefined) {
    let data = {
        subject_id: subject_id,
        type_id: type_id,
    };
    let url = `/api/posts?${calculateSuffix(data)}`;
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            document.getElementById("search_results").innerHTML = request.responseText;
            // TODO: Найти лучший способ определения пустого результата
            if (document.getElementById("search_results").querySelector('.post')) {
                assignOnImageLoadedHooks();
            } else {
                let element = document.createElement('article');
                element.classList.add('post');
                let container = document.createElement('div');
                container.classList.add('post-container');
                container.textContent = 'К сожалению, по вашему запросу ничего не найдено :(';
                element.appendChild(container);
                document.getElementById("search_results").appendChild(element);
            }
            resizeAllPosts();
        } else {
            // TODO: Обработать ошибку, возвращённую сервером
        }
    };
    request.onerror = function () {
        // TODO: Обработать ошибку соединения
    };
    request.send(data);
}

function newSearchRequest(data) {
    search(data.subject_id, data.type_id);
}

ready(() => {
    [
        document.getElementById('id_subject'),
        document.getElementById('id_type'),
    ]
        .forEach(element => {
            element.addEventListener('change', function () {
                let data = getCurrentValues();
                history.pushState(data, null, `/search/?${calculateSuffix(data)}`);
                newSearchRequest(data);
            });
        });
});
