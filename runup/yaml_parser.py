# Built-in
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

# 3rd Pary
import click
import yaml

# Own
from runup.version import yaml_versions
from runup import interpreter
from runup.utils import vCall, vInfo, vResponse


class ParserYAML:
    """Analizer of the `runup.yml` or `runup.yaml` file."""

    def __init__(self, context:str, verbose:bool):
        """Define the properties of the class."""
        self._context:str = context
        self._interpreter:Optional[interpreter.Interpreter] = None
        self._verbose:bool = verbose

    def parse(self)->Optional[interpreter.Interpreter]:
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """

        yaml_config:Optional[Dict[str, Union[str]]]
        vCall(self._verbose, 'ParserYAML:_read_yaml_file')
        yaml_config = self._read_yaml_file(context=self._context)
        vResponse(self._verbose, 'ParserYAML:_read_yaml_file', yaml_config)
        
        if yaml_config is None:
            return None

        vCall(self._verbose, 'ParserYAML:_get_version')
        version = self._get_version(yaml_config)
        vResponse(self._verbose, f' ParserYAML:_get_version', version)

        if version is None:
            vInfo(self._verbose, f'Version not detected')
            return None

        # Select correct interpreter
        if version.split('.')[0] == '1':
            # Initialize interpreter
            vCall(self._verbose, f' interpreter.Interpreter_1')
            my_interpreter = interpreter.Interpreter_1(
                context=Path(self._context), 
                verbose=self._verbose
            )
            vResponse(self._verbose, f'interpreter.Interpreter_1', my_interpreter)

            # Find missing parameter
            vCall(self._verbose, 'my_interpreter.missing_parameter')
            missing_parameter:Optional[str] = my_interpreter.missing_parameter(yaml_config)
            vResponse(self._verbose, f'my_interpreter.missing_parameter', missing_parameter)

            if missing_parameter is not None:
                if missing_parameter.startswith('*'):
                    click.echo(f'Parameter `{missing_parameter[1:]}` cannot be empty.')
                else:
                    click.echo(f'Missing required parameter `{missing_parameter}` on YAML file.')
                return None

            # Validate received parameters
            vCall(self._verbose, 'my_interpreter.validate_parameters')
            invalid_parameters:Optional[str] = my_interpreter.validate_parameters(yaml_config)
            vResponse(self._verbose, f'my_interpreter.validate_parameters', invalid_parameters)

            if invalid_parameters is not None:
                click.echo(f'Found invalid parameter `{invalid_parameters}` on YAML file.')
                return None

        else:
            raise RuntimeError('Impossible to detect the interpreter.')

        return my_interpreter


    def _get_version(self, config)->Union[str, None]:
        """Get the version of the runup.yaml file."""
        
        # If the version is not declared on the YAML file
        if not 'version' in config:
            click.echo('The file runup YAML should contain a version.')
            return None
        # If the version is not declared as string
        elif not isinstance(config['version'], str):
            click.echo(f"The version needs to be a string.")
            return None
        # If the version is not in the list of supported versions
        elif config['version'] not in yaml_versions:
            click.echo(f"The YAML version {config['version']} is not supported.")
            return None
        # If the version is good and and nice ;-)
        else:
            vInfo(self._verbose, f'YAML version found')

            # If it contains a dot (is a minor/specific version)
            if config['version'].find('.') > 0:
                vInfo(self._verbose, f"Info: Version {config['version']} is minor version")
                # Use the vesion defined by the user
                return config['version']
            # If doesn't contains a dot (is major/general)
            else:
                vInfo(self._verbose, f'Version is major version')
                # Use the latest minor version of this major
                found_major:bool = False
                latest_minor:Optional[str] = None
                for version in yaml_versions:
                    if version == config['version']:
                        found_major = True

                    if found_major:
                        if version.startswith(f"{config['version']}."):
                            latest_minor = version
                        elif latest_minor is not None:
                            return latest_minor

                # If this the execution reach this point, that means that the YAML
                # version indicated by the user is the last major verion 
                return yaml_versions[-1]


    def _read_yaml_file(self, context:str)->Optional[Dict[str, Union[str]]]:
        """Automatically detect a `runup.yml` or `runup.yaml` in the given context."""

        # Ensure context ends with /
        if not context.endswith('/'):
            context = f'{context}/'

        # Valid names for the YAML files
        supported_names:List[str] = [
            'runup.yaml', 'runup.yml'
        ]
        # Look for the files in the given context
        file_found:bool = False
        for filename in supported_names:
            yaml_path:Path = Path(f"{context}{filename}")
            if yaml_path.is_file():
                file_found = True
                break
        
        # Raise error if the file has not been found.
        if not file_found:
            click.echo(f'No `runup.yaml` file has been found in the given context: {context}')
            return None
        else:
            vInfo(self._verbose, f'`{file_found}` found.')

        # Return YAML file
        with open(yaml_path, 'r') as stream:
            try:
                yaml_content:Optional[Dict] = yaml.safe_load(stream)
                if yaml_content is None:
                    click.echo('The YAML file is empty. No job have been initated.')

                return yaml_content

            except yaml.parser.ParserError as error:
                where = str(error.args[3]).strip()
                msg = f'ParserError {error.args[0]} {where}'
                click.echo(msg)
                return None

            except yaml.scanner.ScannerError as error:
                where = str(error.args[3]).strip()
                msg = f'ScannerError {error.args[0]} {where}'
                click.echo(msg)
                return None
