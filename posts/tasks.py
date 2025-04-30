import mistune

from posts.models import Post
from posts.views.editorjs import get_link_preview


class PostMigrator:

    def migrate_all_posts_body(self):
        for post in Post.objects.all():
            print(post.id)
            tokens = self.get_tokens_tree(post.text)

            blocks = self.parse_tokens_to_blocks(tokens)

            if post.link is not None and len(post.link) > 5:
                link_block = self.parse_link_to_block(post)
                blocks.append(link_block)

            if post.image and hasattr(post.image, 'url'):
                image_block = self.parse_image_to_block(post)
                blocks.append(image_block)

            if post.file and hasattr(post.file, 'url'):
                file_block = self.parse_file_to_block(post)
                if file_block is not None:
                    blocks.append(file_block)

            post.ejs_body = self.generate_ejs_body(post, blocks)
            post.save()

    def get_tokens_tree(self, mkd_text):
        mistune_tokenizer = mistune.create_markdown(renderer='ast')
        return mistune_tokenizer(mkd_text)

    def parse_token(self, token, parent_token=None):
        block = dict()
        token_type = token['type']

        # just skip
        if token_type == 'blank_line':
            return None

        # inline tools
        if token_type == 'softbreak':
            return " "

        if token_type == 'linebreak':
            return " "

        if token_type == 'text':
           return token['raw']

        if token_type == 'strong':
            strong_inline = ""
            if 'children' in token:
                for child in token['children']:
                    strong_inline += self.parse_token(child, token)
            return f"<b>{strong_inline}</b>"

        if token_type == 'emphasis':
            italic_inline = ""
            if 'children' in token:
                for child in token['children']:
                    italic_inline += self.parse_token(child, token)
            return f"<i>{italic_inline}</i>"

        if token_type == 'codespan':
            return f'<span class="inline-code">{token["raw"]}</span>'

        if token_type == 'link':
            link_text = ""
            if 'children' in token:
                for child in token['children']:
                    link_text += self.parse_token(child, token)
            return f'<a href="{token["attrs"]["url"]}">{link_text}</a>'

        # blocks
        if token_type == 'paragraph':
            block['type'] = 'paragraph'
            block['data'] = {
                'text': ''
            }
            if 'children' in token:
                for child in token['children']:
                    block['data']['text'] += self.parse_token(child, token)
            return block

        if token_type == 'block_code' or token_type == 'block_html':
            block['type'] = 'code'
            block['data'] = {
                'code': token['raw']
            }
            return block

        if token_type == 'heading':
            block['type'] = 'header'
            block['data'] = {
                'text': '',
                'level': token['attrs']['level'],
            }
            if 'children' in token:
                for child in token['children']:
                    block['data']['text'] += self.parse_token(child, token)
            return block

        if token_type == 'thematic_break':
            block['type'] = 'delimiter'
            block['data'] = {}
            return block

        if token_type == 'block_quote':
            block['type'] = 'quote'
            block['data'] = {
                "text": "",
                "caption": "",
                "alignment": "left"
            }
            if 'children' in token:
                for child in token['children']:
                    paragraph_text = self.parse_token(child, token)
                    block['data']['text'] += paragraph_text['data']['text']
            return block

        if token_type == 'list':
            block['type'] = 'list'
            block['data'] = {
                'meta': {},
                'items': [],
                'style': "ordered" if token['attrs']['ordered'] else "unordered",
            }
            if block['data']['style'] == 'ordered':
                block['data']['meta']['counterType'] = "numeric"
            if 'start' in token['attrs']:
                block['data']['meta']['start'] = token['attrs']['start']
            if 'children' in token:
                for child in token['children']:
                    block['data']['items'].append(self.parse_token(child, token))
            return block

        if token_type == 'list_item':
            item = {
                'meta': {},
                'items': [],
                'content': "",
            }
            if 'children' in token:
                for child in token['children']:
                    if child['type'] == 'paragraph':
                        paragraph_text = self.parse_token(child, token)
                        item['content'] += paragraph_text['data']['text']
                    if child['type'] == 'block_text':
                        item['content'] += self.parse_token(child, token)
                    if child['type'] == 'list':
                        sub_list = self.parse_token(child, token)
                        if 'meta' in sub_list:
                            item['meta'] = sub_list['meta']
                        if 'items' in sub_list:
                            item['items'] = sub_list['items']
            return item

        if token_type == 'block_text':
            text = ""
            if 'children' in token:
                for child in token['children']:
                    text += self.parse_token(child, token)
            return text

        return block


    def parse_tokens_to_blocks(self, tokens) -> list:
        blocks = list()
        for token in tokens:
            block = self.parse_token(token)
            if block is not None:
                blocks.append(block)
        return blocks

    def parse_image_to_block(self, post):
        return {
            "type": "image",
            "data": {
                "file": {
                    "url": post.image.url,
                },
                "caption": "",
                "stretched": False,
                "withBorder": False,
                "withBackground": False,
            }
        }

    def parse_file_to_block(self, post):
        try:
            filename = post.file.url.split('/')[-1]
        except ValueError:
            print(f"ERROR - FILE NOT FOUND - {post.id}")
            return None
        extension = filename.split('.')[-1]
        return {
            "type": "attaches",
            "data": {
                "file": {
                    "url": post.file.url,
                    "size": post.file.size,
                    "name": filename,
                    "extension": extension,
                }
            }
        }

    def parse_link_to_block(self, post):
        preview = get_link_preview(post.link)
        if preview['success'] == 1:
            print(f"LINK SUCCESSFULLY LOADED - {post.id}")
            return {
                "data": {
                    "link": preview['link'],
                    "meta": preview['meta'],
                },
                "type": "linkTool",
            }
        else:
            print(f"ERROR - LINK PREVIEW NOT LOADED - {post.id}")
            return {
                "data": {
                    "text": f'<a href="{post.link}">{post.link}</a>',
                },
                "type": "paragraph"
            }

    def generate_ejs_body(self, post, blocks: list):
        ejs_body = dict()

        ejs_body['time'] = int(post.created_date.timestamp() * 1000)
        ejs_body['version'] = "2.31.0-rc.7"
        ejs_body['blocks'] = blocks

        return ejs_body
