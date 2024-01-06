from jinja2 import Environment, FileSystemLoader
import os

class TemplateHandler:
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        
    def render_template(self, template_name, parameters):
        template = self.env.get_template(template_name)
        return template.render(parameters=parameters)

    def render_tmd_files(self, files, template_name, output_name):
        outputs = []
        parameters = []
        for file in files:
            # Definir algunos datos para usar en la plantilla
            parameters.append({'name': 'TMBIN', 'type': 'XPNetStringNotTimeTagged', 'value': file})
        output = self.render_template(template_name,  parameters)
        outputs.append(output)
        with open(output_name, 'w') as f:
            f.write(output)
            

    def render_ras_file(self,ras_files ,dttl_file, template_name, output_name):
        
        outputs = []
        parameters = []
        parameters.append({'name': 'Acquisition Timeline Product', 'type': 'XPNetStringNotTimeTagged', 'value': dttl_file})
        output = self.render_template(template_name,  parameters)
        for file in ras_files:
            parameters.append({'name': 'RAS Product', 'type': 'XPNetStringNotTimeTagged', 'value': file})
        output = self.render_template(template_name,  parameters)
        outputs.append(output)
        with open(output_name, 'a') as f:  # Deja 'a' para agregar al final del archivo
            f.write(output)
            
    def render_ssp_input(self,template_name,output_name,att_product,precision_product):
        parameters = []
        outputs = []
        parameters.append({'name': 'Precision Attitude Product', 'type': 'XPNetStringNotTimeTagged', 'value': att_product})
        output = self.render_template(template_name,  parameters)
        
        parameters.append({'name': 'Precision Orbit Product', 'type': 'XPNetStringNotTimeTagged', 'value': att_product})
        output = self.render_template(template_name,  parameters)
        outputs.append(output)
        with open(output_name, 'a') as f:  # Deja 'a' para agregar al final del archivo
            f.write(output)