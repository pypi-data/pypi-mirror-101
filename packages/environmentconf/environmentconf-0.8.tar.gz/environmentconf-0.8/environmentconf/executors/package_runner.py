from .base import BaseActionRunner

class PackageActionRunner(BaseActionRunner):
    """This class PackageActionRunner.

    It contains properties and methods that handles Package specific action.
    """

    version = "1.0.0"
    def __init__(self, env, action_name, change_manager) -> None:
        """The constructor for PackageActionRunner.

        It takes in the following parameters and initializes member variables.
        @param env: Dict - Environment configuration where action will configure artifact(s).
        @param action_name: str - Name of the action.
        @param change_manager: ChangeManager - Change manager instance.
        """
        self.env = env
        super().__init__([
            "install",
            "uninstall"
        ], action_name, change_manager)
        self.change_manager.register_producer(self.action_name, "UNCHANGED")
    
    def run(self, action, action_args):
        """This method run the Package action type and overrides the default run implementation.
        
        @param action: str - Type of the action. e.g. copy
        @param action_args: Dict - Additional action args
        """
        # check action support
        if action not in self.actions:
            raise(f"Error: Unsupported action {action} found in config")

        self.state = {
            "state": "unknown",
            "exit_code": 0
        }
        
        print("--------------------------- xxxxx ---------------------------")
        if action == "install":    
            # check if package installed or not
            cmd = self.get_command("check", action_args)
            cmd_exitcode = self.execute(cmd)
            if cmd_exitcode > 0:
                print(f"Package {action_args['name']} not found, installing it...")
                # update apt
                cmd = self.get_command("apt_update")
                cmd_exitcode = self.execute(cmd)

                # install package
                cmd = self.get_command("install", action_args)
                cmd_exitcode = self.execute(cmd)
                if cmd_exitcode > 0:
                    print(f"Fail to insatll package {action_args['name']}")
                    self.state = {
                        "state": "error",
                        "exit_code": cmd_exitcode
                    }
                else:
                    self.change_manager.change_state(self.action_name, "CHANGED")
            else:
                print(f"Skipping {action_args['name']} installation as it is already installed")

        if action == "uninstall":
            # check if package installed or not
            cmd = self.get_command("check", action_args)
            cmd_exitcode = self.execute(cmd)
            if cmd_exitcode == 0:
                print(f"Package {action_args['name']} found, uninstalling it...")
                cmd = self.get_command("uninstall", action_args)
                cmd_exitcode = self.execute(cmd)
                if cmd_exitcode > 0:
                    print(f"Fail to uninsatll package {action_args['name']}")
                    self.state = {
                        "state": "error",
                        "exit_code": cmd_exitcode
                    }
            else:
                print(f"Skipping {action_args['name']} uninstalltion as it is not installed")

        print("--------------------------- xxxxx ---------------------------\n")
        if self.state["exit_code"] == 0:
            self.state = {
                "state": "success",
                "exit_code": 0
            }

        # store state
        self.store_state()

        if self.state["exit_code"] == 0:
            return True

        return False
    
    def get_command(self, type, action_args=None):
        """This method generates the commands specifc for target environment.
        
        @param type: str - Command type
        @return str - Valid command
        """
        commands = {
            "docker": {
                "apt_update": "docker exec {} apt update",
                "check": "docker exec {} dpkg -l {}",
                "install": "docker exec {} bash -c 'export DEBIAN_FRONTEND=noninteractive && apt install -y {}'",
                "uninstall": "docker exec {} apt purge -y {}"
            },
            "ssh": {
                "apt_update": "ssh root@{} apt update",
                "check": "ssh root@{} dpkg -l {}",
                "install": "ssh root@{} bash -c 'export DEBIAN_FRONTEND=noninteractive && apt install -y {}'",
                "uninstall": "ssh root@{} apt purge -y {}"
            }
        }
        
        command = commands[self.env["connection_type"]][type]
        if self.env["connection_type"] == "docker":
            if type == "apt_update":
                return command.format(self.env["id"])
            return command.format(self.env["id"], action_args['name'])
        elif self.env["connection_type"] == "ssh":
            if type == "apt_update":
                return command.format(self.env["ip"])
            return command.format(self.env["ip"], action_args['name'])
            