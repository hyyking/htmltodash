from typing import List

#Lib------------------------------------------------------------------------------------------------------------------------------------------------------

from html.parser import HTMLParser

#Samplepage------------------------------------------------------------------------------------------------------------------------------------------------------

page = open('scratch.html', 'r')

#Tag lists------------------------------------------------------------------------------------------------------------------------------------------------------

useless_headers = ['html','head','meta', 'link', 'title', 'base', 'script', '!DOCTYPE html']
selfclosing = ['area','base','br','col', 'command', 'embed', 'hr','input', 'keygen', 'link', 'menuitem', 'meta', 'param','source', 'track', 'wbr']
body = ['body']
link = ['a']

#Idents------------------------------------------------------------------------------------------------------------------------------------------------------

ident_text = '	'
ident_lvl = 0

#Writing Fs------------------------------------------------------------------------------------------------------------------------------------------------------

class htmlAttribute():
    def __init__(self, attribute_string):
        components = attribute_string.split(':')
        self.value = components[1]

        key_words = components[0].split('-')

        #loop by reference
        if len(key_words) >= 2:
            for i in range(1, len(key_words)):
                key_words[i] = key_words[i].capitalize()

        self.key = ''.join(key_words)

def htmlString(string:str) -> str:
    attributes:list = string.split(';')
    htmlAttributes:List[htmlAttribute] = []

    for attribute_str in attributes:
        if attribute_str != '':
            htmlAttributes.append(htmlAttribute(attribute_str))

    style = dict()
    for attribute in htmlAttributes:
        style[attribute.key] = attribute.value

    return str(style)

def input(tag, attrs):
    global ident_lvl

    att = dict(attrs)

    start = ''

    #if useless
    if tag in useless_headers or tag in selfclosing:
        ident_lvl = ident_lvl
        return

    #if the tag is the body
    elif tag in body:
        ident = ident_text * ident_lvl
        x = att.get('style', '')
        start = '(id=\''+ att.get('id','') +'\', className=\''+ att.get('class','') +'\',style=' + htmlString(att.get('style','')) + ', children=['

        ident_lvl = ident_lvl + 1
        return parser.result.write('app.layout = ' + ident + 'html.' + 'div'.title() + start + '\n')

    elif tag in link:
        ident = ident_text * ident_lvl
        start = '(id=\''+ att.get('id','') +'\', className=\''+ att.get('class','') +'\', href=\''+ att.get('href','') +'\', style=' + htmlString(att.get('style','')) + ', children=['
        ident_lvl = ident_lvl + 1
        return parser.result.write(ident + 'html.' + tag.title() + start + '\n')

    else:
        if tag != 'img':
            ident = ident_text * ident_lvl

            start = '(id=\''+ att.get('id','') +'\', className=\''+ att.get('class','') +'\',style=' + htmlString(att.get('style','')) + ', children=['
            ident_lvl = ident_lvl + 1
            return parser.result.write(ident + 'html.' + tag.title() + start + '\n')
        else:
            nonclosing(tag, att)

def output(tag):
    global ident_lvl
    end = ''

    if tag in useless_headers or tag in selfclosing:
        return

    elif tag == 'img':
        print(tag)
        ident_lvl = ident_lvl - 1
        return

    elif tag in body:
        ident_lvl = ident_lvl - 1
        ident = ident_text * ident_lvl
        end = '])'
        return parser.result.write(ident + end + '\n')

    else:
        ident_lvl = ident_lvl - 1
        ident = ident_text * ident_lvl
        end = ']),'
        return parser.result.write(ident + end + '\n')

def nonclosing(tag, att):
    global ident_lvl

    if tag == 'img':
        ident = ident_text * ident_lvl
        nonclosed = '(id=\''+ att.get('id','') +'\', className=\''+ att.get('class','') +'\', src=\''+ att.get('src','') +'\'),'
        return parser.result.write(ident +'html.' + tag.title() + nonclosed + '\n' )
    else:
        return
#Parser------------------------------------------------------------------------------------------------------------------------------------------------------

class GetTags(HTMLParser):
    result = open('rasdfesult.py', 'w')

    def handle_starttag(self, tag, attrs):
        return input(tag, attrs)

    def handle_endtag(self, tag):
        return output(tag)

    def handle_startendtag(self, tag):
        return nonclosing(tag)

if __name__ == '__main__':
    #Create Object------------------------------------------------------------------------------------------------------------------------------------------------------

    parser = GetTags()

    #Write imports------------------------------------------------------------------------------------------------------------------------------------------------------

    parser.result.write('import dash\nimport dash_core_components as dcc\nimport dash_html_components as html\n\n')

    parser.result.write('app = dash.Dash(__name__)\n\n')

    #write html------------------------------------------------------------------------------------------------------------------------------------------------------

    for line in page:
        parser.feed(line)

    #Dash Server------------------------------------------------------------------------------------------------------------------------------------------------------

    parser.result.write('\n\nif __name__ == \'__main__\':\n'+ ident_text +'app.run_server(debug=True)')

    #End of Programme------------------------------------------------------------------------------------------------------------------------------------------------------
    page.close()
    print('done')
