# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479308983.502023
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/tag.tmpl'
_template_uri = u'tag.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'list_post.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        kind = context.get('kind', UNDEFINED)
        subcategories = context.get('subcategories', UNDEFINED)
        description = context.get('description', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        date_format = context.get('date_format', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        title = context.get('title', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        len = context.get('len', UNDEFINED)
        generate_rss = context.get('generate_rss', UNDEFINED)
        posts = context.get('posts', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_head'):
            context['self'].extra_head(**pageargs)
        

        __M_writer(u'\n\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        generate_rss = context.get('generate_rss', UNDEFINED)
        kind = context.get('kind', UNDEFINED)
        subcategories = context.get('subcategories', UNDEFINED)
        description = context.get('description', UNDEFINED)
        title = context.get('title', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        len = context.get('len', UNDEFINED)
        def content():
            return render_content(context)
        posts = context.get('posts', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        date_format = context.get('date_format', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<article class="tagpage">\n    <header>\n        <h1>')
        __M_writer(filters.html_escape(unicode(title)))
        __M_writer(u'</h1>\n')
        if description:
            __M_writer(u'        <p>')
            __M_writer(unicode(description))
            __M_writer(u'</p>\n')
        if subcategories:
            __M_writer(u'        ')
            __M_writer(unicode(messages('Subcategories:')))
            __M_writer(u'\n        <ul>\n')
            for name, link in subcategories:
                __M_writer(u'            <li><a href="')
                __M_writer(unicode(link))
                __M_writer(u'">')
                __M_writer(filters.html_escape(unicode(name)))
                __M_writer(u'</a></li>\n')
            __M_writer(u'        </ul>\n')
        __M_writer(u'        <div class="metadata">\n')
        if len(translations) > 1 and generate_rss:
            for language in sorted(translations):
                __M_writer(u'                <p class="feedlink">\n                    <a href="')
                __M_writer(unicode(_link(kind + "_rss", tag, language)))
                __M_writer(u'" hreflang="')
                __M_writer(unicode(language))
                __M_writer(u'" type="application/rss+xml">')
                __M_writer(unicode(messages('RSS feed', language)))
                __M_writer(u' (')
                __M_writer(unicode(language))
                __M_writer(u')</a>&nbsp;\n                </p>\n')
        elif generate_rss:
            __M_writer(u'                <p class="feedlink"><a href="')
            __M_writer(unicode(_link(kind + "_rss", tag)))
            __M_writer(u'" type="application/rss+xml">')
            __M_writer(unicode(messages('RSS feed')))
            __M_writer(u'</a></p>\n')
        __M_writer(u'        </div>\n    </header>\n')
        if posts:
            __M_writer(u'    <ul class="postlist">\n')
            for post in posts:
                __M_writer(u'        <li><time class="listdate" datetime="')
                __M_writer(unicode(post.formatted_date('webiso')))
                __M_writer(u'" title="')
                __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
                __M_writer(u'">')
                __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
                __M_writer(u'</time> <a href="')
                __M_writer(unicode(post.permalink()))
                __M_writer(u'" class="listtitle">')
                __M_writer(filters.html_escape(unicode(post.title())))
                __M_writer(u'<a></li>\n')
            __M_writer(u'    </ul>\n')
        __M_writer(u'</article>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def extra_head():
            return render_extra_head(context)
        kind = context.get('kind', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        len = context.get('len', UNDEFINED)
        generate_rss = context.get('generate_rss', UNDEFINED)
        tag = context.get('tag', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.extra_head()))
        __M_writer(u'\n')
        if len(translations) > 1 and generate_rss:
            for language in sorted(translations):
                __M_writer(u'            <link rel="alternate" type="application/rss+xml" title="RSS for ')
                __M_writer(unicode(kind))
                __M_writer(u' ')
                __M_writer(filters.html_escape(unicode(tag)))
                __M_writer(u' (')
                __M_writer(unicode(language))
                __M_writer(u')" href="')
                __M_writer(unicode(_link(kind + "_rss", tag, language)))
                __M_writer(u'">\n')
        elif generate_rss:
            __M_writer(u'        <link rel="alternate" type="application/rss+xml" title="RSS for ')
            __M_writer(unicode(kind))
            __M_writer(u' ')
            __M_writer(filters.html_escape(unicode(tag)))
            __M_writer(u'" href="')
            __M_writer(unicode(_link(kind + "_rss", tag)))
            __M_writer(u'">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 46, "129": 46, "130": 46, "131": 46, "132": 46, "133": 46, "134": 46, "135": 46, "136": 48, "137": 50, "143": 4, "178": 11, "27": 0, "157": 4, "158": 5, "159": 5, "160": 6, "161": 7, "162": 8, "163": 8, "164": 8, "165": 8, "166": 8, "167": 8, "168": 8, "169": 8, "170": 8, "171": 10, "172": 11, "173": 11, "174": 11, "175": 11, "176": 11, "177": 11, "50": 2, "55": 13, "184": 178, "60": 51, "66": 16, "85": 16, "86": 19, "87": 19, "88": 20, "89": 21, "90": 21, "91": 21, "92": 23, "93": 24, "94": 24, "95": 24, "96": 26, "97": 27, "98": 27, "99": 27, "100": 27, "101": 27, "102": 29, "103": 31, "104": 32, "105": 33, "106": 34, "107": 35, "108": 35, "109": 35, "110": 35, "111": 35, "112": 35, "113": 35, "114": 35, "115": 38, "116": 39, "117": 39, "118": 39, "119": 39, "120": 39, "121": 41, "122": 43, "123": 44, "124": 45, "125": 46, "126": 46, "127": 46}, "uri": "tag.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/tag.tmpl"}
__M_END_METADATA
"""
