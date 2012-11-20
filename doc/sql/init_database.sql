create user zarkpy identified by 'zarkpy_db_password';
grant all privileges on zarkpy.* to zarkpy@'localhost' identified by 'zarkpy_db_password';
flush privileges;
CREATE DATABASE zarkpy;
