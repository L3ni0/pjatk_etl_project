SELECT 'CREATE DATABASE bronze'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bronze');

SELECT 'CREATE DATABASE silver'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'silver')

SELECT 'CREATE DATABASE gold'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'gold')
