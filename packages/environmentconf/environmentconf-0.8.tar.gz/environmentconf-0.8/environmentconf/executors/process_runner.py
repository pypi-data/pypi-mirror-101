from .base import BaseActionRunner

class ProcessActionRunner(BaseActionRunner):
    """This class ProcessActionRunner.

    It contains properties and methods that handles Process specific action.
    """

    version = "1.0.0"
    
    def __init__(self, env, action_name, change_manager) -> None:
        """The constructor for ProcessActionRunner.

        It takes in the following parameters and initializes member variables.
        @param env: Dict - Environment configuration where action will configure artifact(s).
        @param action_name: str - Name of the action.
        @param change_manager: ChangeManager - Change manager instance.
        """
        self.env = env
        super().__init__([
            "start",
            "stop",
            "restart",
            "graceful-stop",
            "reload",
            "force-reload"
        ], action_name, change_manager)
    
    def run(self, action, action_args):
        """This method run the Process action type and overrides the default run implementation.
        
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

        # Check if this action need to subscribe to any change
        if "subscribe" in action_args:
            for p_action in action_args["subscribe"]:
                self.change_manager.register_subscriber(p_action, self, action_args)

        print("--------------------------- xxxxx ---------------------------")
        # Start the service
        cmd = self.get_command("process", action, action_args)
        cmd_exitcode = self.execute(cmd)
        if cmd_exitcode > 0:
            print(f"Fail to {action} service {action_args['name']}")
            self.state = {
                "state": "error",
                "exit_code": cmd_exitcode
            }
        
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
    
    def get_command(self, type, action, action_args=None):
        """This method generates the commands specifc for target environment.
        
        @param type: str - Command type
        @return str - Valid command
        """
        commands = {
            "docker": {
                "process": "docker exec {} service {} {}"
            },
            "ssh": {
                "process": "ssh root@{} service {} {}"
            }
        }
        
        command = commands[self.env["connection_type"]][type]
        if self.env["connection_type"] == "docker":
            return command.format(self.env["id"], action_args['name'], action)
        elif self.env["connection_type"] == "ssh":
            return command.format(self.env["ip"], action_args['name'], action)
    
    def change_handler(self, action_args):
        """This method is an implementation of post processing change when change producer action notifies subscriber action.
        
        @param action_args: Dict - Action arguments
        """
        # empty the subscribe array so we don't endup registering multiple
        action_args["subscribe"] = []
        return self.run("restart", action_args)