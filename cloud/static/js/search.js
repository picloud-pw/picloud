function post_to_html(post) {
    let request = new XMLHttpRequest();
    request.open('GET', '/post/' + post.id + '/render/', false);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.send();
    return request.responseText;
}

function update_post_list(posts) {
    let search_results = document.getElementById("search_results");
    while (search_results.lastChild) search_results.removeChild(search_results.lastChild);
    if (search_results.querySelector('.post') === null) {
        $('#search_results').append("");
    } else {
        posts.forEach(function (item, i, arr) {
            $('#search_results').append(post_to_html(item));
        });
    }
}

function get_element_value_if_enabled(element_id) {
    let subject_elem = document.getElementById(element_id);
    return subject_elem.disabled === false ? subject_elem.value : null;
}

function get_current_values() {
    let university_id = get_element_value_if_enabled('id_university');
    let department_id = get_element_value_if_enabled('id_department');
    let chair_id = get_element_value_if_enabled('id_chair');
    let program_id = get_element_value_if_enabled('id_program');
    let subject_id = get_element_value_if_enabled('id_subject');
    let type_id = get_element_value_if_enabled('id_type');
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

// FIXME: copied from post_edit
function setSubject(id) {
    setOption('id_subject', id);
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
    new_search_request(data);
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

function new_search_request(data) {
    search(data.subject_id, data.type_id);
}

[
    document.getElementById('id_subject'),
    document.getElementById('id_type'),
].forEach(element => {
    element.addEventListener('change', function () {
        let data = get_current_values();
        history.pushState(data, null, `/search/?${calculateSuffix(data)}`);
        new_search_request(data);
    });
});

function search_posts() {
    let search_request = $("#search-line").find("input").val().toLowerCase();
    $.ajax({
        url: "/api/search_posts/",
        data: {"search_request": search_request},
        dataType: 'json',
        success: function (data) {
            $("#search_results").innerHTML = data;
        }
    });
}
