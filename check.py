from jinja2 import Template
string = open('templates/email/email.html','rb')
template = Template(string)
print(template.render({'apikey':'6969420'}))