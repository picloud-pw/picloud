function get_all_universities() {
    change_options("/api/universities/", 0, "id_university", "Выберите университет");
}

function clear_options_and_disabled(element_id, default_option) {
    $('#' + element_id)
        .find('option')
        .remove()
        .end()
        .append($('<option>', {text: default_option}))
        .prop('disabled', true)
        .css('background-color', 'lightgray');
}

function clear_options(element_id) {
    $('#' + element_id).find('option').remove().end();
}

function clear_and_disabled_all_elements() {
    clear_options_and_disabled("id_department", "Выберите факультет");
    clear_options_and_disabled("id_chair", "Выберите кафедру");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
}

function change_options(url, id, element_id, default_option, changed_element) {
    $.ajax({
        url: url,
        data: {'id': id},
        dataType: 'json',
        success: function (data) {
            // FIXME: Костыль. Необходимо для автоматического заполнения полей
            $("#"+changed_element).val(id);
            clear_options(element_id);
            if (data.length !== 0) {
                $('#' + element_id).append($('<option>', {text: default_option, value: "", disabled: true, selected: true}));
                data.forEach(function (item, i, arr) {
                    $('#' + element_id).append($('<option>', {
                        value: item["id"],
                        text: item["title"]
                    }));
                });
                $('#' + element_id)
                    .prop('disabled', false)
                    .css('background-color', 'white');
            } else {
                $('#' + element_id)
                    .prop('disabled', true)
                    .css('background-color', '#FFCCCC')
                    .append($('<option>', {text: "К сожалению, список пуст"}));
            }
        }
    });
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
