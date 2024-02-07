"""
Usage:
    PyPromote -h
    PyPromote --help
    PyPromote <file>

Arguments:
    <file>      YAML Instruction File

Options:
    -h, --help  Show this screen
    --version   Show Version Information
© 2023 Application Consulting Group
"""
from TM1py.Exceptions import TM1pyException
from TM1py.Services import TM1Service
from docopt import docopt
from PyPromote import PyPromoteService
from PyPromote import ReadFile
from base_settings import application_path

APP_NAME = 'PyPromote'
APP_VERSION = '2.1'
COPYRIGHT = '© 2023 Application Consulting Group'


def main(file: str):
    file = ReadFile(file=file)
    _deployment_conn = file.read_section('Server')
    _source_conn = file.read_section('Source')
    _target_con = file.read_section('Target')
    _deployment = file.read_section('Deployment')
    _deployments = file.read_section('Deployments')
    try:
        source = TM1Service(**_source_conn)
        target = TM1Service(**_target_con)
        dep_conn = TM1Service(**_deployment_conn)
        promote = PyPromoteService(source=source, target=target, server=dep_conn)
        for dep in _deployments:
            _type = _deployments[dep]['Type']
            match _type:
                case 'Dimension':
                    promote.dimension.copy_dimension(dimension=_deployments[dep]['Name'], item=dep,
                                                     deployment=_deployment)
                case 'Subset':
                    _dim, _sub = _deployments[dep]['Name'].split('|')
                    promote.dimension.copy_subset(dimension=_dim, subset=_sub, item=dep, deployment=_deployment)
                case 'Cube':
                    promote.cube.copy_cube(cube=_deployments[dep]['Name'], item=dep, deployment=_deployment)
                case 'View':
                    _cub, _vue = _deployments[dep]['Name'].split('|')
                    promote.cube.copy_view(cube=_cub, view=_vue, item=dep, deployment=_deployment)
                case 'Rules':
                    promote.cube.copy_rule(cube=_deployments[dep]['Name'], item=dep, deployment=_deployment)
                case 'Attributes':
                    promote.cube.copy_attributes(dimension=_deployments[dep]['Name'], item=dep, deployment=_deployment)
                case 'Process':
                    promote.process.copy_process(process=_deployments[dep]['Name'], item=dep, deployment=_deployment)
                case 'Chore':
                    promote.process.copy_chore(chore=_deployments[dep]['Name'], item=dep, deployment=_deployment)
                case 'RunTI':
                    promote.process.run_process(process=_deployments[dep]['Name'], params=_deployments[dep]['Params'],
                                                item=dep, deployment=_deployment)
    except TM1pyException as t:
        print(t)


if __name__ == "__main__":
    cmd_args = docopt(__doc__, version=f"{APP_NAME}, Version: {APP_VERSION} \n {COPYRIGHT}p")
    _file = cmd_args['<file>']
    main(_file)
