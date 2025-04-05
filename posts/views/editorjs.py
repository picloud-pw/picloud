import json
import logging
import os

from datetime import datetime
from secrets import token_urlsafe

from django.http import JsonResponse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

from django.utils.module_loading import import_string
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.views.decorators.csrf import csrf_exempt

from picloud.settings import get_config

FILE_NAME = lambda **_: token_urlsafe(8)
FILE_NAME_ORIGINAL = False
FILE_UPLOAD_PATH = "resources/posts/"
FILE_UPLOAD_PATH_DATE = "%Y/%m/%d/"
FILE_MAX_SIZE = 1048576  # 1 Mb in bytes

STORAGE = import_string('django.core.files.storage.DefaultStorage')()

OPEN_GRAPH_API_KEY = get_config('OPEN_GRAPH_API_KEY')

LOGGER = logging.getLogger('picloud_posts')


@csrf_exempt
def file_upload(request):
    for f_n, f in request.FILES.items():
        the_file = request.FILES[f_n]
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/pjpeg',
            'image/x-png',
            'image/png',
            'image/webp',
            'image/gif',

            'application/pdf',
            'application/zip',
            'application/x-7z-compressed',
            'application/x-tar',
            'application/vnd.rar',
            'application/gzip',
            'application/msword',
            'application/vnd.ms-excel',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        ]
        if the_file.content_type not in allowed_types:
            return JsonResponse(
                {'success': 0, 'message': 'You can only upload images, PDFs, archives, and MS office documents.'}
            )
        if the_file.size > FILE_MAX_SIZE:
            return JsonResponse(
                {'success': 0, 'message': f'Maximum file size exceeded - {FILE_MAX_SIZE} bytes.'}
            )

        filename, extension = os.path.splitext(the_file.name)

        if FILE_NAME_ORIGINAL is False:
            filename = FILE_NAME(filename=filename, file=the_file)

        filename += extension

        upload_path = FILE_UPLOAD_PATH

        if FILE_UPLOAD_PATH_DATE:
            upload_path += datetime.now().strftime(FILE_UPLOAD_PATH_DATE)

        path = STORAGE.save(
            os.path.join(upload_path, filename), the_file
        )
        link = STORAGE.url(path)

        return JsonResponse({
            'success': 1,
            'file': {
                "url": link,
                "size": the_file.size,
                "name": filename,
                "extension": extension.replace('.', ''),
            },
        })
    return JsonResponse({'success': 0})


@csrf_exempt
def file_by_url(request):
    body = json.loads(request.body.decode())
    if 'url' in body:
        return JsonResponse({'success': 1, 'file': {"url": body['url']}})
    return JsonResponse({'success': 0})


# def image_delete(request):
#     path_file = request.GET.get('pathFile')

#     if not path_file:
#         return JsonResponse({'success': 0, 'message': 'Parameter "pathFile" Not Found'})

#     base_dir = getattr(settings, "BASE_DIR", '')
#     path_file = f'{base_dir}{path_file}'

#     if not os.path.isfile(path_file):
#         return JsonResponse({'success': 0, 'message': 'File Not Found'})

#     os.remove(path_file)

#     return JsonResponse({'success': 1})


@csrf_exempt
def link_tool(request):

    url = request.GET.get('url', '')
    link_preview = get_link_preview(url)
    return JsonResponse(link_preview)


def get_link_preview(url):

    LOGGER.debug('Starting to get meta for: %s', url)

    if not any([url.startswith(s) for s in ('http://', 'https://')]):
        LOGGER.debug('Adding the http protocol to the link: %s', url)
        url = 'http://' + url

    validate = URLValidator(schemes=['http', 'https'])

    try:
        validate(url)
    except ValidationError as e:
        LOGGER.error(e)
        return {'success': 0, 'message': str(e)}

    microlink_preview = microlink_link_preview(url)
    if microlink_preview['success'] == 1:
        return microlink_preview
    else:
        return opengraph_link_preview(url)


def microlink_link_preview(url):
    try:
        full_url = 'https://api.microlink.io/?' + urlencode({'url': url})
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = Request(full_url, headers={'User-Agent': user_agent})
        res = urlopen(req)
    except Exception as e:
        LOGGER.error('The server couldn\'t fulfill the request.')
        return {'success': 0, 'message': str(e)}

    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))

    if res.status == 200:
        data = res_json.get('data')

        if data:
            LOGGER.debug('Response meta: %s', data)
            meta = {}
            meta['title'] = data.get('title')
            meta['description'] = data.get('description')
            meta['image'] = data.get('image')

            return {
                'success': 1,
                'link': data.get('url', url),
                'meta': meta
            }
    else:
        return {'success': 0, 'message': "Response is not 200."}


def opengraph_link_preview(url):
    try:
        req = Request(
            f'https://opengraph.io/api/1.1/site/{quote(url, safe="")}?' +
            urlencode({'app_id': OPEN_GRAPH_API_KEY, })
        )
        res = urlopen(req)
    except Exception as e:
        LOGGER.error('The server couldn\'t fulfill the request.')
        return {'success': 0, 'message': str(e)}

    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))

    if res.status == 200:
        data = res_json.get('hybridGraph')

        if data:
            LOGGER.debug('Response meta: %s', data)
            meta = {}
            meta['title'] = data.get('title')
            meta['description'] = data.get('description')
            meta['image'] = data.get('image')

            return {
                'success': 1,
                'link': data.get('url', url),
                'meta': meta
            }
    else:
        return {'success': 0, 'message': "Response is not 200."}
