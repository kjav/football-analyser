1. install ruby-dev and libsqlite3-dev with apt-get
2. gem install sportdb
3. sportdb new max


TODO: We may need to transfer this data to the postgres database. It is easy to create a dump
file (an giant sql query which puts all the data into another database):

sqlite3 sport.db .dump > dump.sql

However, some of the datatypes of sqlite may not match up with the datatypes of postgres.
