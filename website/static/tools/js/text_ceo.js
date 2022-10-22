const SESSION_TEXT_KEY = 'picloud_text_ceo';

document.addEventListener("DOMContentLoaded", () => {
    let saved_text = sessionStorage.getItem(SESSION_TEXT_KEY);
    $('.ui.checkbox').checkbox();
    if (saved_text) {
        document.getElementById('main_text_area').value = saved_text;
    }
    document.getElementById('main_text_area').oninput = () => {
        analyze_text();
    }
    analyze_text();
});

function analyze_text() {
    let text = document.getElementById('main_text_area').value;
    sessionStorage.setItem(SESSION_TEXT_KEY, text);

    display_statistics(document.getElementById('ceo_container'), text);
    draw_words_cloud(document.getElementById('words_cloud_container'), text);
}

function display_statistics(container, text) {
    let symbols = text.length;
    let spaces = text.split(/[\t\s]/g).length - 1;
    let words = text.split(/[\t\s]+/g).length - 1;
    let paragraphs = text.split(/[\n]+/g).length - 1;

    container.innerHTML = `
        <div class="ui stackable center aligned grid">
            <div class="four wide column">
                <div class="ui statistic segment">
                    <div class="value">
                        <i class="ui font icon" style="color: #5ba9fd"></i>
                        <span id="invitations_subscribers">${symbols}</span>
                    </div>
                    <div class="label">Symbols</div>
                </div>
            </div>
            <div class="four wide column">
            <div class="ui statistic segment">
                <div class="value">
                    <i class="ui file outline icon" style="color: #5ba9fd"></i>
                    <span id="1_day_reminder">${spaces}</span>
                </div>
                <div class="label">Spaces</div>
            </div>
            </div>
            <div class="four wide column">
            <div class="ui statistic segment">
                <div class="value">
                    <i class="ui wikipedia w icon" style="color: #5ba9fd"></i>
                    <span id="30_mins_reminder">${words}</span>
                </div>
                <div class="label">Words</div>
            </div>
            </div>
            <div class="four wide column">
            <div class="ui statistic segment" title="Registrations based on Google Analytics statistics">
                <div class="value">
                    <i class="ui paragraph icon" style="color: #5ba9fd"></i>
                    <span id="unique_registrations_stat">${paragraphs}</span>
                </div>
                <div class="label">Paragraphs</div>
            </div>
            </div>
        </div>
    `;
}

function draw_words_cloud(container, text) {
    let words = text.split(/[\t\s]+/g);
    let words_cloud = {};
    for (let word of words) {
        let norm_word = word.toUpperCase()
            .replace('.', '')
            .replace(',', '')
            .replace(':', '')
            .replace(';', '')
            .replace('!', '')
            .replace('?', '');
        if(!words_cloud[norm_word]) {
            words_cloud[norm_word] = 1;
        } else {
            words_cloud[norm_word] += 1;
        }
    }
    let words_count = [];
    for (let word in words_cloud) {
        words_count.push([word, words_cloud[word]])
    }
    WordCloud(container, {
        list: words_count,
        weightFactor: document.getElementById('weight_factor').value,
        shuffle: document.getElementById('shuffle').checked,
        rotateRatio: 0,
    });
}


function do_command(command) {
    let textarea = document.getElementById(`main_text_area`);
    textarea.select();
    textarea.setSelectionRange(0, 99999);
    if (command === 'copy') {
        document.execCommand(command);
    } else if (command === 'clear') {
        textarea.value = '';
    }
    analyze_text();
}

async function paste() {
    document.getElementById(`main_text_area`).value = await navigator.clipboard.readText();
    analyze_text();
}
