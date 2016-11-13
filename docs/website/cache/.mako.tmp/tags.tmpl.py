# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479068711.782789
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/tags.tmpl'
_template_uri = u'tags.tmpl'
_source_encoding = 'utf-8'
_exports = [u'content']


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
    return runtime._inherit_from(context, u'base.tmpl', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        cat_items = context.get('cat_items', UNDEFINED)
        cat_hierarchy = context.get('cat_hierarchy', UNDEFINED)
        title = context.get('title', UNDEFINED)
        items = context.get('items', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        len = context.get('len', UNDEFINED)
        hidden_tags = context.get('hidden_tags', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        range = context.get('range', UNDEFINED)
        __M_writer = context.writer()
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
        cat_items = context.get('cat_items', UNDEFINED)
        cat_hierarchy = context.get('cat_hierarchy', UNDEFINED)
        title = context.get('title', UNDEFINED)
        items = context.get('items', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        len = context.get('len', UNDEFINED)
        hidden_tags = context.get('hidden_tags', UNDEFINED)
        def content():
            return render_content(context)
        range = context.get('range', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<article class="tagindex">\n    <header>\n        <h1>')
        __M_writer(filters.html_escape(unicode(title)))
        __M_writer(u'</h1>\n    </header>\n')
        if cat_items:
            if items:
                __M_writer(u'            <h2>')
                __M_writer(unicode(messages("Categories")))
                __M_writer(u'</h2>\n')
            for text, full_name, path, link, indent_levels, indent_change_before, indent_change_after in cat_hierarchy:
                for i in range(indent_change_before):
                    __M_writer(u'                <ul class="postlist">\n')
                __M_writer(u'            <li><a class="reference" href="')
                __M_writer(unicode(link))
                __M_writer(u'">')
                __M_writer(unicode(text))
                __M_writer(u'</a>\n')
                if indent_change_after <= 0:
                    __M_writer(u'                </li>\n')
                for i in range(-indent_change_after):
                    __M_writer(u'                </ul>\n')
                    if i + 1 < len(indent_levels):
                        __M_writer(u'                    </li>\n')
            if items:
                __M_writer(u'            <h2>')
                __M_writer(unicode(messages("Tags")))
                __M_writer(u'</h2>\n')
        if items:
            __M_writer(u'        <ul class="postlist">\n')
            for text, link in items:
                if text not in hidden_tags:
                    __M_writer(u'                <li><a class="reference listtitle" href="')
                    __M_writer(unicode(link))
                    __M_writer(u'">')
                    __M_writer(filters.html_escape(unicode(text)))
                    __M_writer(u'</a></li>\n')
            __M_writer(u'        </ul>\n')
        __M_writer(u'</article>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"27": 0, "42": 2, "47": 42, "53": 4, "67": 4, "68": 7, "69": 7, "70": 9, "71": 10, "72": 11, "73": 11, "74": 11, "75": 13, "76": 14, "77": 15, "78": 17, "79": 17, "80": 17, "81": 17, "82": 17, "83": 18, "84": 19, "85": 21, "86": 22, "87": 23, "88": 24, "89": 28, "90": 29, "91": 29, "92": 29, "93": 32, "94": 33, "95": 34, "96": 35, "97": 36, "98": 36, "99": 36, "100": 36, "101": 36, "102": 39, "103": 41, "109": 103}, "uri": "tags.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/tags.tmpl"}
__M_END_METADATA
"""
