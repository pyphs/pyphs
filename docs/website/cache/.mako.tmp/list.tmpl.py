# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1486071345.845089
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/list.tmpl'
_template_uri = 'list.tmpl'
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
        def content():
            return render_content(context._locals(__M_locals))
        items = context.get('items', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        title = context.get('title', UNDEFINED)
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
        def content():
            return render_content(context)
        items = context.get('items', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<article class="listpage">\n    <header>\n        <h1>')
        __M_writer(filters.html_escape(unicode(title)))
        __M_writer(u'</h1>\n    </header>\n')
        if items:
            __M_writer(u'    <ul class="postlist">\n')
            for text, link, count in items:
                __M_writer(u'        <li><a href="')
                __M_writer(unicode(link))
                __M_writer(u'">')
                __M_writer(filters.html_escape(unicode(text)))
                __M_writer(u'</a>\n')
                if count:
                    __M_writer(u'            (')
                    __M_writer(unicode(count))
                    __M_writer(u')\n')
            __M_writer(u'    </ul>\n')
        else:
            __M_writer(u'    <p>')
            __M_writer(unicode(messages("Nothing found.")))
            __M_writer(u'</p>\n')
        __M_writer(u'</article>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"27": 0, "37": 2, "42": 22, "48": 4, "57": 4, "58": 7, "59": 7, "60": 9, "61": 10, "62": 11, "63": 12, "64": 12, "65": 12, "66": 12, "67": 12, "68": 13, "69": 14, "70": 14, "71": 14, "72": 17, "73": 18, "74": 19, "75": 19, "76": 19, "77": 21, "83": 77}, "uri": "list.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/list.tmpl"}
__M_END_METADATA
"""
