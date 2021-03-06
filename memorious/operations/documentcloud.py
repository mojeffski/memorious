import os
from urlparse import urljoin
from pycountry import languages

DEFAULT_HOST = 'https://documentcloud.org/'
DEFAULT_INSTANCE = 'documentcloud'


def documentcloud_query(context, data):
    host = context.get('host', DEFAULT_HOST)
    instance = context.get('instance', DEFAULT_INSTANCE)
    query = context.get('query')
    page = data.get('page', 1)

    search_url = urljoin(host, 'search/documents.json')
    res = context.http.get(search_url, params={
        'q': query,
        'per_page': 100,
        'page': page
    })
    documents = res.json.get('documents', [])
    for document in documents:
        data['foreign_id'] = '%s:%s' % (instance, document.get('id'))
        data['url'] = document.get('pdf_url')
        data['source_url'] = document.get('canonical_url')
        data['title'] = document.get('title')
        data['author'] = document.get('author')
        data['file_name'] = os.path.basename(document.get('pdf_url'))
        data['mime_type'] = 'application/pdf'

        # lang_code = document.get('language')
        # try:
        #     lang = languages.get(alpha_3=lang_code)
        #     data['languages'] = [lang.alpha_2]
        # except Exception:
        #     context.emit_warning("Unknown language code: %s" % lang_code)
        context.emit(rule='pass', data=data)

    if len(documents):
        context.recurse(data={'page': page + 1})
