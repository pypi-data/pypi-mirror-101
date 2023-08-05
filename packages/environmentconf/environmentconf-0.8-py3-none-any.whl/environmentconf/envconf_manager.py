#! /usr/bin/env python
from os.path import isfile
import sys
import os
from .utils.command_parser import CommandParser
from .utils.config_reader import ConfigReader
from .utils.change_manager import ChangeManager
from .executors.executor_factory import ExecutorFactory

class EnvConf(object):
    """This class represents the EnvConf.

    It contains method that help start configuration of the environments.
    """

    def main(self):
        """This method start configuration of the environments."""
        cmd_parser = CommandParser()
        command_data = cmd_parser.parse()

        if command_data['command'] == "init":
            #TODO: implement init command
            # init process will create the environments.yaml from user provided values
            # if init is there then it will fill the missing information
            print("envconf init")
            return 0
        if command_data['command'] == "plan":
            #TODO: implement plan command
            # plan command is responsible for forcasting the diff between environments and local config
            print("envconf plan")
            return 0
        if command_data['command'] == "apply":
            conf_reader = ConfigReader()
            #check if all required files are in config path
            config_dir = command_data["extra_args"]["config_path"]

            if not os.path.exists(config_dir):
                print("Invalid config file path")
                return 1
            
            # read configurations.yaml
            conf_path = os.path.join(config_dir, "configurations.yaml")
            if not isfile(conf_path):
                print("Config directory does not contain configurations.yaml. Please check wiki page how to write config")
                return 1
            config = conf_reader.read(conf_path)
            
            # read environments.yaml
            conf_path = os.path.join(command_data["extra_args"]["config_path"], "environments.yaml")
            if not isfile(conf_path):
                print("Config directory does not contain environments.yaml. Please check wiki page how to write config")
                return 1
            environ = conf_reader.read(conf_path)
            
            success = True
            for group in config:
                group_name = group["hosts"]
                print("+++++ Running actions for host group: " + group_name + "\n")
                
                # get environments from environment inventory
                envs = environ[group_name]["environments"]
                for env in envs:
                    change_manager = ChangeManager()
                    
                    if env["connection_type"] == "docker":
                        print(f"++++++++++++++ Start configuring docker environment : {env['id']}\n")
                    if env["connection_type"] == "ssh":
                        print(f"++++++++++++++ Start configuring remote environment : {env['ip']}\n")

                    for action in group["actions"]:
                        print(f"Executing action `{action['name']}` using executor `{action['executor']}`")
                        factory = ExecutorFactory().get(action["executor"], env, action["name"], change_manager)
                        success = factory.run(action["action"], action["args"])
                        if not success:
                            break

                    # exit if any action returns error
                    if not success:
                        break
                    
                    # notify actions which subscribed to other actions
                    change_manager.trigger_changes()

            if not success:
                print("Failed to configure environments")
                return 1

            print("Successfully configured all the environments")
            return 0

if __name__ == "__main__":
    envConf = EnvConf()
    sys.exit(envConf.main())


