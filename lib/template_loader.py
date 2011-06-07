from jinja2 import Template, Environment, FileSystemLoader
import os.path

def render(template_name, data=''):
	path = os.path.join(os.path.dirname(__file__), '../view')
	env = Environment(loader=FileSystemLoader(path))
	tmpl = env.get_template(template_name)
	return tmpl.render(data)
