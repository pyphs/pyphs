# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1488973179.074261
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/index.tmpl'
_template_uri = u'index.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head', u'content_header']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'comments', context._clean_inheritance_tokens(), templateuri=u'comments_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'comments')] = ns

    ns = runtime.TemplateNamespace(u'helper', context._clean_inheritance_tokens(), templateuri=u'index_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'helper')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        permalink = context.get('permalink', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        date_format = context.get('date_format', UNDEFINED)
        author_pages_generated = context.get('author_pages_generated', UNDEFINED)
        def content_header():
            return render_content_header(context._locals(__M_locals))
        posts = context.get('posts', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        pagekind = context.get('pagekind', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        index_teasers = context.get('index_teasers', UNDEFINED)
        front_index_header = context.get('front_index_header', UNDEFINED)
        index_file = context.get('index_file', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_head'):
            context['self'].extra_head(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        date_format = context.get('date_format', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        posts = context.get('posts', UNDEFINED)
        def content_header():
            return render_content_header(context)
        author_pages_generated = context.get('author_pages_generated', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        def content():
            return render_content(context)
        pagekind = context.get('pagekind', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        index_teasers = context.get('index_teasers', UNDEFINED)
        front_index_header = context.get('front_index_header', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content_header'):
            context['self'].content_header(**pageargs)
        

        __M_writer(u'\n')
        if 'main_index' in pagekind:
            __M_writer(u'    ')
            __M_writer(unicode(front_index_header))
            __M_writer(u'\n')
        __M_writer(u'<div class="postindex">\n')
        for post in posts:
            __M_writer(u'    <article class="h-entry post-')
            __M_writer(unicode(post.meta('type')))
            __M_writer(u'">\n    <header>\n        <h1 class="p-name entry-title"><a href="')
            __M_writer(unicode(post.permalink()))
            __M_writer(u'" class="u-url">')
            __M_writer(filters.html_escape(unicode(post.title())))
            __M_writer(u'</a></h1>\n        <div class="metadata">\n            <p class="byline author vcard"><span class="byline-name fn">\n')
            if author_pages_generated:
                __M_writer(u'                <a href="')
                __M_writer(unicode(_link('author', post.author())))
                __M_writer(u'">')
                __M_writer(filters.html_escape(unicode(post.author())))
                __M_writer(u'</a>\n')
            else:
                __M_writer(u'                ')
                __M_writer(filters.html_escape(unicode(post.author())))
                __M_writer(u'\n')
            __M_writer(u'            </span></p>\n            <p class="dateline"><a href="')
            __M_writer(unicode(post.permalink()))
            __M_writer(u'" rel="bookmark"><time class="published dt-published" datetime="')
            __M_writer(unicode(post.formatted_date('webiso')))
            __M_writer(u'" title="')
            __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
            __M_writer(u'">')
            __M_writer(filters.html_escape(unicode(post.formatted_date(date_format))))
            __M_writer(u'</time></a></p>\n')
            if not post.meta('nocomments') and site_has_comments:
                __M_writer(u'                <p class="commentline">')
                __M_writer(unicode(comments.comment_link(post.permalink(), post._base_path)))
                __M_writer(u'\n')
            __M_writer(u'        </div>\n    </header>\n')
            if index_teasers:
                __M_writer(u'    <div class="p-summary entry-summary">\n    ')
                __M_writer(unicode(post.text(teaser_only=True)))
                __M_writer(u'\n')
            else:
                __M_writer(u'    <div class="e-content entry-content">\n    ')
                __M_writer(unicode(post.text(teaser_only=False)))
                __M_writer(u'\n')
            __M_writer(u'    </div>\n    </article>\n')
        __M_writer(u'</div>\n')
        __M_writer(unicode(helper.html_pager()))
        __M_writer(u'\n')
        __M_writer(unicode(comments.comment_link_script()))
        __M_writer(u'\n')
        __M_writer(unicode(helper.mathjax_script(posts)))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def extra_head():
            return render_extra_head(context)
        permalink = context.get('permalink', UNDEFINED)
        posts = context.get('posts', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        index_file = context.get('index_file', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.extra_head()))
        __M_writer(u'\n')
        if posts and (permalink == '/' or permalink == '/' + index_file):
            __M_writer(u'        <link rel="prefetch" href="')
            __M_writer(unicode(posts[0].permalink()))
            __M_writer(u'" type="text/html">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content_header():
            return render_content_header(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 31, "129": 31, "130": 32, "131": 33, "132": 33, "133": 33, "134": 35, "135": 37, "136": 38, "137": 39, "138": 39, "139": 40, "140": 41, "141": 42, "142": 42, "143": 44, "144": 47, "145": 48, "146": 48, "147": 49, "148": 49, "149": 50, "150": 50, "23": 3, "26": 2, "156": 6, "32": 0, "166": 6, "167": 7, "168": 7, "169": 8, "170": 9, "171": 9, "172": 9, "178": 14, "56": 2, "57": 3, "58": 4, "189": 178, "63": 11, "68": 51, "74": 13, "92": 13, "97": 14, "98": 15, "99": 16, "100": 16, "101": 16, "102": 18, "103": 19, "104": 20, "105": 20, "106": 20, "107": 22, "108": 22, "109": 22, "110": 22, "111": 25, "112": 26, "113": 26, "114": 26, "115": 26, "116": 26, "117": 27, "118": 28, "119": 28, "120": 28, "121": 30, "122": 31, "123": 31, "124": 31, "125": 31, "126": 31, "127": 31}, "uri": "index.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/index.tmpl"}
__M_END_METADATA
"""
