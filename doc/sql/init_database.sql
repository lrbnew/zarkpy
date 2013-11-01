CREATE USER homework IDENTIFIED BY 'homework_db_password';
GRANT ALL PRIVILEGES ON homework.* TO homework@'localhost' IDENTIFIED BY 'homework_db_password';
GRANT ALL PRIVILEGES ON homework_test.* TO homework@'localhost' IDENTIFIED BY 'homework_db_password';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS homework;
CREATE DATABASE IF NOT EXISTS homework_test;
