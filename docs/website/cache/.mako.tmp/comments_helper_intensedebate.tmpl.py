# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479307072.977542
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_intensedebate.tmpl'
_template_uri = u'comments_helper_intensedebate.tmpl'
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
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u"\n<script>\nvar idcomments_acct = '")
        __M_writer(unicode(comment_system_id))
        __M_writer(u'\';\nvar idcomments_post_id = "')
        __M_writer(unicode(identifier))
        __M_writer(u'";\nvar idcomments_post_url = "')
        __M_writer(unicode(url))
        __M_writer(u'";\n</script>\n<span id="IDCommentsPostTitle" style="display:none"></span>\n<script src=\'http://www.intensedebate.com/js/genericCommentWrapperV2.js\'></script>\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system_id = context.get('comment_system_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<a href="{link}" onclick="this.href=\'')
        __M_writer(unicode(link))
        __M_writer(u'\'; this.target=\'_self\';"><span class=\'IDCommentsReplace\' style=\'display:none\'>')
        __M_writer(unicode(identifier))
        __M_writer(u"</span>\n<script>\nvar idcomments_acct = '")
        __M_writer(unicode(comment_system_id))
        __M_writer(u'\';\nvar idcomments_post_id = "')
        __M_writer(unicode(identifier))
        __M_writer(u'";\nvar idcomments_post_url = "')
        __M_writer(unicode(link))
        __M_writer(u'";\n</script>\n<script src="http://www.intensedebate.com/js/genericLinkWrapperV2.js"></script>\n</a>\n')
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
{"source_encoding": "utf-8", "line_map": {"16": 0, "21": 11, "22": 22, "23": 25, "29": 2, "34": 2, "35": 4, "36": 4, "37": 5, "38": 5, "39": 6, "40": 6, "46": 13, "51": 13, "52": 14, "53": 14, "54": 14, "55": 14, "56": 16, "57": 16, "58": 17, "59": 17, "60": 18, "61": 18, "67": 24, "71": 24, "77": 71}, "uri": "comments_helper_intensedebate.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper_intensedebate.tmpl"}
__M_END_METADATA
"""
