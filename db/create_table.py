import sqlite3

con = sqlite3.connect("../tiktok.db")

with con:
    cur = con.cursor()
    cur.execute("""
              CREATE TABLE IF NOT EXISTS tiktok(
                id INT UNIQUE,
                created_at TEXT,
                title TEXT,
                width INT,
                height INT,
                duration INT,
                ratio TEXT,
                music_id INT,
                music_title TEXT,
                music_author TEXT,
                author_name TEXT
              )
              """)
    cur.execute("""
                INSERT INTO tiktok VALUES(
                3357,
                '2022',
                'test',
                360,
                1080,
                60,
                "640p",
                3357,
                "test music",
                "hoanglong",
                "hoanglont"
                )
                """)
