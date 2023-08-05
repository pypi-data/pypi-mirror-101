#! /usr/bin/env python
import argparse
from typing import Dict

class CommandParser(object):
    """This class CommandParser.

    It contains properties and methods that parses the command.
    """
    
    def parse(self) -> Dict:
        """This method parses the command."""
        parser = argparse.ArgumentParser(
            description="A configuration management tool. Bootstrap & configure runtime environments.")

        parser.add_argument('-i',
                            '--init',
                            dest="init",
                            help='Initialize target configurations and validate configs',
                            metavar="KEY=VALUE",
                            nargs="+")

        parser.add_argument('-p',
                            '--plan',
                            dest="plan",
                            help='Execute and show configuration plan based on local and remote state of target runtime',
                            metavar="KEY=VALUE",
                            nargs="+")

        parser.add_argument('-a',
                            '--apply',
                            dest="apply",
                            help='Apply configurations to target runtime environments',
                            metavar="KEY=VALUE",
                            nargs="+")

        args = parser.parse_args()
        parsed_args = {}
        command = ""
        if args.init is not None:
            parsed_args = self.parse_extra_args(args.init)
            command = "init"
        if args.plan is not None:
            parsed_args = self.parse_extra_args(args.plan)
            command = "plan"
        if args.apply is not None:
            command = "apply"
            parsed_args = self.parse_extra_args(args.apply)
            # additional validation of arguments
            if "config_path" not in parsed_args:
                raise("Pass config directory path which contains configuration.yaml & environments.yaml")

        return {
            "command": command,
            "extra_args": parsed_args
        }

    def parse_extra_args(self, parsed_args):
        """This method parses the extra command arguments."""
        mapped_args = {}

        if parsed_args is None:
            return mapped_args

        for parsed_arg in parsed_args:
            split_arg = parsed_arg.split('=')
            mapped_args[split_arg[0]] = split_arg[1]
        return mapped_args