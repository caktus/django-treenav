BEGIN;
ALTER TABLE treenav_menuitem MODIFY link varchar(255) NOT NULL;
COMMIT;
