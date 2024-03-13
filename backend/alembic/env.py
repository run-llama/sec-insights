import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import settings

# 这是 Alembic Config 对象，提供对正在使用的 .ini 文件中的值的访问。
config = context.config

# 解释用于 Python 日志记录的配置文件。
# 这一行基本上设置了记录器。
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 在这里添加你的模型的 MetaData 对象
# 以支持 'autogenerate'
from app.db.base import Base  # noqa: E402

# 设置目标元数据为 Base.metadata
target_metadata = Base.metadata

# 可以通过 env.py 的需要来获取配置中的其他值：
# my_important_option = config.get_main_option("my_important_option")
# ...等等。
# 从配置中获取数据库 URL
db_url = config.get_main_option("sqlalchemy.url")
# 如果设置了环境变量中的数据库 URL，则使用它
if settings.DATABASE_URL.strip():
    db_url = settings.DATABASE_URL.strip()
    # 打印正在使用的数据库 URL
    print(f"Using DATABASE_URL {db_url} from environment for migrations")
# 将数据库 URL 设置为主要选项
config.set_main_option("sqlalchemy.url", db_url)



def run_migrations_offline() -> None:
    """以‘离线’模式运行迁移。

    这里只需配置上下文使用一个 URL，而不是一个 Engine，虽然在这里也可以接受一个 Engine。
    通过跳过 Engine 的创建，我们甚至不需要一个 DBAPI 可用。

    这里对 context.execute() 的调用会将给定的字符串发送到脚本输出。

    """
    # 配置迁移上下文
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),  # 使用配置中的数据库 URL
        target_metadata=target_metadata,  # 指定目标元数据
        literal_binds=True,  # 使用文字绑定
        dialect_opts={"paramstyle": "named"},  # 方言选项，指定参数风格为命名参数
        transaction_per_migration=True,  # 每次迁移一个事务
    )

    # 开启一个事务
    with context.begin_transaction():
        # 执行迁移
        context.run_migrations()



def do_run_migrations(connection: Connection) -> None:
    """执行迁移。

    在此场景中，我们需要创建一个 Engine 并将一个连接与上下文关联。

    """
    # 配置迁移上下文
    context.configure(
        connection=connection,  # 设置连接
        target_metadata=target_metadata,  # 指定目标元数据
        transaction_per_migration=True,  # 每次迁移一个事务
    )

    # 开启一个事务
    with context.begin_transaction():
        # 执行迁移
        context.run_migrations()


async def run_async_migrations() -> None:
    """以异步方式运行迁移。"""

    # 创建可连接对象
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # 使用异步上下文连接
    async with connectable.connect() as connection:
        # 在连接上同步运行迁移
        await connection.run_sync(do_run_migrations)

    # 处置连接
    await connectable.dispose()


def run_migrations_online() -> None:
    """以‘在线’模式运行迁移。"""

    # 运行异步迁移
    asyncio.run(run_async_migrations())


# 如果是离线模式，则运行离线迁移，否则运行在线迁移
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

