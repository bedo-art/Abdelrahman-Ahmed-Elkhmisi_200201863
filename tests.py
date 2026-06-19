import unittest
import database


class TestLibrarySystem(unittest.TestCase):

    def test_database_connection(self):
        conn = database.get_connection()

        self.assertIsNotNone(conn)

        conn.close()


    def test_tables_creation(self):
        database.create_tables()

        conn = database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        tables = cursor.fetchall()

        conn.close()

        table_names = [table[0] for table in tables]

        self.assertIn("books", table_names)
        self.assertIn("members", table_names)
        self.assertIn("borrowings", table_names)



if __name__ == "__main__":
    unittest.main()