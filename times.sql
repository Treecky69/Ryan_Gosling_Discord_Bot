PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE times(id integer primary key autoincrement, type text not null, day integer not null, hour integer not null, minute integer not null, channel integer not null, cloud text);
COMMIT;
