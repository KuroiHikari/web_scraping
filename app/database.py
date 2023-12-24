from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor, execute_batch
from schemas import Car
from typing import Any, Dict, List, Tuple, Literal

DATABASE_URL = "postgresql://postgres:postgres@db/scraper"

Filter = Tuple[str, int | None, int | None] | Tuple[str, str | None]
Sort = Tuple[str, Literal["ASC", "DESC"]]


class DB:
    @staticmethod
    def __cursor() -> Tuple[connection, cursor]:
        conn = connect(
            host="db", database="scraper", user="postgres", password="postgres"
        )
        return conn, conn.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def __close(conn: connection, cur: cursor) -> None:
        cur.close()
        conn.close()


    @staticmethod
    def should_import() -> bool:
        conn, cursor = DB.__cursor()

        query = """
            SELECT EXISTS(
                SELECT id 
                FROM car_import_jobs 
                WHERE started_at >= current_date 
                AND started_at < current_date + interval '1 day' 
                AND finished_at IS NOT NULL
            ) as exists"""
        cursor.execute(query)
        result = cursor.fetchone()
        DB.__close(conn, cursor)
        if result:
            return not result["exists"] # type: ignore
        return True

    @staticmethod
    def mark_start_of_import() -> int | None:
        conn, cursor = DB.__cursor()

        insert_query = "INSERT INTO car_import_jobs DEFAULT VALUES returning id;"
        try:
            cursor.execute(insert_query)
            conn.commit()
            result = cursor.fetchone()
            if result:
                return result['id'] # type: ignore
        except (Exception, DatabaseError):
            conn.rollback()
        finally:
            DB.__close(conn, cursor)

    @staticmethod
    def mark_end_of_import(id: int) -> None:
        conn, cursor = DB.__cursor()

        update_query = "UPDATE car_import_jobs SET finished_at = NOW() WHERE id = %s;"
        try:
            cursor.execute(update_query, [id])
            conn.commit()
        except (Exception, DatabaseError):
            conn.rollback()
        finally:
            DB.__close(conn, cursor)

    @staticmethod
    def import_cars(tuples: List[Tuple[Any, ...]], columns: str) -> None:
        conn, cursor = DB.__cursor()
        delete_query = "DELETE FROM cars WHERE 1=1"
        insert_query = f"INSERT INTO cars({columns}) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(delete_query)
            execute_batch(cur=cursor, sql=insert_query, argslist=tuples)
            conn.commit()
        except (Exception, DatabaseError):
            conn.rollback()
            DB.__close(conn, cursor)
        DB.__close(conn, cursor)

    @staticmethod
    def all(sortBy: Sort | None = None, filters: List[Filter] = []) -> List[Car]:
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
                    params.append(min)
                    params.append(max)
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
