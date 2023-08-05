from .artifact_runner import ArtifactActionRunner
from .package_runner import PackageActionRunner
from .process_runner import ProcessActionRunner

class ExecutorFactory:
    """This class ExecutorFactory.

    It is a factory implementation used to get Runner object based on type of action.
    """
    def get(self, type, env, action_name, change_manager):
        """This factory method get the action runner object based on type.
        
        @param type: str - Type of the action. e.g. package
        @param env: Dict - Target environment config
        @param action_name: str - Name of the action
        @param change_manager: obj - Change manager instance
        """
        if type == 'package':
            return PackageActionRunner(env, action_name, change_manager)

        elif type == 'artifact':
            return ArtifactActionRunner(env, action_name, change_manager)

        elif type == 'process':
            return ProcessActionRunner(env, action_name, change_manager)