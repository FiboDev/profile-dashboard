-- CREATE DATABASE IF NOT EXISTS factored_employees --
SELECT 'CREATE DATABASE factored_employees'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'factored_employees')\gexec
