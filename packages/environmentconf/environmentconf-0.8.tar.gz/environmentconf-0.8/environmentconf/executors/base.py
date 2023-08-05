import abc
import subprocess

class BaseActionRunner(abc.ABC):
    """This class base class for all the actions.

    It contains base properties and methods that action runner class need.
    """

    actions = []
    version = ""
    state = {}
    action_name = None
    change_manager = None
    
    def __init__(self, actions, action_name, change_manager) -> None:
        """The constructor for BaseActionRunner.

        It takes in the following parameters and initializes member variables.
        @param actions: Dict - List of valid actions.
        @param action_name: str - Name of the action.
        @param change_manager: ChangeManager - Change manager instance.
        """
        self.actions = actions
        self.action_name = action_name
        self.change_manager = change_manager
        self.state = {
            "state": "unknown"
        }
    
    def store_state(self):
        print("Storing state")

    @abc.abstractmethod
    def run(self, action, action_args):
        """This is an abstract method to be implemented by all child classes.

        Typically this method will run the action.
        """
        while False:
            yield None
    
    def execute(self, cmd) -> int:
        """This method executes the command on remote environments.

        @param cmd: str - Environment specific command.
        """
        result = None
        try:
            result = subprocess.run(cmd, shell=True, executable='/bin/bash')
            return result.returncode
        except Exception as ex:
            print(f"Error executing command : {cmd}")
            print(ex)
            return result.returncode
    
    def change_handler(self, action_args):
        """This method is a default implementation of post processing change when change producer action notifies subscriber action."""
        # Default change handler
        return True