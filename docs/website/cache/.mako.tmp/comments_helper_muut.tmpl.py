# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479312043.932778
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_muut.tmpl'
_template_uri = u'comments_helper_muut.tmpl'
_source_encoding = 'utf-8'
_exports = ['comment_form', 'comment_link', 'comment_link_script']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
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
        __M_writer(u'\n    <a class="muut" href="https://muut.com/i/')
        __M_writer(unicode(comment_system_id))
        __M_writer(u'/')
        __M_writer(unicode(identifier))
        __M_writer(u'">')
        __M_writer(unicode(comment_system_id))
        __M_writer(u' forums</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link_script(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n<script src="https://cdn.muut.com/1/moot.min.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"67": 61, "35": 3, "36": 4, "37": 4, "38": 4, "39": 4, "40": 4, "41": 4, "47": 7, "16": 0, "51": 7, "21": 2, "22": 5, "23": 8, "24": 13, "57": 11, "61": 11, "30": 3}, "uri": "comments_helper_muut.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_muut.tmpl"}
__M_END_METADATA
"""
