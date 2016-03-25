migrations take the form of a file of form:

-- rambler up

// sql code to implement some table, schema, database, etc

-- rambler down

// sql code to remove and reverse the implementations in rambler up

after make this file, run the command: "rambler apply" to apply the migration,
this runs all of the sql in the rambler up bits. run the command: "rambler reverse"
to get rid of the last migration. migrations are ran in alphabetic order, so
run name the files something like: 01__asdfsadfsadf.sql, where 01 is the integer order
of the migration. so 03__migration.sql will run before 04_migration.sql.
