--- Create database
DROP DATABASE IF EXISTS hb_item_exchange;
CREATE DATABASE hb_item_exchange;

\connect hb_item_exchange;

-- Create tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS exchange_requests;
DROP TABLE IF EXISTS comments;

-- Create users table

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(64) NOT NULL
);

-- Create items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    owner_id SERIAL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

-- Create exchange_requests table
CREATE TABLE exchange_requests (
    id SERIAL PRIMARY KEY,
    item_id SERIAL REFERENCES items(id),
    requester_user_id SERIAL REFERENCES users(id),
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    address VARCHAR(255),
    shipping_type VARCHAR(255)
);

-- Create comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exchange_request_id SERIAL REFERENCES exchange_requests(id),
    user_id SERIAL REFERENCES users(id)
);

CREATE TABLE item_locations (
  id SERIAL PRIMARY KEY,
  item_id SERIAL REFERENCES items(id),
  geohash VARCHAR(20) NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL
);

-- Populate users table
INSERT INTO users (name, email, password, salt) VALUES
    ('John Doe', 'johndoe@example.com', 'password' , 'salt'),
    ('Jane Doe', 'janedoe@example.com', 'password', 'salt'),
    ('Peter Smith', 'petersmith@example.com', 'password', 'salt'),
    ('Mary Johnson', 'maryjohnson@example.com', 'password', 'salt')
;

-- Populate items table
INSERT INTO items (name, description, image_url, owner_id) VALUES
    ('Book', 'This is a book.', 'https://storage.googleapis.com/item-exchange/item-images/book.jpeg', 1),
    ('Phone', 'This is a phone.', 'https://storage.googleapis.com/item-exchange/item-images/phone.jpg', 2),
    ('Computer', 'This is a computer.', 'https://storage.googleapis.com/item-exchange/item-images/computer.jpeg', 3),
    ('Car', 'This is a car.', 'https://storage.googleapis.com/item-exchange/item-images/car.webp', 4),
    ('Sneaker', 'Not Adidas', 'https://storage.googleapis.com/item-exchange/item-images/shoes.jpeg', 1)
;

DROP USER IF EXISTS lien_dao;
CREATE USER lien_dao WITH PASSWORD 'dummy';
GRANT ALL PRIVILEGES ON DATABASE hb_item_exchange TO lien_dao;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lien_dao;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO lien_dao;