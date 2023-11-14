PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE sound (emoji text not null, file text not null);
COMMIT;
