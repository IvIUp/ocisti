DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS cleaner;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS post;

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE cleaner (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NULL,
  last_name TEXT NULL,
--   TODO: Create new table with availabilities and make this FK
  availability TEXT NULL,
  birth_date TIMESTAMP NULL,
  location TEXT NULL,
  profile_pict TEXT NULL,
  description TEXT NULL
);

CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES cleaner (id)
);