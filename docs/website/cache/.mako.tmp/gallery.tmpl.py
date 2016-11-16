# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479308651.266177
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/gallery.tmpl'
_template_uri = u'gallery.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'sourcelink', u'extra_head']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'ui', context._clean_inheritance_tokens(), templateuri=u'crumbs.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'ui')] = ns

    ns = runtime.TemplateNamespace(u'comments', context._clean_inheritance_tokens(), templateuri=u'comments_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'comments')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, u'ui')._populate(_import_ns, [u'bar'])
        folders = _import_ns.get('folders', context.get('folders', UNDEFINED))
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        permalink = _import_ns.get('permalink', context.get('permalink', UNDEFINED))
        photo_array = _import_ns.get('photo_array', context.get('photo_array', UNDEFINED))
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        title = _import_ns.get('title', context.get('title', UNDEFINED))
        def sourcelink():
            return render_sourcelink(context._locals(__M_locals))
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context._locals(__M_locals))
        ui = _mako_get_namespace(context, 'ui')
        crumbs = _import_ns.get('crumbs', context.get('crumbs', UNDEFINED))
        site_has_comments = _import_ns.get('site_has_comments', context.get('site_has_comments', UNDEFINED))
        enable_comments = _import_ns.get('enable_comments', context.get('enable_comments', UNDEFINED))
        post = _import_ns.get('post', context.get('post', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'sourcelink'):
            context['self'].sourcelink(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_head'):
            context['self'].extra_head(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'ui')._populate(_import_ns, [u'bar'])
        folders = _import_ns.get('folders', context.get('folders', UNDEFINED))
        permalink = _import_ns.get('permalink', context.get('permalink', UNDEFINED))
        photo_array = _import_ns.get('photo_array', context.get('photo_array', UNDEFINED))
        title = _import_ns.get('title', context.get('title', UNDEFINED))
        comments = _mako_get_namespace(context, 'comments')
        def content():
            return render_content(context)
        ui = _mako_get_namespace(context, 'ui')
        crumbs = _import_ns.get('crumbs', context.get('crumbs', UNDEFINED))
        site_has_comments = _import_ns.get('site_has_comments', context.get('site_has_comments', UNDEFINED))
        enable_comments = _import_ns.get('enable_comments', context.get('enable_comments', UNDEFINED))
        post = _import_ns.get('post', context.get('post', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(ui.bar(crumbs)))
        __M_writer(u'\n')
        if title:
            __M_writer(u'    <h1>')
            __M_writer(filters.html_escape(unicode(title)))
            __M_writer(u'</h1>\n')
        if post:
            __M_writer(u'    <p>\n        ')
            __M_writer(unicode(post.text()))
            __M_writer(u'\n    </p>\n')
        if folders:
            __M_writer(u'    <ul>\n')
            for folder, ftitle in folders:
                __M_writer(u'        <li><a href="')
                __M_writer(filters.url_escape(unicode(folder)))
                __M_writer(u'"><i\n        class="icon-folder-open"></i>&nbsp;')
                __M_writer(filters.html_escape(unicode(ftitle)))
                __M_writer(u'</a></li>\n')
            __M_writer(u'    </ul>\n')
        if photo_array:
            __M_writer(u'    <ul class="thumbnails">\n')
            for image in photo_array:
                __M_writer(u'            <li><a href="')
                __M_writer(unicode(image['url']))
                __M_writer(u'" class="thumbnail image-reference" title="')
                __M_writer(unicode(image['title']))
                __M_writer(u'">\n                <img src="')
                __M_writer(unicode(image['url_thumb']))
                __M_writer(u'" alt="')
                __M_writer(filters.html_escape(unicode(image['title'])))
                __M_writer(u'" /></a>\n')
            __M_writer(u'    </ul>\n')
        if site_has_comments and enable_comments:
            __M_writer(u'    ')
            __M_writer(unicode(comments.comment_form(None, permalink, title)))
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_sourcelink(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'ui')._populate(_import_ns, [u'bar'])
        def sourcelink():
            return render_sourcelink(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'ui')._populate(_import_ns, [u'bar'])
        def extra_head():
            return render_extra_head(context)
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(unicode(parent.extra_head()))
        __M_writer(u'\n<link rel="alternate" type="application/rss+xml" title="RSS" href="rss.xml">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 29, "129": 31, "130": 33, "131": 34, "132": 34, "133": 34, "139": 5, "23": 4, "152": 38, "26": 3, "32": 0, "161": 38, "162": 39, "163": 39, "169": 163, "56": 2, "57": 3, "58": 4, "63": 5, "68": 36, "73": 41, "79": 7, "97": 7, "98": 8, "99": 8, "100": 9, "101": 10, "102": 10, "103": 10, "104": 12, "105": 13, "106": 14, "107": 14, "108": 17, "109": 18, "110": 19, "111": 20, "112": 20, "113": 20, "114": 21, "115": 21, "116": 23, "117": 25, "118": 26, "119": 27, "120": 28, "121": 28, "122": 28, "123": 28, "124": 28, "125": 29, "126": 29, "127": 29}, "uri": "gallery.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/gallery.tmpl"}
__M_END_METADATA
"""
