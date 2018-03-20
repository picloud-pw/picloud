function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrf_token = getCookie('csrftoken');

function get_all_universities() {
    change_options("/api/universities/", 0, "id_university", "Выберите университет");
}

function clear_options_and_disabled(element_id, default_option) {
    let element = document.getElementById(element_id);
    if (!element) return;
    clear_options(element);
    let option = document.createElement('option');
    option.textContent = default_option;
    element.append(option);
    element.disabled = true;
    element.style.backgroundColor = 'lightgray';
}

function clear_options(element) {
    while (element.lastChild) {
        element.removeChild(element.lastChild);
    }
}

function clear_and_disabled_all_elements() {
    clear_options_and_disabled("id_department", "Выберите факультет");
    clear_options_and_disabled("id_chair", "Выберите кафедру");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
}

function change_options(url, id, element_id, default_option, changed_element_id) {
    let element = document.getElementById(element_id);
    if (!element) return;

    let request = new XMLHttpRequest();
    request.open('GET', url + '?id=' + id, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            let data = JSON.parse(request.responseText);
            // FIXME: Костыль. Необходимо для автоматического заполнения полей
            let changed_element = document.getElementById(changed_element_id);
            if (changed_element != null) {
                changed_element.value = id;
            }
            clear_options(element);
            if (data.length !== 0) {
                let option = document.createElement("option");
                option.textContent = default_option;
                option.value = "";
                option.disabled = true;
                element.appendChild(option);
                element.value = "";
                data.forEach(function (item) {
                    let option = document.createElement("option");
                    option.value = item["id"];
                    option.textContent = item["title"];
                    element.appendChild(option);
                });
                element.disabled = false;
                element.style.backgroundColor = 'white';
            } else {
                element.style.backgroundColor = '#FFCCCC';
                let option = document.createElement('option');
                option.textContent = "К сожалению, список пуст";
                element.disabled = true;
                element.appendChild(option);
            }
        } else {
            // TODO: Обработать ошибку, возвращённую сервером
        }
    };
    request.onerror = function () {
        // TODO: Обработать ошибку соединения
    };
    request.send();
}


function university_updated(university_id) {
    change_options("/api/departments/", university_id, "id_department", "Выберите факультет", "id_university");
    clear_options_and_disabled("id_chair", "Выберите кафедру");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
}

function department_updated(department_id) {
    change_options("/api/chairs/", department_id, "id_chair", "Выберите кафедру", "id_department");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
}

function chair_updated(chair_id) {
    change_options("/api/programs/", chair_id, "id_program", "Выберите программу обучения", "id_chair");
    clear_options_and_disabled("id_subject", "Выберите предмет");
}

function program_updated(program_id) {
    change_options("/api/subjects/", program_id, "id_subject", "Выберите предмет", "id_program");
}
