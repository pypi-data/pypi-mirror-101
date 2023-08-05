from sys import stderr
from .base import BaseActionRunner
import subprocess
import os
import hashlib

class ArtifactActionRunner(BaseActionRunner):
    """This class represents the ArtifactActionRunner

    It contains properties and methods that handles Artifact specific action.
    """

    version = "1.0.0"
    source = None
    destination = None
    mode = None
    owner = None
    servers = None
    
    def __init__(self, env, action_name, change_manager) -> None:
        """The constructor for ArtifactActionRunner.

        It takes in the following parameters and initializes member variables.
        @param env: Dict - Environment configuration where action will configure artifact(s).
        @param action_name: str - Name of the action.
        @param change_manager: ChangeManager - Change manager instance.
        """
        self.env = env
        self.action_name = action_name
        super().__init__([
            "copy",
            "delete",
            "overwrite"
        ], action_name, change_manager)
        
    def run(self, action, action_args):
        """This method run the Artifact action type and overrides the default run implementation.
        
        @param action: str - Type of the action. e.g. copy
        @param action_args: Dict - Additional action args
        """
        # check action support
        if action not in self.actions:
            print(f"Error: Unsupported action {action} found in config")
            return False

        self.state = {
            "state": "unknown",
            "exit_code": 0
        }
        print("--------------------------- xxxxx ---------------------------")
        if 'source' in action_args:
            self.source = action_args["source"]
            if not os.path.exists(self.source):
                print(f"Error: artifact {self.source} does not exist")
                return False

        if 'destination' in action_args:
            self.destination = action_args["destination"]

        if action == "copy":
            self.copy(action_args)

        if action == "delete":
            self.delete()

        if action == "overwrite":
            self.copy(action_args, True)

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

    def copy(self, action_args, force_copy=False):
        """This method copies the artifact.
        
        @param action_args: Dict - Additional action args
        """
        if 'mode' in action_args:
            self.mode = action_args["mode"]
        if 'owner' in action_args:
            self.owner = action_args["owner"]

        if not self.source or not self.destination:
            print("Error: need to specify artifact source and destination")
            return False

        # if destination is a directory, add file name
        if not os.path.basename(self.destination):
            self.destination = self.destination + \
                os.path.basename(self.source)

        # start copy
        if self.needToCopy() or force_copy:
            cmd = self.get_command("copy")
            cmd_exitcode, cmd_out = self.execute(cmd)
            if cmd_exitcode > 0:
                print(f"Error: Fail to copy file")
                # store the state
                self.state = {
                    "state": "error",
                    "exit_code": cmd_exitcode
                }
                return False

            if self.mode:
                self.changeMode()
            if self.owner:
                self.changeOwner()
        else:
            print(f"Skipping copying file as {self.destination} is up to date.")
        
        return True

    def delete(self):
        """This method deletes the artifact."""
        # check if file exist or not
        exit_code, output = self.execute(self.get_command("exist"))
        if exit_code == 0:
            print(f"File {self.destination} found, deleting it...")
            cmd_exitcode, cmd_out = self.execute(self.get_command("delete"))
            if cmd_exitcode > 0:
                print(f"Fail to delete file {self.destination}")
                self.state = {
                    "state": "error",
                    "exit_code": cmd_exitcode
                }
                return False
        else:
            print(f"Skipping file delete operation as file {self.destination} does not exist")

        return True

    def execute(self, cmd):
        """This method executes the action specific command on remote environment.
        
        @param cmd: str - Command to execute
        """
        result = None
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True, executable='/bin/bash')
            return result.returncode, result.stdout
        except Exception as ex:
            print(f"Error executing command : {cmd}")
            print(ex)
            return 1, None

    def needToCopy(self):
        """This method checks whether to copy artifact or not."""
        print(f"Checking if {self.destination} is out of date on environment")
        exit_code, output = self.execute(self.get_command("exist"))
        if exit_code > 0:
            print(f"{self.destination} does not exist")
            return True
        
        sha1sum = hashlib.sha1()
        with open(self.source, 'rb') as source:
            block = source.read(2**16)
            while len(block) != 0:
                sha1sum.update(block)
                block = source.read(2**16)

        localSha = sha1sum.hexdigest()
        exit_code, output = self.execute(self.get_command("sha1sum"))
        remoteSha = output.strip()
        if localSha != remoteSha:
            print(f"{self.destination} exist but content is not matching. Need to copy file...")
            return True
        return False

    def changeMode(self, server):
        """This method changes the mode of an artifact on remote environment."""
        return self.execute(self.get_command("filemode"))
        
    def changeOwner(self, server):
        """This method changes the owner of an artifact on remote environment."""
        return self.execute(self.get_command("fileowner"))

    def get_command(self, type):
        """This method generates the commands specifc for target environment.
        
        @param type: str - Command type
        @return str - Valid command
        """
        commands = {
            "docker": {
                "copy": "docker cp {} {}:{}",
                "exist": "docker exec {} [ -f {} ] && echo 'exist' || bla",
                "sha1sum": "docker exec {} sha1sum {} ",
                "delete": "docker exec {}  rm {}",
                "filemode": "docker exec {} chmod {} {}",
                "fileowner": "docker exec {} chown {} {}"
            },
            "ssh": {
                "copy": "scp {} root@{}:{}",
                "exist": "ssh root@{} [ -f {} ] && echo 'exist' || bla",
                "sha1sum": "ssh root@{} sha1sum {} ",
                "delete": "ssh root@{} rm {}",
                "filemode": "ssh root@{} chmod {} {}",
                "fileowner": "ssh root@{} chown {} {}"
            }
        }
        
        command = commands[self.env["connection_type"]][type]
        env = ""
        if self.env["connection_type"] == "docker":
            env = self.env["id"]
        elif self.env["connection_type"] == "ssh":
            env = self.env["ip"]

        if type == "copy":
            return command.format(self.source, env, self.destination)
        elif type == "exist" or type == "delete":
            return command.format(env, self.destination)
        elif type == "sha1sum":
            return command.format(env, self.destination) + "| awk '{ print $1 }'"
        elif type == "filemode":
            return command.format(env, self.mode, self.destination)
        elif type == "fileowner":
            return command.format(env, self.owner, self.destination)