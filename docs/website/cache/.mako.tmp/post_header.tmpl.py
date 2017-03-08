# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1488933642.902441
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/post_header.tmpl'
_template_uri = u'post_header.tmpl'
_source_encoding = 'utf-8'
_exports = ['html_post_header', 'html_title', 'html_translations', 'html_sourcelink']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'comments', context._clean_inheritance_tokens(), templateuri=u'comments_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'comments')] = ns

    ns = runtime.TemplateNamespace(u'helper', context._clean_inheritance_tokens(), templateuri=u'post_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'helper')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_post_header(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        date_format = context.get('date_format', UNDEFINED)
        def html_title():
            return render_html_title(context)
        messages = context.get('messages', UNDEFINED)
        author_pages_generated = context.get('author_pages_generated', UNDEFINED)
        def html_sourcelink():
            return render_html_sourcelink(context)
        _link = context.get('_link', UNDEFINED)
        def html_translations(post):
            return render_html_translations(context,post)
        comments = _mako_get_namespace(context, 'comments')
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        post = context.get('post', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    <header>\n        ')
        __M_writer(unicode(html_title()))
        __M_writer(u'\n        <div class="metadata">\n            <p class="byline author vcard"><span class="byline-name fn">\n')
        if author_pages_generated:
            __M_writer(u'                    <a href="')
            __M_writer(unicode(_link('author', post.author())))
            __M_writer(u'">')
            __M_writer(filters.html_escape(unicode(post.author())))
            __M_writer(u'</a>\n')
        else:
            __M_writer(u'                    ')
            __M_writer(filters.html_escape(unicode(post.author())))
            __M_writer(u'\n')
        __M_writer(u'            </span></p>\n            <p class="dateline"><a href="')
        __M_writer(unicode(post.permalink()))
        __M_writer(u'" rel="bookmark"><time class="published dt-published" datetime="')
        __M_writer(unicode(post.formatted_date('webiso')))
        __M_writer(u'" itemprop="datePublished" title="')
        __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
        __M_writer(u'">')
        __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
        __M_writer(u'</time></a></p>\n')
        if not post.meta('nocomments') and site_has_comments:
            __M_writer(u'                <p class="commentline">')
            __M_writer(unicode(comments.comment_link(post.permalink(), post._base_path)))
            __M_writer(u'\n')
        __M_writer(u'            ')
        __M_writer(unicode(html_sourcelink()))
        __M_writer(u'\n')
        if post.meta('link'):
            __M_writer(u'                    <p class="linkline"><a href="')
            __M_writer(unicode(post.meta('link')))
            __M_writer(u'">')
            __M_writer(unicode(messages("Original site")))
            __M_writer(u'</a></p>\n')
        if post.description():
            __M_writer(u'                <meta name="description" itemprop="description" content="')
            __M_writer(filters.html_escape(unicode(post.description())))
            __M_writer(u'">\n')
        __M_writer(u'        </div>\n        ')
        __M_writer(unicode(html_translations(post)))
        __M_writer(u'\n    </header>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        post = context.get('post', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if title and not post.meta('hidetitle'):
            __M_writer(u'    <h1 class="p-name entry-title" itemprop="headline name"><a href="')
            __M_writer(unicode(post.permalink()))
            __M_writer(u'" class="u-url">')
            __M_writer(filters.html_escape(unicode(post.title())))
            __M_writer(u'</a></h1>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_translations(context,post):
    __M_caller = context.caller_stack._push_frame()
    try:
        lang = context.get('lang', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if len(post.translated_to) > 1:
            __M_writer(u'        <div class="metadata posttranslations translations">\n            <h3 class="posttranslations-intro">')
            __M_writer(unicode(messages("Also available in:")))
            __M_writer(u'</h3>\n')
            for langname in sorted(translations):
                if langname != lang and post.is_translation_available(langname):
                    __M_writer(u'                <p><a href="')
                    __M_writer(unicode(post.permalink(langname)))
                    __M_writer(u'" rel="alternate" hreflang="')
                    __M_writer(unicode(langname))
                    __M_writer(u'">')
                    __M_writer(unicode(messages("LANGUAGE", langname)))
                    __M_writer(u'</a></p>\n')
            __M_writer(u'        </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_sourcelink(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        post = context.get('post', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        show_sourcelink = context.get('show_sourcelink', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if show_sourcelink:
            __M_writer(u'        <p class="sourceline"><a href="')
            __M_writer(unicode(post.source_link()))
            __M_writer(u'" id="sourcelink">')
            __M_writer(unicode(messages("Source")))
            __M_writer(u'</a></p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"136": 11, "137": 12, "138": 13, "139": 14, "140": 14, "141": 15, "142": 16, "143": 17, "144": 17, "145": 17, "146": 17, "147": 17, "148": 17, "149": 17, "150": 20, "23": 3, "26": 2, "175": 169, "156": 24, "29": 0, "34": 2, "35": 3, "36": 9, "37": 22, "38": 28, "39": 55, "168": 26, "169": 26, "166": 26, "45": 30, "164": 25, "163": 24, "62": 30, "63": 32, "64": 32, "65": 35, "66": 36, "67": 36, "68": 36, "69": 36, "70": 36, "71": 37, "72": 38, "73": 38, "74": 38, "75": 40, "76": 41, "77": 41, "78": 41, "79": 41, "80": 41, "81": 41, "82": 41, "83": 41, "84": 42, "85": 43, "86": 43, "87": 43, "88": 45, "89": 45, "90": 45, "91": 46, "92": 47, "93": 47, "94": 47, "95": 47, "96": 47, "97": 49, "98": 50, "99": 50, "100": 50, "101": 52, "102": 53, "103": 53, "167": 26, "109": 5, "115": 5, "116": 6, "117": 7, "118": 7, "119": 7, "120": 7, "121": 7, "165": 26, "127": 11}, "uri": "post_header.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/post_header.tmpl"}
__M_END_METADATA
"""
