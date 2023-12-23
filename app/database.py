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
    def all(sortBy = None, filters = []):
        conn, cur = DB.__cursor()
        query = "SELECT * FROM cars"

        whereClauses = []
        params = []
        for f in filters:
            match f:
                case (_, None) | (_, None, None):
                    continue
                case (col, None, max):
                    whereClauses.append(f"{col} <= %s")
                    params.append(max)
                case (col, min, None):
                    whereClauses.append(f"{col} >= %s")
                    params.append(min)
                case (col, min, max):
                    whereClauses.append(f"{col} >= %s AND {col} <= %s")
                    params.append(min, max)
                case (col, like):
                    whereClauses.append(f"{col} LIKE %s")
                    params.append(like)

        if whereClauses:
            query = f"{query} WHERE {' AND '.join(whereClauses)}" 

        if sortBy:
            query = f"{query} ORDER BY {sortBy[0]} {sortBy[1]}"

        query = f"{query};"

        cur.execute(query, params)
        res = cur.fetchall()
        DB.__close(conn, cur)

        return [Car.parse_obj(r) for r in res]

