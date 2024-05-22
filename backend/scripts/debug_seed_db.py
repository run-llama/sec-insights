# pip install python-dotenv
from dotenv import load_dotenv; load_dotenv()
import os

# 设置工作目录
def setup_workdir(path: str = ".")->str:
    try:
        work_dir = os.environ["WORK_DIR"]
    except KeyError:
        work_dir = os.path.abspath(path)
    os.chdir(work_dir)
    print(f"WORK_DIR: {os.getcwd()}")
    return work_dir

if __name__ == "__main__":
    # 必须设置工作目录是backend
    setup_workdir(os.path.dirname(__file__)+"/..")
    from scripts.seed_db import seed_db
    from fire import Fire

    Fire(seed_db)
