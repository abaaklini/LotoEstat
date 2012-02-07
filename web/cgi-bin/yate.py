
from string import Template

def start_response(resp="text/html"):
    return('Content-type: ' + resp + '\n\n')

def include_header(the_title):
    headf = open('../templates/header.html')
    head_text = headf.read()
    header = Template(head_text)
    headf.close()
    return(header.substitute(title=the_title))

def include_footer(the_links):
    footf = open('../templates/footer.html')
    foot_text = footf.read()
    link_string = ''
    if isinstance(the_links, dict):
        for key in the_links:
            link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    else:
        link_string += the_links

    footer = Template(foot_text)
    footf.close()
    return(footer.substitute(links=link_string))

def start_form(legend, the_url, form_type="POST"):
    form = '\n<form action="' + the_url + '" method="' + form_type + '">\n<fieldset>\n <legend>' + legend + '</legend>'
    return(form)

def end_form(submit_msg="Submit"):
    return('<div class="clearfix"><div class="input"><input type=submit value="' + submit_msg + '"></div></div></fieldset></form>')

def radio_button(rb_name, rb_value):
    return('<input type="radio" name="' + rb_name +
                             '" value="' + rb_value + '"> ' + rb_value + '<br />')
def drop_box(drop_title, drop_name, op_dict, selected):
    dropbox = '\n<div class="clearfix">'
    dropbox += '\n<label for="' + drop_name + '">' + drop_title + '</label>'
    dropbox += '\n<div class="input">'
    dropbox += ' \n<select name="' + drop_name + '" id="' + drop_name + '">' 
    for key, value in op_dict.items():
        dropbox += '\n<option value="' + key + '"'
        if key == selected:
            dropbox += 'selected'
        dropbox += '>' + value + '</option>'
    dropbox += '</select>\n</div>\n</div>'
    return dropbox

def u_list(items):
    u_string = '<ul>'
    for item in items:
        u_string += '<li>' + item + '</li>'
    u_string += '</ul>'
    return(u_string)

def header(header_text, header_level=2):
    return('<h' + str(header_level) + '>' + header_text +
           '</h' + str(header_level) + '>')

def para(para_text):
    return('<p>' + para_text + '</p>') 

def start_tb (hd_list):
    table = '<table class="condensed-table"><tr>'
    for el in hd_list:
        table += '<th>' + str(el) + '</th>'
    table += '</tr>'
    return table

def end_tb():
    return ('</table>')

def inner_tb(row_list):
    table = '<tr>'
    for el in row_list:
        table += '<td>' + str(el) + '</td>'
    table += '</tr>'
    return table

def open_div(Class):
    return ('<div class=' + Class + '>')

def close_div():
    return ('</div>')
