-- Prepares a MySQL server for the HBNB.
-- A db hbtn_dev_db
CREATE DATABASE IF NOT EXISTS 'hbtn_dev_db';

-- A new user hbnb_dev (in localhost)
-- Password for hbnbn dev called hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- hbnb_dev all privileges ONLY for db hbnb_dev_db
GRANT ALL PRIVILEGES ON 'hbnb_dev_db'.* TO 'hbnb_dev'@'localhost';
-- hbnb_dev SELECT privileges ONLY on db performance_schema
GRANT SELECT ON 'performance_schema'.* TO 'hbnb_dev'@'localhost';
