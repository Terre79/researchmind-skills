from common import execute
from model_download import cli

ASSETS = (
    (
        "mattersim-v1.0.0-1M.pth",
        "https://github.com/Terre79/researchmind-skills/releases/download/models-v1/mattersim-v1.0.0-1M.pth",
        "28b0b0b0f13efefee06b47ea4c9105a26bd3e2c8396da193430da96b3b49a8be",
    ),
)

if __name__ == "__main__":
    raise SystemExit(execute(lambda: cli(ASSETS)))
