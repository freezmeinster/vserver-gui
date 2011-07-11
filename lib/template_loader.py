from jinja2 import Template, Environment, FileSystemLoader
import os.path

def render(template_name, data={},url_name=''):
        data['current_url'] = url_name
	path = os.path.join(os.path.dirname(__file__), '../view')
	env = Environment(loader=FileSystemLoader(path))
	tmpl = env.get_template(template_name)
	return tmpl.render(data)
