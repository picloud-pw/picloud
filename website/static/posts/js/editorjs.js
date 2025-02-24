

export class PostBodyEditor {

    tools = {
        header: {
            class: Header,
            inlineToolbar: true,
            placeholder: 'Enter a header',
            levels: [2, 3, 4],
        },
        paragraph: {
            class: Paragraph,
            inlineToolbar: true,
        },
        quote: {
            class: Quote,
            inlineToolbar: true,
        },
        image: {
            class: ImageTool,
            config: {
                endpoints: {
                    byFile: '/editorjs/image_upload/',
                    byUrl: '/editorjs/image_by_url/',
                }
            }
        },
        delimiter: Delimiter,
        list: EditorjsList,
        Marker: {
            class: Marker,
        },
    }

    config = {
        tools: Object.assign({}, {
            columns: {
                class: editorjsColumns,
                config: {
                    EditorJsLibrary: EditorJS,
                    tools: this.tools
                }
            },
        }, this.tools),
        readOnly: false,
        placeholder: 'Let`s write something awesome!',
        logLevel: 'ERROR',
    }

    editor = null;

    constructor(container, settings={}) {
        this.container = container;
        this.editor = this.init_editor(settings['data']);
        this.on_change = settings['on_change'] ? settings['on_change'] : () => {};
    }

    init_editor(data) {
        let editor = new EditorJS(Object.assign({}, {
            holder: this.container.id,
            data: data,
            minHeight: 300,
            onChange: (api, event) => { this.on_change() },
            onReady: () => {
                new Undo({editor});
                new DragDrop(editor);
            },
        }, this.config));
        return editor;
    }

    save() {
        return this.editor.save();
    }

    render(body) {
        const parser = new edjsParser();
        return parser.parse(body);
    }

}
