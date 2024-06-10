from jinja2 import Environment, FileSystemLoader, select_autoescape

from rasadecuator.Log import Log

log_adec = Log(__name__, "/home/administrator/disk2tb/retriever/descarga_adquisiciones")


class TemplateHandler:
    """
    A class that handles rendering templates using Jinja2.

    Args:
        templates_dir (str): The directory where the templates are located.

    Attributes:
        templates_dir (str): The directory where the templates are located.
        env (jinja2.Environment): The Jinja2 environment.

    Methods:
        render_template: Renders a template with the given parameters.
        render_tmd_files: Renders TMD files using a template and writes the output to a file.
        render_ras_file: Renders RAS files using a template and writes the output to a file.
        render_ssp_input: Renders SSP input using a template and writes the output to a file.
        render_ssp_offline: Renders SSP offline using a template and writes the output to a file.
        render_ssp_offline_fast: Renders SSP offline fast using a template and writes the output to a file.
        render_offline_fast_final: Renders offline fast final using a template and writes the output to a file.
        render_offline_very_fast: Renders offline very fast using a template and writes the output to a file.
        render_online_very_fast: Renders online very fast using a template and writes the output to a file.
        render_arg1: Renders a template with no arguments and writes the output to a file.
        render_arg2: Renders a template with two arguments and writes the output to a file.
        render_arg3: Renders a template with three arguments and writes the output to a file.
    """

    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render_template(self, template_name, parameters, product_type=None):
        """
        Renders a template with the given parameters.

        Args:
            template_name (str): The name of the template file.
            parameters (list): A list of dictionaries containing the parameters for the template.
            product_type (str, optional): The type of the product. Defaults to None.

        Returns:
            str: The rendered template as a string.
        """
        template = self.env.get_template(template_name)
        return template.render(parameters=parameters, outputs=product_type)

    def render_tmd_files(self, files, template_name, output_name):
        """
        Renders TMD files using a template and writes the output to a file.

        Args:
            files (list): A list of TMD files.
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
        """
        outputs = []
        parameters = []
        for file in files:
            parameters.append(
                {"name": "TMBIN", "type": "XPNetStringNotTimeTagged", "value": file}
            )
        output = self.render_template(template_name, parameters)
        outputs.append(output)
        with open(output_name, "w") as f:
            f.write(output)

    def render_ras_file(self, ras_files, dttl_file, template_name, output_name):
        """
        Renders RAS files using a template and writes the output to a file.

        Args:
            ras_files (list): A list of RAS files.
            dttl_file (str): The DTTL file.
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
        """
        parameters = [
            {
                "name": "Acquisition Timeline Product",
                "type": "XPNetStringNotTimeTagged",
                "value": dttl_file,
            }
        ]
        for file in ras_files:
            parameters.append(
                {
                    "name": "RAS Product",
                    "type": "XPNetStringNotTimeTagged",
                    "value": file,
                }
            )
        output = self.render_template(template_name, parameters)
        with open(output_name, "w") as f:
            f.write(output)

    def render_ssp_input(
        self, template_name, output_name, att_product, precision_product,product_type
    ):
        """
        Renders SSP input using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
        """
        parameters = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        with open(output_name, "w") as f:
            f.write(output)

    def render_ssp_offline(
        self, template_name, output_name, att_product, precision_product,product_type
    ):
        """
        Renders SSP offline using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
        """
        parameters = []
        outputs = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_ssp_offline_fast(
        self, template_name, output_name, att_product, precision_product,product_type
    ):
        """
        Renders SSP offline fast using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
        """
        parameters = []
        outputs = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_offline_fast_final(
        self, template_name, output_name, att_product, precision_product,product_type
    ):
        """
        Renders offline fast final using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
        """
        parameters = []
        outputs = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_offline_very_fast(self, template_name, output_name,product_type):
        """
        Renders offline very fast using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
        """
        outputs = []
        output = self.render_template(template_name, "",product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_online_very_fast(self, template_name, output_name,product_type):
        """
        Renders online very fast using a template and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
        """
        outputs = []
        output = self.render_template(template_name, "",product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_arg1(self, template_name, output_name,product_type):
        """
        Renders a template with no arguments and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
        """
        outputs = []
        output = self.render_template(template_name, "",product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_arg2(self, template_name, output_name, att_product, precision_product,product_type):
        """
        Renders a template with two arguments and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
        """
        parameters = []
        outputs = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)

    def render_arg3(
        self,
        template_name,
        output_name,
        att_product,
        precision_product,
        total_electron_content,
        product_type
    ):
        """
        Renders a template with three arguments and writes the output to a file.

        Args:
            template_name (str): The name of the template file.
            output_name (str): The name of the output file.
            att_product (str): The precision attitude product.
            precision_product (str): The precision orbit product.
            total_electron_content (str): The total electron content CUSS product.
        """
        parameters = []
        outputs = []
        parameters.append(
            {
                "name": "Precision Attitude Product",
                "type": "XPNetStringNotTimeTagged",
                "value": att_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Precision Orbit Product",
                "type": "XPNetStringNotTimeTagged",
                "value": precision_product,
            }
        )
        output = self.render_template(template_name, parameters,product_type)

        parameters.append(
            {
                "name": "Total Electron Content CUSS Product",
                "type": "XPNetStringNotTimeTagged",
                "value": total_electron_content,
            }
        )
        output = self.render_template(template_name, parameters,product_type)
        outputs.append(output)
        with open(output_name, "a") as f:
            f.write(output)
