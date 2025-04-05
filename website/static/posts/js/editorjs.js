import "https://cdn.jsdelivr.net/npm/@editorjs/editorjs@latest";
import "https://cdn.jsdelivr.net/npm/editorjs-drag-drop";

import "https://cdn.jsdelivr.net/npm/@editorjs/header@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/paragraph@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/quote@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/delimiter@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/list@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/marker@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/link@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/image@2.3.0";
import "https://cdn.jsdelivr.net/npm/@editorjs/code@2.9.3";
import "https://cdn.jsdelivr.net/npm/@editorjs/inline-code@latest";
import "https://cdn.jsdelivr.net/npm/@editorjs/attaches@latest";

import edjsParser from 'https://cdn.jsdelivr.net/npm/editorjs-parser@1.5.3/+esm';


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
        delimiter: Delimiter,
        list: {
            class: EditorjsList,
            inlineToolbar: true,
        },
        code: CodeTool,
        inlineCode: InlineCode,
        Marker: {
            class: Marker,
        },
        linkTool: {
          class: LinkTool,
          config: {
            endpoint: '/posts/editorjs/link_tool/',
          }
        },
        image: {
            class: ImageTool,
            config: {
                endpoints: {
                    byFile: '/posts/editorjs/file_upload/',
                    byUrl: '/posts/editorjs/image_by_url/',
                }
            }
        },
        attaches: {
            class: AttachesTool,
            config: {
                endpoint: '/posts/editorjs/file_upload/'
            }
        }
    }

    config = {
        tools: Object.assign({}, this.tools),
        readOnly: false,
        placeholder: 'Let`s write something awesome!',
        logLevel: 'ERROR',
    }

    editor = null;

    constructor(container, settings = {}) {
        this.container = container;
        this.editor = this.init_editor(settings['data']);
        this.on_change = settings['on_change'] ? settings['on_change'] : () => {
        };
    }

    init_editor(data) {
        let editor = new EditorJS(Object.assign({}, {
            holder: this.container.id,
            data: data,
            minHeight: 300,
            onChange: (api, event) => {
                this.on_change()
            },
            onReady: () => {
                new DragDrop(editor);
            },
        }, this.config));
        return editor;
    }

    save() {
        return this.editor.save();
    }

}


export class PostBodyParser {

    config = {

    }

    custom_parsers = {
        custom_block_name: (data, config) => {
            // parsing functionality
            // the config arg is user provided config merged with default config
            // return string
        },
        list: (data, config) => {
            const listStyle = data.style === "unordered" ? "ul" : "ol";
            const recursor = (items, listStyle) => {
                const list = items.map((item) => {
                    if (!item.content && !item.items) return `<li>${item}</li>`;

                    let nestedList = "";
                    if (item.items?.length) nestedList = recursor(item.items, listStyle);
                    if (item.content) return `<li>${item.content}${nestedList}</li>`;
                });

                return `<${listStyle}>${list.join("")}</${listStyle}>`;
            };
            return recursor(data.items, listStyle);
        },
        image: (data, config) => {
            return `
                <img style="width: 100%" src="${data['file']['url']}" alt="${data['caption']}">
            `;
        },
        linkTool: (data, config) => {
            let image = data.meta.image;
            return `
                <div class="link-tool">
                    <a class="link-tool__content link-tool__content--rendered" target="_blank" rel="nofollow noindex noreferrer" href="${data.link}">
                    ${image ? `<div class="link-tool__image" style="background-image: url(${image});"></div>` : ''}
                    <div class="link-tool__title">${data.meta.title ? data.meta.title : ''}</div>
                    <p class="link-tool__description">${data.meta.description ? data.meta.description : ''}</p>
                    <span class="link-tool__anchor">${data.link ? new URL(data.link).host : ''}</span></a>
                </div>
            `;
        },
        attaches: (data, config) => {
            function humanFileSize(bytes, si=false, dp=1) {
              const thresh = si ? 1000 : 1024;

              if (Math.abs(bytes) < thresh) {
                return [bytes, 'B'];
              }

              const units = si
                ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
                : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
              let u = -1;
              const r = 10**dp;
              do {
                bytes /= thresh;
                ++u;
              } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

              return [bytes.toFixed(dp), units[u]];
            }
            let [filesize, units] = humanFileSize(data.file.size);
            const color_map = {
                'pdf': '#ef0202',
                'docx': '#2a7acf',
                'doc': '#2a7acf',
                'ppt': '#d04423',
                'pptx': '#d04423',
                'rar': '#5aa512',
                'zip': '#3e7807',
                'tar': '#93ed3a',
            }
            let extension = data.file.extension;
            let extension_color = color_map[extension] ? color_map[extension] : 'black';
            return `
                <div class="cdx-attaches cdx-attaches--with-file" style="margin-top: 14px">
                    <div class="cdx-attaches__file-icon" style="width: 50px; text-align: center; text-transform: uppercase; font-size: smaller;
                        border-radius: 10px; padding: 6px 0; margin-right: 10px; color: white; background-color: ${extension_color}">
                        <b>${extension}</b>
                    </div>
                    <div class="cdx-attaches__file-info">
                        <div class="cdx-attaches__title" contenteditable="false" data-placeholder="File title" data-empty="false">
                            ${data.title ? decodeURI(data.title) : decodeURI(data.file.name)}
                        </div>
                        <div class="cdx-attaches__size" data-size="${units}">${filesize}</div>
                    </div>
                    <a class="cdx-attaches__download-button" href="${data.file.url}" target="_blank" rel="nofollow noindex noreferrer" data-empty="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M7 10L11.8586 14.8586C11.9367 14.9367 12.0633 14.9367 12.1414 14.8586L17 10"></path>
                        </svg>
                    </a>
                </div>
            `;
        },
    }

    constructor() {
        this.parser = new edjsParser(this.config, this.custom_parsers);
    }

    parse(body) {
        return this.parser.parse(body);
    }

}
