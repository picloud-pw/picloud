$.uiAlert = (options) => {
    let timer;
    let alert_id = '_' + Math.random().toString(36).substr(2, 9);
    let setUI = $.extend({
        textHead: 'Default head text.',
        text: 'Default description.',
        classColor: '',
        bgColor: '',
        textColor: '',
        position: 'top-right',
        icon: 'info circle',
        time: 5,
        permanent: false,
    }, options);

    let ui_alert = `ui-alert-content-${setUI.position}`;
    if (!$(`body > .${ui_alert}`).length) {
        $(`body`).append(
            `<div class="ui-alert-content ${ui_alert}" style="width: inherit;"></div>`
        );
    }

    let style = `style="
        background-color: ${setUI.bgColor};
        color: ${setUI.textColor};
    "`;

    let message = $(
        `<div id="${alert_id}" class="ui ${setUI.classColor} icon message" ${style}>
            <i class="${setUI.icon} icon"/>
            <i id="${alert_id}_close" class="close icon"/>
            <div class="content">
                <div class="header">${setUI.textHead}</div>
                <p>${setUI.text}</p>
            </div>
        </div>`
    );

    $(`.${ui_alert}`).prepend(message);
    message.animate({
        opacity: '1',
    }, 300);
    if (setUI.permanent === false) {
        timer = 0;
        $(message).mouseenter(() => {
            clearTimeout(timer);
        }).mouseleave(() => {
            uiAlertHide();
        });
        uiAlertHide();
    }

    function uiAlertHide() {
        timer = setTimeout(() => {
            message.animate({
                opacity: '0',
            }, 300, function () {
                message.remove();
            });
        }, (setUI.time * 1000));
    }

    $(`#${alert_id}_close`)
        .on('click', () => {
            $(`#${alert_id}`).remove();
        })
    ;

};


function show_alert(type, message, time = 2) {
    let color_class = '';
    let icon = '';
    if (type === "success") {
        color_class = 'teal';
        icon = 'checkmark box';
    }
    if (type === "info") {
        color_class = 'blue';
        icon = 'info circle';
    }
    if (type === "warning") {
        color_class = 'yellow';
        icon = 'warning sign';
    }
    if (type === "error") {
        color_class = 'red';
        icon = 'remove circle';
    }

    $.uiAlert({
        textHead: type.charAt(0).toUpperCase() + type.slice(1),
        text: message,
        classColor: color_class,
        position: 'top-right',
        icon: icon,
        time: time,
    });
}