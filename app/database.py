import psycopg2
from psycopg2.extras import RealDictCursor
from schemas import Car
from pydantic import parse_obj_as

DATABASE_URL = "postgresql://postgres:postgres@db/scraper"

class DB:
    @staticmethod
    def __cursor():
        conn = psycopg2.connect(
            host="db",
            database="scraper",
            user="postgres",
            password="postgres"
        )

        return conn, conn.cursor(cursor_factory=RealDictCursor)


    @staticmethod
    def __close(conn, cur):
        cur.close()
        conn.close()


    @staticmethod
    def all():
        conn, cur = DB.__cursor()

        cur.execute("SELECT * FROM cars;")
        res = cur.fetchall()
        print(res)
        DB.__close(conn, cur)

        return [Car.parse_obj(r) for r in res]

