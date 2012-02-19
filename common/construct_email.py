import ast
from string import Template


def construct_html_email(email, data):
    result_map = {"html": "<ol>", "plain": ""}
    for values_set in data:
        for el in values_set:
            el_dict = ast.literal_eval(el)
            html_data = "<li><a href=%s>%s</a></li><br />" % (el_dict["link"],
                                                              el_dict["title"])
            plain_data = "%s : %s /n" % (el_dict["link"], el_dict["title"])
            result_map["html"] += html_data
            result_map["plain"] += plain_data

    #create html
    f = open("templates/email_template.html", "r")
    text = f.read()
    t = Template(unicode(text, errors='ignore'))
    text = t.substitute(links=result_map["html"] + "</ol>", keywords=[])
    result_map["html"] = text

    return result_map
