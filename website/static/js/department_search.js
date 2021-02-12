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

function getCsrfToken() {
    return getCookie('csrftoken');
}

function clearAndDisableList(element_id, default_option) {
    let element = document.getElementById(element_id);
    if (!element) return;
    clearOptions(element);
    let option = document.createElement('option');
    option.textContent = default_option;
    element.disabled = true;
    element.style.backgroundColor = '#d3d3d3';
    element.appendChild(option);
}

function clearOptions(element) {
    while (element.lastChild) {
        element.removeChild(element.lastChild);
    }
}

function clearAndDisableAllLists() {
    clearAndDisableList("id_department", "Выберите факультет");
    clearAndDisableList("id_chair", "Выберите кафедру");
    clearAndDisableList("id_program", "Выберите программу обучения");
    clearAndDisableList("id_subject", "Выберите дисциплину");
}

function loadUniversities() {
    return loadOptions("id_university", "/api/universities/", null, "Выберите университет");
}

function loadOptions(elementId, endpointUrl, changedElementValue, defaultOptionText) {
    let element = document.getElementById(elementId);
    if (!element) return;

    let request = new Request(`${endpointUrl}?id=${changedElementValue}`, {
        method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        }),
    });
    return fetch(request)
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Response.error();
            }
        })
        .then(function (jsonArray) {
            clearOptions(element);
            if (jsonArray.length !== 0) {
                let option = document.createElement("option");
                option.textContent = defaultOptionText;
                option.value = "";
                option.disabled = (elementId !== 'id_subject');
                element.appendChild(option);
                element.value = "";

                let lastSemester = null;
                jsonArray.forEach(function (item) {
                    if (elementId === 'id_subject') {
                        if (lastSemester !== item.semester) {
                            let lineSplitter = document.createElement("option");
                            lineSplitter.textContent = "____________________";
                            lineSplitter.disabled = true;
                            element.appendChild(lineSplitter);

                            let headingSplitter = document.createElement("option");
                            headingSplitter.disabled = true;
                            if (item["semester"] > 0) {
                                headingSplitter.textContent = `Семестр ${item.semester}`;
                            } else {
                                headingSplitter.textContent = "Общие дисциплины";
                            }
                            headingSplitter.style.fontFamily = "bold";
                            element.appendChild(headingSplitter);
                            lastSemester = item.semester;
                        }
                    }
                    let option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.title;
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
        });
}

function setOption(elementId, newValue) {
    let element = document.getElementById(elementId);
    if (element && element.value.toString() !== (newValue || '').toString()) {
        element.value = newValue;
        return true;
    } else {
        return false;
    }
}

/*
 * Change hooks
 */

function universityChanged(university_id) {
    return loadOptions("id_department", "/api/departments/", university_id, "Выберите факультет")
        .then(() => {
            clearAndDisableList("id_chair", "Выберите кафедру");
            clearAndDisableList("id_program", "Выберите программу обучения");
            clearAndDisableList("id_subject", "Выберите дисциплину");
            return Promise.resolve();
        });
}

function departmentChanged(department_id) {
    return loadOptions('id_chair', '/api/chairs/', department_id, 'Выберите кафедру')
        .then(() => {
            clearAndDisableList("id_program", 'Выберите программу обучения');
            clearAndDisableList("id_subject", "Выберите дисциплину");
            return Promise.resolve();
        });
}

function chairChanged(chair_id) {
    return loadOptions('id_program', '/api/programs/', chair_id, 'Выберите программу обучения')
        .then(() => {
            clearAndDisableList('id_subject', 'Выберите дисциплину');
            return Promise.resolve();
        });
}

function programChanged(program_id) {
    return loadOptions('id_subject', '/api/subjects/', program_id, 'Любая дисциплина');
}

/*
 * Setters
 */

function setUniversity(university_id) {
    if (setOption('id_university', university_id)) {
        return universityChanged(university_id);
    } else return Promise.resolve();
}

function setDepartment(department_id) {
    if (setOption('id_department', department_id)) {
        return departmentChanged(department_id);
    } else return Promise.resolve();
}

function setChair(chair_id) {
    if (setOption('id_chair', chair_id)) {
        return chairChanged(chair_id);
    } else return Promise.resolve();
}

function setProgram(program_id) {
    if (setOption('id_program', program_id)) {
        return programChanged(program_id);
    } else return Promise.resolve();
}

function setSubject(id) {
    setOption('id_subject', id);
    return Promise.resolve();
}
