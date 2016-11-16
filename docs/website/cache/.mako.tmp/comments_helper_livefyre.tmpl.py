# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479308983.283051
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_livefyre.tmpl'
_template_uri = u'comments_helper_livefyre.tmpl'
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
        __M_writer(u'\n<div id="livefyre-comments"></div>\n<script src="http://zor.livefyre.com/wjs/v3.0/javascripts/livefyre.js"></script>\n<script>\n(function () {\n    var articleId = "')
        __M_writer(unicode(identifier))
        __M_writer(u'";\n    fyre.conv.load({}, [{\n        el: \'livefyre-comments\',\n        network: "livefyre.com",\n        siteId: "')
        __M_writer(unicode(comment_system_id))
        __M_writer(u'",\n        articleId: articleId,\n        signed: false,\n        collectionMeta: {\n            articleId: articleId,\n            url: fyre.conv.load.makeCollectionUrl(),\n        }\n    }], function() {});\n}());\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    <a href="')
        __M_writer(unicode(link))
        __M_writer(u'">\n    <span class="livefyre-commentcount" data-lf-site-id="')
        __M_writer(unicode(comment_system_id))
        __M_writer(u'" data-lf-article-id="')
        __M_writer(unicode(identifier))
        __M_writer(u'">\n    0 Comments\n    </span>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link_script(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n<script src="http://zor.livefyre.com/wjs/v1.0/javascripts/CommentCount.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"65": 31, "34": 2, "35": 7, "36": 7, "37": 11, "38": 11, "71": 65, "55": 25, "44": 23, "61": 31, "16": 0, "49": 23, "50": 24, "51": 24, "52": 25, "21": 21, "22": 28, "23": 33, "54": 25, "29": 2, "53": 25}, "uri": "comments_helper_livefyre.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_livefyre.tmpl"}
__M_END_METADATA
"""
