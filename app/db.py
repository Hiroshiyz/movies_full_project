from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
dbPath = "database.db"
# 創建database
engine = create_engine("sqlite:/// % s" % dbPath)
# 讓session可以綁定到不同threads
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
# 把 query 屬性加到所有繼承 Base 的 model 上


def init_db():
    import app.models
    print("Creating tables")
    Base.metadata.create_all(bind=engine)
    # 利用 metadata.create_all 方法在資料庫中創建所有資料表（如果尚未創建）。
    result = db_session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table';")
    )
    tables = result.fetchall()
    print(f"Available tables: {tables}")


if __name__ == "__main__":
    init_db()
