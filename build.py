import os
import subprocess

for i in os.listdir("output"):
    os.chdir(
        os.path.join("output", i),
    )
    subprocess.run(
        [
            "pipx",
            "run",
            "cibuildwheel",
            "--platform",
            "android",
            "--output-dir",
            "../../wheelhouse",
            "--archs",
            "arm64_v8",
        ],
    )
