$(document).ready(function(){
    clear_and_disabled_all_elements();
    get_all_universities();
});

function get_all_universities(){
    change_options("/get_universities/", 0, "id_university");
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

function change_options(url, id, element_id) {
    $.ajax({
        url: url,
        data: {'id': id},
        dataType: 'json',
        success: function (data) {
            clear_options(element_id);
            if (data.length !== 0){
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
                .css('background-color', '#FFCCCC')
                .append($('<option>', {text: "К сожалению список пуст"}));
            }
        }
    });
}

$("#id_university").change(function () {
    let university_id = $(this).val();
    change_options("/get_departments/", university_id, "id_department");
    clear_options_and_disabled("id_chair", "Выберите кафедру");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
});

$("#id_department").change(function () {
    let department_id = $(this).val();
    change_options("/get_chairs/", department_id, "id_chair");
    clear_options_and_disabled("id_program", "Выберите программу обучения");
    clear_options_and_disabled("id_subject", "Выберите предмет");
});

$("#id_chair").change(function () {
    let chair_id = $(this).val();
    change_options("/get_programs/", chair_id, "id_program");
    clear_options_and_disabled("id_subject", "Выберите предмет");
});

$("#id_program").change(function () {
    let program_id = $(this).val();
    change_options("/get_subjects/", program_id, "id_subject");
});