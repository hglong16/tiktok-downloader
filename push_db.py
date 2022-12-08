import sqlite3


def push_db(single_video):

    con = sqlite3.connect('tiktok.db')
    with con:
        cur = con.cursor()
        author = single_video['author'] if isinstance(
            single_video['author'], str) else single_video['author']['uniqueId']

        cur.execute("""
                                  INSERT or ignore INTO tiktok VALUES (?,?,?,?,?,?,?,?,?,?,?)
                                  """, (
            single_video['id'],
            single_video['createTime'],
            single_video['desc'],
            single_video['video']['width'],
            single_video['video']['height'],
            single_video['video']['duration'],
            single_video['video']['ratio'],
            single_video['music']['id'],
            single_video['music']['title'],
            single_video['music']['authorName'],
            author

        ))
