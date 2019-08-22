from jinja2 import Environment, PackageLoader, select_autoescape


def generate_report_html(**kwargs):
    """
    Responsible to the write html report
    :param '**kwargs': The keyword arguments are used for the all report 
     variables
    :type 'kwargs': dict
    """
    env = Environment(
        loader=PackageLoader('report', 'templates'),
        autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('chart.html')
    name_file = "report_%s.html" % (
        "frontend" if kwargs["report"]["frontend"] else "backend") 
    with open(name_file, 'w') as f:
        f.write(template.render(**kwargs))
