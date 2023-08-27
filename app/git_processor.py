import subprocess
from abc import ABC, abstractmethod

DB_BRANCH = "database/podcasts"


class GitDatabaseBase(ABC):
    @abstractmethod
    def pull(self) -> None:
        pass

    @abstractmethod
    def run_cmd(self, cmd: list[str], critical: bool = True) -> str:
        pass

    @abstractmethod
    def commit(self, filename: str) -> None:
        pass


class GitDatabase(GitDatabaseBase):
    def __init__(self) -> None:
        self.run_cmd(["git", "checkout", DB_BRANCH])

    def pull(self) -> None:
        self.run_cmd(["git", "pull"])

    def run_cmd(self, cmd: list[str], critical: bool = True) -> str:
        status = subprocess.run(cmd)

        if status.returncode != 0 and critical:
            stderr = status.stderr.decode() if status.stderr is not None else ""
            raise RuntimeError(
                f"Error when executing command {cmd}: "
                + f"{stderr}; return: {status.returncode}"
            )

        return status.stdout.decode() if status.stdout is not None else ""

    def commit(self, filename: str) -> None:
        self.run_cmd(["git", "pull"])
        self.run_cmd(["git", "add", f"database/{filename}"])
        self.run_cmd(
            [
                "git",
                "-c",
                'user.name="DonatasTamosauskas"',
                "-c",
                "user.email=donatas.tamosauskas@gmail.com",
                "commit",
                "-m",
                f'"auto: add file {filename} to the database"',
            ]
        )
        self.run_cmd(["git", "push"])


class GitDatabaseMock(GitDatabaseBase):
    def pull(self) -> None:
        print("INFO: Mocked git PULL attempted.")

    def run_cmd(self, cmd: list[str], critical: bool = True) -> str:
        print(f"INFO: Mocked git cmd: {' '.join(cmd)} attempted.")
        return ""

    def commit(self, filename: str) -> None:
        print(f"INFO: Mocked git commit of file: {filename} attempted.")
