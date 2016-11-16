# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479311098.252636
_enable_loop = True
_template_filename = u'themes/lanyon/templates/base.tmpl'
_template_uri = u'base.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content', u'extra_head', u'extra_js']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'header', context._clean_inheritance_tokens(), templateuri=u'base_header.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'header')] = ns

    ns = runtime.TemplateNamespace(u'base', context._clean_inheritance_tokens(), templateuri=u'base_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'base')] = ns

    ns = runtime.TemplateNamespace(u'annotations', context._clean_inheritance_tokens(), templateuri=u'annotation_helper.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'annotations')] = ns

    ns = runtime.TemplateNamespace(u'footer', context._clean_inheritance_tokens(), templateuri=u'base_footer.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'footer')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, u'header')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'footer')._populate(_import_ns, [u'*'])
        lang = _import_ns.get('lang', context.get('lang', UNDEFINED))
        def extra_head():
            return render_extra_head(context._locals(__M_locals))
        body_end = _import_ns.get('body_end', context.get('body_end', UNDEFINED))
        template_hooks = _import_ns.get('template_hooks', context.get('template_hooks', UNDEFINED))
        footer = _mako_get_namespace(context, 'footer')
        js_date_format = _import_ns.get('js_date_format', context.get('js_date_format', UNDEFINED))
        messages = _import_ns.get('messages', context.get('messages', UNDEFINED))
        momentjs_locales = _import_ns.get('momentjs_locales', context.get('momentjs_locales', UNDEFINED))
        set_locale = _import_ns.get('set_locale', context.get('set_locale', UNDEFINED))
        def content():
            return render_content(context._locals(__M_locals))
        header = _mako_get_namespace(context, 'header')
        base = _mako_get_namespace(context, 'base')
        date_fanciness = _import_ns.get('date_fanciness', context.get('date_fanciness', UNDEFINED))
        lanyon_subtheme = _import_ns.get('lanyon_subtheme', context.get('lanyon_subtheme', UNDEFINED))
        def extra_js():
            return render_extra_js(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
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
        __M_writer(u'\n</head>\n')
        if lanyon_subtheme:
            __M_writer(u'<body class="')
            __M_writer(unicode(lanyon_subtheme))
            __M_writer(u'">\n')
        else:
            __M_writer(u'<body>\n')
        __M_writer(u'    <a href="#content" class="sr-only sr-only-focusable">')
        __M_writer(unicode(messages("Skip to main content")))
        __M_writer(u'</a>\n    <!-- Target for toggling the sidebar `.sidebar-checkbox` is for regular\n            styles, `#sidebar-checkbox` for behavior. -->\n    <input type="checkbox" class="sidebar-checkbox" id="sidebar-checkbox">\n\n    <!-- Toggleable sidebar -->\n    <div class="sidebar" id="sidebar">\n        <div class="sidebar-item">\n            <p><a href="https://github.com/afalaize/pyphs/" target="_blank">PyPHS</a> as been developed between 2012 and 2016 as part of the PhD project of Antoine Falaize, through EDITE (UPMC ED-130) funding in the <a href="http://s3.ircam.fr/?lang=en" target="_blank">project/team S3</a> (Sound Signals and Systems) at <a href="http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/" target="_blank">STMS Research Lab</a> (CNRS UMR 9912), hosted by IRCAM. It is distributed under the french <a href="http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html" target="_blank">CeCILL-B</a> licence.</p>\n        </div>\n        ')
        __M_writer(unicode(header.html_navigation_links()))
        __M_writer(u'\n    </div>\n\n    <!-- Wrap is the content to shift when toggling the sidebar. We wrap the\n         content to avoid any CSS collisions with our real content. -->\n    <div class="wrap">\n      <div class="masthead">\n        <div class="container">\n          ')
        __M_writer(unicode(header.html_site_title()))
        __M_writer(u'\n        </div>\n      </div>\n\n      <div class="container content" id="content">\n        ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n        ')
        __M_writer(unicode(footer.html_footer()))
        __M_writer(u'\n      </div>\n    </div>\n    <label for="sidebar-checkbox" class="sidebar-toggle"></label>\n    ')
        __M_writer(unicode(body_end))
        __M_writer(u'\n    ')
        __M_writer(unicode(template_hooks['body_end']()))
        __M_writer(u'\n    ')
        __M_writer(unicode(base.late_load_js()))
        __M_writer(u'\n    <!-- fancy dates -->\n    <script>\n    moment.locale("')
        __M_writer(unicode(momentjs_locales[lang]))
        __M_writer(u'");\n    fancydates(')
        __M_writer(unicode(date_fanciness))
        __M_writer(u', ')
        __M_writer(unicode(js_date_format))
        __M_writer(u');\n    </script>\n    <!-- end fancy dates -->\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra_js'):
            context['self'].extra_js(**pageargs)
        

        __M_writer(u'\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'header')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'footer')._populate(_import_ns, [u'*'])
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
        _mako_get_namespace(context, u'header')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'footer')._populate(_import_ns, [u'*'])
        def extra_head():
            return render_extra_head(context)
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra_js(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, u'header')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'base')._populate(_import_ns, [u'*'])
        _mako_get_namespace(context, u'footer')._populate(_import_ns, [u'*'])
        def extra_js():
            return render_extra_js(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"134": 8, "144": 8, "150": 55, "23": 3, "26": 2, "29": 5, "32": 4, "35": 0, "165": 150, "62": 2, "63": 3, "64": 4, "65": 5, "66": 6, "67": 6, "68": 7, "69": 7, "74": 10, "75": 11, "76": 11, "77": 13, "78": 14, "79": 14, "80": 14, "81": 15, "82": 16, "83": 18, "84": 18, "85": 18, "86": 28, "87": 28, "88": 36, "89": 36, "94": 41, "95": 42, "96": 42, "97": 46, "98": 46, "99": 47, "100": 47, "101": 48, "102": 48, "103": 51, "104": 51, "105": 52, "106": 52, "107": 52, "108": 52, "113": 55, "119": 41}, "uri": "base.tmpl", "filename": "themes/lanyon/templates/base.tmpl"}
__M_END_METADATA
"""
