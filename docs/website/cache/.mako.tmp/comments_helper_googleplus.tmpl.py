# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479311098.602679
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_googleplus.tmpl'
_template_uri = u'comments_helper_googleplus.tmpl'
_source_encoding = 'utf-8'
_exports = ['comment_form', 'comment_link', 'comment_link_script']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_form(context,url,title,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n<script src="https://apis.google.com/js/plusone.js"></script>\n<div class="g-comments"\n    data-href="')
        __M_writer(unicode(url))
        __M_writer(u'"\n    data-first_party_property="BLOGGER"\n    data-view_type="FILTERED_POSTMOD">\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n<div class="g-commentcount" data-href="')
        __M_writer(unicode(link))
        __M_writer(u'"></div>\n<script src="https://apis.google.com/js/plusone.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link_script(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"33": 2, "34": 5, "35": 5, "41": 11, "45": 11, "46": 12, "47": 12, "16": 0, "21": 9, "22": 14, "23": 17, "57": 16, "63": 57, "29": 2, "53": 16}, "uri": "comments_helper_googleplus.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_googleplus.tmpl"}
__M_END_METADATA
"""
