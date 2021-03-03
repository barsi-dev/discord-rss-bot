import feedparser

def get_latest_chapters(database, row):
    cursor = database.cursor()

    link = row[0]
    latest_chapter = row[1]

    return_value = []

    feed = feedparser.parse(link)
    latest_parsed_chapter = feed.entries[0].title
    if latest_parsed_chapter != latest_chapter:
        i = 0 
        while feed.entries[i].title != latest_chapter:
            new_chapter = {
                "title": feed.entries[i].title,
                "link": feed.entries[i].link
            }
            i += 1

            return_value.append(new_chapter)

    cursor.execute(f"UPDATE feeds SET latest = \"{latest_parsed_chapter}\" WHERE latest = \"{latest_chapter}\"")
    database.commit()
    
    cursor.close()
    return return_value
            

        

def is_latest(row):
    feed = feedparser.parse(row[0])
    if feed.entries:
        return 1 if feed.entries[0].title == row[1] else 0
    else:
        return 0;

def is_valid_rss(link):
    feed = feedparser.parse(link)

    if not feed.entries:
        return 0
    
    return feed


def link_in_database(database, link):
    cursor = database.cursor()

    cursor.execute(F"SELECT COUNT(1) FROM feeds WHERE link=\"{link}\"")
    result = cursor.fetchone()[0]

    cursor.close()

    return result

def add_to_db(database, link):
    cursor = database.cursor()

    result = link_in_database(database, link)
    if result:
        cursor.close()
        return 1

    feed = is_valid_rss(link)
    
    if not feed:
        cursor.close()
        return 0

    latest = feed.entries[0].title

    cursor.execute(F"INSERT INTO feeds (link, latest) VALUES (\"{link}\", \"{latest}\")")
    database.commit()

    cursor.close()
    return latest.rsplit(' ', 2)[0]

# IF RSS LINK IS VALID RETURN THE PARSED ENTRIES
# ELSE RETURN 0

