import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events
(
    artist VARCHAR(256),
    auth VARCHAR(16),
    firstName VARCHAR(256),
    gender VARCHAR(256),
    itemInSession INTEGER,
    lastName VARCHAR(256),
    length NUMERIC(10,4),
    level VARCHAR(8),
    location VARCHAR(256), 
    method VARCHAR(6),
    page VARCHAR(16),
    registration BIGINT,
    sessionId INTEGER,
    song VARCHAR(256),
    status INT,
    ts BIGINT,
    userAgent VARCHAR(256),
    userId INT
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs
(
    num_songs INTEGER,
    artist_id VARCHAR(20),
    artist_latitude NUMERIC(9,6), 
    artist_longitude NUMERIC(9,6),
    artist_location VARCHAR(256),
    artist_name VARCHAR(256),
    song_id VARCHAR(20),
    title VARCHAR(256),
    duration NUMERIC(10,6), 
    year INT
);
""")

songplay_table_create = ("""
CREATE TABLE songplays
(
    songplay_id INTEGER IDENTITY(0, 1) PRIMARY KEY, 
    start_time TIMESTAMP NOT NULL, 
    user_id INTEGER NOT NULL, 
    level VARCHAR(8), 
    song_id VARCHAR(20) NOT NULL, 
    artist_id VARCHAR(20) NOT NULL, 
    session_id INTEGER NOT NULL, 
    location VARCHAR(256) NOT NULL, 
    user_agent VARCHAR(256) NOT NULL
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time );
""")

user_table_create = ("""
CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY, 
    first_name VARCHAR(256) NOT NULL, 
    last_name VARCHAR(256) NOT NULL, 
    gender VARCHAR(64) ENCODE BYTEDICT NOT NULL, 
    level VARCHAR(8) ENCODE BYTEDICT NOT NULL
)
DISTSTYLE ALL
SORTKEY ( user_id );
""")

song_table_create = ("""
CREATE TABLE songs
(
    song_id VARCHAR(20) NOT NULL PRIMARY KEY, 
    title VARCHAR(256) NOT NULL, 
    artist_id VARCHAR(20) NOT NULL, 
    year INTEGER NOT NULL, 
    duration NUMERIC(8,4) NOT NULL
)
DISTSTYLE ALL
SORTKEY ( song_id );
""")

artist_table_create = ("""
CREATE TABLE artists
(
    artist_id VARCHAR(20) NOT NULL PRIMARY KEY, 
    name VARCHAR(256) NOT NULL, 
    location VARCHAR(256), 
    latitude NUMERIC(9,6), 
    longitude NUMERIC(9,6)
)
DISTSTYLE ALL
SORTKEY ( artist_id );
""")

time_table_create = ("""
CREATE TABLE time
(
    start_time TIMESTAMP NOT NULL PRIMARY KEY, 
    hour INTEGER NOT NULL, 
    day INTEGER NOT NULL, 
    week INTEGER NOT NULL, 
    month INTEGER NOT NULL, 
    year INTEGER NOT NULL, 
    weekday VARCHAR(9) ENCODE BYTEDICT NOT NULL
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time );
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events 
                          from {}
                          iam_role {}
                          json {};
                       """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs 
                          from {} 
                          iam_role {}
                          json 'auto';
                      """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
SELECT  
    TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time, 
    e.user_id, 
    e.user_level, 
    s.song_id,
    s.artist_id, 
    e.session_id,
    e.location, 
    e.user_agent
FROM staging_events e, staging_songs s
WHERE e.page = 'NextSong' 
AND e.song_title = s.title 
AND e.artist_name = s.artist_name 
AND e.song_length = s.duration
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT  
    user_id, 
    user_first_name, 
    user_last_name, 
    user_gender, 
    user_level
FROM staging_events
WHERE page = 'NextSong'
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) 
SELECT DISTINCT 
    song_id, 
    title,
    artist_id,
    year,
    duration
FROM staging_songs
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
SELECT DISTINCT 
    artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
SELECT start_time, 
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time), 
    extract(month from start_time),
    extract(year from start_time), 
    extract(dayofweek from start_time)
FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
