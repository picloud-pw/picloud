document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

function restore_state() {
    display_student_search_page();
}

function display_student_search_page() {
    document.getElementById('students_container').innerHTML = `
        <div class="ui centered stackable grid">
            <div class="six wide computer ten wide tablet sixteen wide mobile column">
                <div class="ui segment">
                    <div class="ui dividing header">Filters</div>
                    <div id="filters_container"></div>
                </div>
                <div class="ui segment">
                    <div class="ui dividing header">Students</div>
                    <div id="students_list"></div>
                </div>
            </div>
        </div>
    `;

    init_students_filters(
        document.getElementById('filters_container'),
        document.getElementById('students_list'),
    );
}
