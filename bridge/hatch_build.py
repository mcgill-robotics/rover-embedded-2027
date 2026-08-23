import shutil
import subprocess
import sys
import warnings

from hatchling.metadata.plugin.interface import MetadataHookInterface


class GitDynamicVersionHook(MetadataHookInterface):

    def update(self, metadata):
        commit_string = ""

        # Try to use git to fetch short commit hash
        if shutil.which("git") is not None:
            process_get_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,check=False, text=True)
            if process_get_sha.returncode != 0:
                warnings.warn(f"Could not get repo path, git exit code: {process_get_sha.returncode}, skipping commit details", RuntimeWarning)
            else:
                commit_string = process_get_sha.stdout.strip()
        else:
            warnings.warn("Could not find git, skipping commit details", RuntimeWarning)

        # Add commit hash to build metadata if it exists
        build_metadata = ""
        if commit_string:
            build_metadata = f"+{commit_string}"
        
        # Generate version number
        if "version" not in self.config:
            raise KeyError("Version was not specified pyproject.toml, make sure it is placed under [tool.hatch.metadata.hooks.custom]")

        version = self.config["version"]
        metadata["version"] = f"{version}{build_metadata}"
