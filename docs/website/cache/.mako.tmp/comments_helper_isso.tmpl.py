# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479311332.295997
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_isso.tmpl'
_template_uri = u'comments_helper_isso.tmpl'
_source_encoding = 'utf-8'
_exports = ['comment_form', 'comment_link', 'comment_link_script']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_form(context,url,title,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system_id:
            __M_writer(u'        <div data-title="')
            __M_writer(filters.url_escape(unicode(title)))
            __M_writer(u'" id="isso-thread"></div>\n        <script src="')
            __M_writer(unicode(comment_system_id))
            __M_writer(u'js/embed.min.js" data-isso="')
            __M_writer(unicode(comment_system_id))
            __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system_id:
            __M_writer(u'        <a href="')
            __M_writer(unicode(link))
            __M_writer(u'#isso-thread">Comments</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link_script(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        pagekind = context.get('pagekind', UNDEFINED)
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system_id and 'index' in pagekind:
            __M_writer(u'        <script src="')
            __M_writer(unicode(comment_system_id))
            __M_writer(u'js/count.min.js" data-isso="')
            __M_writer(unicode(comment_system_id))
            __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "21": 7, "22": 13, "23": 20, "29": 2, "34": 2, "35": 3, "36": 4, "37": 4, "38": 4, "39": 5, "40": 5, "41": 5, "42": 5, "48": 9, "53": 9, "54": 10, "55": 11, "56": 11, "57": 11, "63": 16, "69": 16, "70": 17, "71": 18, "72": 18, "73": 18, "74": 18, "75": 18, "81": 75}, "uri": "comments_helper_isso.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_isso.tmpl"}
__M_END_METADATA
"""
