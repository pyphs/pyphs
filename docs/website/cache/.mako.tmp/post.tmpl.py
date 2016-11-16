# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479312238.108337
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/post.tmpl'
_template_uri = u'post.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'pheader', context._clean_inheritance_tokens(), templateuri=u'post_header.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'pheader')] = ns

    ns = runtime.TemplateNamespace(u'comments', context._clean_inheritance_tokens(), templateuri=u'comments_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'comments')] = ns

    ns = runtime.TemplateNamespace(u'helper', context._clean_inheritance_tokens(), templateuri=u'post_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'helper')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        pheader = _mako_get_namespace(context, 'pheader')
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        parent = context.get('parent', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        messages = context.get('messages', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context._locals(__M_locals))
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        post = context.get('post', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
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
        pheader = _mako_get_namespace(context, 'pheader')
        helper = _mako_get_namespace(context, 'helper')
        messages = context.get('messages', UNDEFINED)
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context)
        site_has_comments = context.get('site_has_comments', UNDEFINED)
        post = context.get('post', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<article class="post-')
        __M_writer(unicode(post.meta('type')))
        __M_writer(u' h-entry hentry postpage" itemscope="itemscope" itemtype="http://schema.org/Article">\n    ')
        __M_writer(unicode(pheader.html_post_header()))
        __M_writer(u'\n    <div class="e-content entry-content" itemprop="articleBody text">\n    ')
        __M_writer(unicode(post.text()))
        __M_writer(u'\n    </div>\n    <aside class="postpromonav">\n    <nav>\n    ')
        __M_writer(unicode(helper.html_tags(post)))
        __M_writer(u'\n    ')
        __M_writer(unicode(helper.html_pager(post)))
        __M_writer(u'\n    </nav>\n    </aside>\n')
        if not post.meta('nocomments') and site_has_comments:
            __M_writer(u'        <section class="comments hidden-print">\n        <h2>')
            __M_writer(unicode(messages("Comments")))
            __M_writer(u'</h2>\n        ')
            __M_writer(unicode(comments.comment_form(post.permalink(absolute=True), post.title(), post._base_path)))
            __M_writer(u'\n        </section>\n')
        __M_writer(u'    ')
        __M_writer(unicode(helper.mathjax_script(post)))
        __M_writer(u'\n</article>\n')
        __M_writer(unicode(comments.comment_link_script()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def extra_head():
            return render_extra_head(context)
        post = context.get('post', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.extra_head()))
        __M_writer(u'\n')
        if post.meta('keywords'):
            __M_writer(u'    <meta name="keywords" content="')
            __M_writer(filters.html_escape(unicode(post.meta('keywords'))))
            __M_writer(u'">\n')
        if post.description():
            __M_writer(u'    <meta name="description" content="')
            __M_writer(filters.html_escape(unicode(post.description())))
            __M_writer(u'">\n')
        __M_writer(u'    <meta name="author" content="')
        __M_writer(filters.html_escape(unicode(post.author())))
        __M_writer(u'">\n')
        if post.prev_post:
            __M_writer(u'        <link rel="prev" href="')
            __M_writer(unicode(post.prev_post.permalink()))
            __M_writer(u'" title="')
            __M_writer(filters.html_escape(unicode(post.prev_post.title())))
            __M_writer(u'" type="text/html">\n')
        if post.next_post:
            __M_writer(u'        <link rel="next" href="')
            __M_writer(unicode(post.next_post.permalink()))
            __M_writer(u'" title="')
            __M_writer(filters.html_escape(unicode(post.next_post.title())))
            __M_writer(u'" type="text/html">\n')
        if post.is_draft:
            __M_writer(u'        <meta name="robots" content="noindex">\n')
        __M_writer(u'    ')
        __M_writer(unicode(helper.open_graph_metadata(post)))
        __M_writer(u'\n    ')
        __M_writer(unicode(helper.twitter_card_information(post)))
        __M_writer(u'\n    ')
        __M_writer(unicode(helper.meta_translations(post)))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 13, "129": 15, "130": 15, "131": 15, "132": 16, "133": 17, "134": 17, "135": 17, "136": 17, "137": 17, "138": 19, "139": 20, "140": 20, "141": 20, "142": 20, "143": 20, "144": 22, "145": 23, "146": 25, "147": 25, "148": 25, "149": 26, "150": 26, "23": 3, "152": 27, "26": 4, "29": 2, "158": 152, "35": 0, "51": 2, "52": 3, "53": 4, "54": 5, "59": 28, "151": 27, "64": 51, "70": 30, "82": 30, "83": 31, "84": 31, "85": 32, "86": 32, "87": 34, "88": 34, "89": 38, "90": 38, "91": 39, "92": 39, "93": 42, "94": 43, "95": 44, "96": 44, "97": 45, "98": 45, "99": 48, "100": 48, "101": 48, "102": 50, "103": 50, "109": 7, "118": 7, "119": 8, "120": 8, "121": 9, "122": 10, "123": 10, "124": 10, "125": 12, "126": 13, "127": 13}, "uri": "post.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/post.tmpl"}
__M_END_METADATA
"""
