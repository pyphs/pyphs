# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479063795.201723
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/bootstrap3/templates/base.tmpl'
_template_uri = u'base.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head', u'sourcelink', u'extra_js', u'belowtitle']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'notes', context._clean_inheritance_tokens(), templateuri=u'annotation_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'notes')] = ns

    ns = runtime.TemplateNamespace(u'base', context._clean_inheritance_tokens(), templateuri=u'base_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'base')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def sourcelink():
            return render_sourcelink(context._locals(__M_locals))
        show_blog_title = _import_ns.get('show_blog_title', context.get('show_blog_title', UNDEFINED))
        momentjs_locales = _import_ns.get('momentjs_locales', context.get('momentjs_locales', UNDEFINED))
        date_fanciness = _import_ns.get('date_fanciness', context.get('date_fanciness', UNDEFINED))
        abs_link = _import_ns.get('abs_link', context.get('abs_link', UNDEFINED))
        blog_title = _import_ns.get('blog_title', context.get('blog_title', UNDEFINED))
        show_sourcelink = _import_ns.get('show_sourcelink', context.get('show_sourcelink', UNDEFINED))
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        js_date_format = _import_ns.get('js_date_format', context.get('js_date_format', UNDEFINED))
        content_footer = _import_ns.get('content_footer', context.get('content_footer', UNDEFINED))
        _link = _import_ns.get('_link', context.get('_link', UNDEFINED))
        def content():
            return render_content(context._locals(__M_locals))
        logo_url = _import_ns.get('logo_url', context.get('logo_url', UNDEFINED))
        annotations = _import_ns.get('annotations', context.get('annotations', UNDEFINED))
        body_end = _import_ns.get('body_end', context.get('body_end', UNDEFINED))
        template_hooks = _import_ns.get('template_hooks', context.get('template_hooks', UNDEFINED))
        translations = _import_ns.get('translations', context.get('translations', UNDEFINED))
        len = _import_ns.get('len', context.get('len', UNDEFINED))
        base = _mako_get_namespace(context, 'base')
        def extra_js():
            return render_extra_js(context._locals(__M_locals))
        post = _import_ns.get('post', context.get('post', UNDEFINED))
        lang = _import_ns.get('lang', context.get('lang', UNDEFINED))
        def belowtitle():
            return render_belowtitle(context._locals(__M_locals))
        search_form = _import_ns.get('search_form', context.get('search_form', UNDEFINED))
        messages = _import_ns.get('messages', context.get('messages', UNDEFINED))
        set_locale = _import_ns.get('set_locale', context.get('set_locale', UNDEFINED))
        notes = _mako_get_namespace(context, 'notes')
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(unicode(set_locale(lang)))
        __M_writer(u'\n')
        __M_writer(unicode(base.html_headstart()))
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_head'):
            context['self'].extra_head(**pageargs)
        

        __M_writer(u'\n')
        __M_writer(unicode(template_hooks['extra_head']()))
        __M_writer(u'\n</head>\n<body>\n<a href="#content" class="sr-only sr-only-focusable">')
        __M_writer(unicode(messages("Skip to main content")))
        __M_writer(u'</a>\n\n<!-- Menubar -->\n\n<nav class="navbar navbar-inverse navbar-static-top">\n    <div class="container"><!-- This keeps the margins nice -->\n        <div class="navbar-header">\n            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-navbar" aria-controls="bs-navbar" aria-expanded="false">\n            <span class="sr-only">Toggle navigation</span>\n            <span class="icon-bar"></span>\n            <span class="icon-bar"></span>\n            <span class="icon-bar"></span>\n            </button>\n            <a class="navbar-brand" href="')
        __M_writer(unicode(abs_link(_link("root", None, lang))))
        __M_writer(u'">\n')
        if logo_url:
            __M_writer(u'                <img src="')
            __M_writer(unicode(logo_url))
            __M_writer(u'" alt="')
            __M_writer(filters.html_escape(unicode(blog_title)))
            __M_writer(u'" id="logo">\n')
        __M_writer(u'\n')
        if show_blog_title:
            __M_writer(u'                <span id="blog-title">')
            __M_writer(filters.html_escape(unicode(blog_title)))
            __M_writer(u'</span>\n')
        __M_writer(u'            </a>\n        </div><!-- /.navbar-header -->\n        <div class="collapse navbar-collapse" id="bs-navbar" aria-expanded="false">\n            <ul class="nav navbar-nav">\n                ')
        __M_writer(unicode(base.html_navigation_links()))
        __M_writer(u'\n                ')
        __M_writer(unicode(template_hooks['menu']()))
        __M_writer(u'\n            </ul>\n')
        if search_form:
            __M_writer(u'                ')
            __M_writer(unicode(search_form))
            __M_writer(u'\n')
        __M_writer(u'\n            <ul class="nav navbar-nav navbar-right">\n                ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'belowtitle'):
            context['self'].belowtitle(**pageargs)
        

        __M_writer(u'\n')
        if show_sourcelink:
            __M_writer(u'                    ')
            if 'parent' not in context._data or not hasattr(context._data['parent'], 'sourcelink'):
                context['self'].sourcelink(**pageargs)
            

            __M_writer(u'\n')
        __M_writer(u'                ')
        __M_writer(unicode(template_hooks['menu_alt']()))
        __M_writer(u'\n            </ul>\n        </div><!-- /.navbar-collapse -->\n    </div><!-- /.container -->\n</nav>\n\n<!-- End of Menubar -->\n\n<div class="container" id="content" role="main">\n    <div class="body-content">\n        <!--Body content-->\n        <div class="row">\n            ')
        __M_writer(unicode(template_hooks['page_header']()))
        __M_writer(u'\n            ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n        </div>\n        <!--End of body content-->\n\n        <footer id="footer">\n            ')
        __M_writer(unicode(content_footer))
        __M_writer(u'\n            ')
        __M_writer(unicode(template_hooks['page_footer']()))
        __M_writer(u'\n        </footer>\n    </div>\n</div>\n\n')
        __M_writer(unicode(base.late_load_js()))
        __M_writer(u'\n    <script>$(\'a.image-reference:not(.islink) img:not(.islink)\').parent().colorbox({rel:"gal",maxWidth:"100%",maxHeight:"100%",scalePhotos:true});</script>\n    <!-- fancy dates -->\n    <script>\n    moment.locale("')
        __M_writer(unicode(momentjs_locales[lang]))
        __M_writer(u'");\n    fancydates(')
        __M_writer(unicode(date_fanciness))
        __M_writer(u', ')
        __M_writer(unicode(js_date_format))
        __M_writer(u');\n    </script>\n    <!-- end fancy dates -->\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_js'):
            context['self'].extra_js(**pageargs)
        

        __M_writer(u'\n')
        if annotations and post and not post.meta('noannotations'):
            __M_writer(u'        ')
            __M_writer(unicode(notes.code()))
            __M_writer(u'\n')
        elif not annotations and post and post.meta('annotations'):
            __M_writer(u'        ')
            __M_writer(unicode(notes.code()))
            __M_writer(u'\n')
        __M_writer(unicode(body_end))
        __M_writer(u'\n')
        __M_writer(unicode(template_hooks['body_end']()))
        __M_writer(u'\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def content():
            return render_content(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def extra_head():
            return render_extra_head(context)
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_sourcelink(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def sourcelink():
            return render_sourcelink(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_js(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def extra_js():
            return render_extra_js(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_belowtitle(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'notes')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        def belowtitle():
            return render_belowtitle(context)
        base = _mako_get_namespace(context, 'base')
        translations = _import_ns.get('translations', context.get('translations', UNDEFINED))
        len = _import_ns.get('len', context.get('len', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')
        if len(translations) > 1:
            __M_writer(u'                    <li>')
            __M_writer(unicode(base.html_translations()))
            __M_writer(u'</li>\n')
        __M_writer(u'                ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 66, "129": 71, "130": 71, "131": 72, "132": 72, "133": 77, "134": 77, "135": 81, "136": 81, "137": 82, "138": 82, "139": 82, "140": 82, "233": 46, "145": 85, "146": 86, "147": 87, "148": 87, "149": 87, "150": 88, "23": 3, "152": 89, "153": 89, "26": 2, "155": 91, "156": 92, "29": 0, "163": 66, "220": 45, "154": 91, "157": 92, "177": 6, "186": 6, "151": 89, "232": 45, "192": 51, "69": 2, "70": 3, "71": 4, "72": 4, "73": 5, "74": 5, "206": 85, "79": 8, "80": 9, "81": 9, "82": 12, "83": 12, "84": 25, "85": 25, "86": 26, "87": 27, "88": 27, "89": 27, "90": 27, "91": 27, "92": 29, "93": 30, "94": 31, "95": 31, "96": 31, "97": 33, "98": 37, "99": 37, "100": 38, "101": 38, "102": 40, "103": 41, "104": 41, "105": 41, "106": 43, "235": 47, "236": 47, "237": 49, "111": 49, "112": 50, "113": 51, "243": 237, "118": 51, "119": 53, "120": 53, "121": 53, "122": 65, "123": 65, "234": 47}, "uri": "base.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/bootstrap3/templates/base.tmpl"}
__M_END_METADATA
"""
