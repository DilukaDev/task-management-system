import os
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from app.core.config import get_settings

settings = get_settings()

# Initialize a global async connection pool
pool: AsyncConnectionPool = None

async def init_pool() -> None:
    """Initialize the async connection pool."""
    global pool
    pool = AsyncConnectionPool(
        conninfo=settings.database_url,
        min_size=1,
        max_size=10,
        kwargs={"row_factory": dict_row},
        open=False
    )
    await pool.open()

async def close_pool() -> None:
    """Close the async connection pool."""
    global pool
    if pool:
        await pool.close()

async def init_db() -> None:
    """Reads the init.sql file and executes it to ensure the database schema exists."""
    if not pool:
        await init_pool()
    
    sql_file_path = os.path.join(os.path.dirname(__file__), "init.sql")
    with open(sql_file_path, "r") as f:
        sql_commands = f.read()
    
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql_commands)
        await conn.commit()

async def get_db_connection():
    """Async generator to obtain a connection from the pool."""
    async with pool.connection() as conn:
        yield conn
