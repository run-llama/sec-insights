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

if  __name__ == "__main__":
    # 必须设置工作目录是backend，否则无法找到配置文件alembic.ini
    setup_workdir(os.path.dirname(__file__)+"/..")
    from app.main import start
    start()