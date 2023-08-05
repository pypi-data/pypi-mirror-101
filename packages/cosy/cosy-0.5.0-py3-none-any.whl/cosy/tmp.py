from pathlib import Path

import tbump.main

# @app.command()
def init():
    """create new project"""
    # shutil.which("cookiecutter")
    # shutil.which("poetry")
    # shutil.which("bump2version")

    subprocess.run(["poetry", "init"])
    # ask if is public?
    # call cookieshit?


def main():
    tbump.main()

    working_path = Path.cwd()
    new_version = "1.2.3"
    bump_options = tbump.main.BumpOptions(
        working_path=working_path, new_version=new_version
    )

    operations = ["patch", "hooks"]  # , "commit", "tag", "push_commit", "push_tag"]
    tbump.main.bump(bump_options, operations)

    # if opt_dict["--only-patch"]:
    #     operations = ["patch"]
    # if opt_dict["--no-push"]:
    #     operations.remove("push_commit")
    #     operations.remove("push_tag")
    # if opt_dict["--no-tag-push"]:
    #     operations.remove("push_tag")
    # if opt_dict["--no-tag"]:
    #     operations.remove("tag")
    #     # Also remove push_tag if it's still in the list:
    #     if "push_tag" in operations:
    #         operations.remove("push_tag")


main()
