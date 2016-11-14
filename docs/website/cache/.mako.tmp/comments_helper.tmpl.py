# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1479081993.368401
_enable_loop = True
_template_filename = u'/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper.tmpl'
_template_uri = u'comments_helper.tmpl'
_source_encoding = 'utf-8'
_exports = ['comment_form', 'comment_link', 'comment_link_script']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'livefyre', context._clean_inheritance_tokens(), templateuri=u'comments_helper_livefyre.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'livefyre')] = ns

    ns = runtime.TemplateNamespace(u'googleplus', context._clean_inheritance_tokens(), templateuri=u'comments_helper_googleplus.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'googleplus')] = ns

    ns = runtime.TemplateNamespace(u'facebook', context._clean_inheritance_tokens(), templateuri=u'comments_helper_facebook.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'facebook')] = ns

    ns = runtime.TemplateNamespace(u'muut', context._clean_inheritance_tokens(), templateuri=u'comments_helper_muut.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'muut')] = ns

    ns = runtime.TemplateNamespace(u'disqus', context._clean_inheritance_tokens(), templateuri=u'comments_helper_disqus.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'disqus')] = ns

    ns = runtime.TemplateNamespace(u'intensedebate', context._clean_inheritance_tokens(), templateuri=u'comments_helper_intensedebate.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'intensedebate')] = ns

    ns = runtime.TemplateNamespace(u'isso', context._clean_inheritance_tokens(), templateuri=u'comments_helper_isso.tmpl', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'isso')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_form(context,url,title,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system = context.get('comment_system', UNDEFINED)
        livefyre = _mako_get_namespace(context, 'livefyre')
        googleplus = _mako_get_namespace(context, 'googleplus')
        facebook = _mako_get_namespace(context, 'facebook')
        muut = _mako_get_namespace(context, 'muut')
        disqus = _mako_get_namespace(context, 'disqus')
        intensedebate = _mako_get_namespace(context, 'intensedebate')
        isso = _mako_get_namespace(context, 'isso')
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system == 'disqus':
            __M_writer(u'        ')
            __M_writer(unicode(disqus.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'livefyre':
            __M_writer(u'        ')
            __M_writer(unicode(livefyre.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'intensedebate':
            __M_writer(u'        ')
            __M_writer(unicode(intensedebate.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'muut':
            __M_writer(u'        ')
            __M_writer(unicode(muut.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'googleplus':
            __M_writer(u'        ')
            __M_writer(unicode(googleplus.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'facebook':
            __M_writer(u'        ')
            __M_writer(unicode(facebook.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'isso':
            __M_writer(u'        ')
            __M_writer(unicode(isso.comment_form(url, title, identifier)))
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link(context,link,identifier):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system = context.get('comment_system', UNDEFINED)
        livefyre = _mako_get_namespace(context, 'livefyre')
        googleplus = _mako_get_namespace(context, 'googleplus')
        facebook = _mako_get_namespace(context, 'facebook')
        muut = _mako_get_namespace(context, 'muut')
        disqus = _mako_get_namespace(context, 'disqus')
        intensedebate = _mako_get_namespace(context, 'intensedebate')
        isso = _mako_get_namespace(context, 'isso')
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system == 'disqus':
            __M_writer(u'        ')
            __M_writer(unicode(disqus.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'livefyre':
            __M_writer(u'        ')
            __M_writer(unicode(livefyre.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'intensedebate':
            __M_writer(u'        ')
            __M_writer(unicode(intensedebate.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'muut':
            __M_writer(u'        ')
            __M_writer(unicode(muut.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'googleplus':
            __M_writer(u'        ')
            __M_writer(unicode(googleplus.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'facebook':
            __M_writer(u'        ')
            __M_writer(unicode(facebook.comment_link(link, identifier)))
            __M_writer(u'\n')
        elif comment_system == 'isso':
            __M_writer(u'        ')
            __M_writer(unicode(isso.comment_link(link, identifier)))
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comment_link_script(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        comment_system = context.get('comment_system', UNDEFINED)
        livefyre = _mako_get_namespace(context, 'livefyre')
        googleplus = _mako_get_namespace(context, 'googleplus')
        facebook = _mako_get_namespace(context, 'facebook')
        muut = _mako_get_namespace(context, 'muut')
        disqus = _mako_get_namespace(context, 'disqus')
        intensedebate = _mako_get_namespace(context, 'intensedebate')
        isso = _mako_get_namespace(context, 'isso')
        __M_writer = context.writer()
        __M_writer(u'\n')
        if comment_system == 'disqus':
            __M_writer(u'        ')
            __M_writer(unicode(disqus.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'livefyre':
            __M_writer(u'        ')
            __M_writer(unicode(livefyre.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'intensedebate':
            __M_writer(u'        ')
            __M_writer(unicode(intensedebate.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'muut':
            __M_writer(u'        ')
            __M_writer(unicode(muut.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'googleplus':
            __M_writer(u'        ')
            __M_writer(unicode(googleplus.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'facebook':
            __M_writer(u'        ')
            __M_writer(unicode(facebook.comment_link_script()))
            __M_writer(u'\n')
        elif comment_system == 'isso':
            __M_writer(u'        ')
            __M_writer(unicode(isso.comment_link_script()))
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"23": 4, "26": 7, "29": 8, "32": 6, "35": 3, "38": 5, "41": 9, "44": 0, "49": 2, "50": 3, "51": 4, "52": 5, "53": 6, "54": 7, "55": 8, "56": 9, "57": 27, "58": 45, "59": 63, "65": 11, "77": 11, "78": 12, "79": 13, "80": 13, "81": 13, "82": 14, "83": 15, "84": 15, "85": 15, "86": 16, "87": 17, "88": 17, "89": 17, "90": 18, "91": 19, "92": 19, "93": 19, "94": 20, "95": 21, "96": 21, "97": 21, "98": 22, "99": 23, "100": 23, "101": 23, "102": 24, "103": 25, "104": 25, "105": 25, "111": 29, "123": 29, "124": 30, "125": 31, "126": 31, "127": 31, "128": 32, "129": 33, "130": 33, "131": 33, "132": 34, "133": 35, "134": 35, "135": 35, "136": 36, "137": 37, "138": 37, "139": 37, "140": 38, "141": 39, "142": 39, "143": 39, "144": 40, "145": 41, "146": 41, "147": 41, "148": 42, "149": 43, "150": 43, "151": 43, "157": 47, "169": 47, "170": 48, "171": 49, "172": 49, "173": 49, "174": 50, "175": 51, "176": 51, "177": 51, "178": 52, "179": 53, "180": 53, "181": 53, "182": 54, "183": 55, "184": 55, "185": 55, "186": 56, "187": 57, "188": 57, "189": 57, "190": 58, "191": 59, "192": 59, "193": 59, "194": 60, "195": 61, "196": 61, "197": 61, "203": 197}, "uri": "comments_helper.tmpl", "filename": "/Users/Falaize/anaconda/lib/python2.7/site-packages/nikola/data/themes/base/templates/comments_helper.tmpl"}
__M_END_METADATA
"""
