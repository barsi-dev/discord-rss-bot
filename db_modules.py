import feedparser
import validators

#   LEGEND:
#       actual_latest = latest in rss feed
#       saved_latest = latest in database


#   Parses an rss link and returns all chapters from actual latest to saved latest
#   RETURNS a list of dictionaries
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
            


#   Checks if the saved latest chapter is equal to the latest title of the entry.
#   RETURNS 0 if saved_latest != actual_latest
#   RETURNS 1 if feed entry is empty
#   RETURNS 1 if  saved_latest == actual_latest

#   FIX 
#       make different return values for different errors
def is_latest(row):
    url_validate = validators.url(row[0])

    if not url_validate: return 1
    
    try:
        feed = feedparser.parse(row[0])
    except:
        print("An error occured! Check error logs!")

    # Checks if feed has an entry
    if not feed.entries: return 1
    
    # Return TRUE if latest chapter in entry is equal to saved latest
    return 1 if feed.entries[0].title == row[1] else 0


#   Checks if the link passed is a valid rss link and 
#   RETURNS feed
def is_valid_rss(link):
    url_validate = validators.url(link)

    if not url_validate: return 0

    feed = feedparser.parse(link)

    if not feed.entries: return 0
    
    return feed

#   Checks if link is in database
#   USED BY add_to_db()
#   RETURNS 0 if link is not found
#   RETURNS 1 if link is found
def link_in_database(database, link):
    cursor = database.cursor()

    cursor.execute(F"SELECT COUNT(1) FROM feeds WHERE link=\"{link}\"")
    result = cursor.fetchone()[0]

    cursor.close()

    return result

#   USED when an "!!rss" is invoked
#   Returns the actual_latest without "Chapter #"
#   FIX
#       Add a row to feeds with latest using feed.title
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

    #    Error can be ignored
    # notes a type mismatch but it is due
    latest = feed.entries[0].title

    cursor.execute(F"INSERT INTO feeds (link, latest) VALUES (\"{link}\", \"{latest}\")")
    database.commit()

    cursor.close()
    return latest.rsplit(' ', 2)[0]

# IF RSS LINK IS VALID RETURN THE PARSED ENTRIES
# ELSE RETURN 0

