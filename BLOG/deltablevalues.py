import sqlite3

def delete_all_table_values(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Get a list of all tables in the database
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    # Delete all values from each table
    for table in tables:
        table_name = table[0]
        cur.execute(f"DELETE FROM {table_name};")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_filename = "blog.db"  # Change this to your database file name
    delete_all_table_values(db_filename)
    print("All values have been deleted from all tables.")
