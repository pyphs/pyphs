# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1490183308.194281
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/crumbs.tmpl'
_template_uri = u'crumbs.tmpl'
_source_encoding = 'utf-8'
_exports = ['bar']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bar(context,crumbs):
    __M_caller = context.caller_stack._push_frame()
    try:
        index_file = context.get('index_file', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if crumbs:
            __M_writer(u'<nav class="breadcrumbs">\n<ul class="breadcrumb">\n')
            for link, text in crumbs:
                if text != index_file:
                    if link == '#':
                        __M_writer(u'                <li>')
                        __M_writer(unicode(text.rsplit('.html', 1)[0]))
                        __M_writer(u'</li>\n')
                    else:
                        __M_writer(u'                <li><a href="')
                        __M_writer(unicode(link))
                        __M_writer(u'">')
                        __M_writer(unicode(text))
                        __M_writer(u'</a></li>\n')
            __M_writer(u'</ul>\n</nav>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"33": 3, "34": 4, "35": 5, "36": 7, "37": 8, "38": 9, "39": 10, "40": 10, "41": 10, "42": 11, "43": 12, "44": 12, "45": 12, "46": 12, "47": 12, "16": 0, "48": 16, "21": 2, "22": 19, "54": 48, "28": 3}, "uri": "crumbs.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/crumbs.tmpl"}
__M_END_METADATA
"""
