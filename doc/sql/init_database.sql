CREATE USER zarkpy IDENTIFIED BY 'zarkpy_db_password';
GRANT ALL PRIVILEGES ON zarkpy.* TO zarkpy@'localhost' IDENTIFIED BY 'zarkpy_db_password';
GRANT ALL PRIVILEGES ON zarkpy_test.* TO zarkpy@'localhost' IDENTIFIED BY 'zarkpy_db_password';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS zarkpy;
CREATE DATABASE IF NOT EXISTS zarkpy_test;
