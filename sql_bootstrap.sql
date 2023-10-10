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
    address VARCHAR(255)
);

-- Create items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    owner_id SERIAL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(255) DEFAULT 'ACTIVE' NOT NULL,
    condition VARCHAR(255),
    type VARCHAR(255) DEFAULT 'Other' NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

-- Create exchange_requests table
CREATE TABLE exchange_requests (
    id SERIAL PRIMARY KEY,
    item_id SERIAL REFERENCES items(id),
    requester_item_id SERIAL REFERENCES items(id),
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
INSERT INTO users (name, email, password, address) VALUES
    ('John Doe', 'johndoe@example.com', 'password' , '123 Main Street, Anytown, CA 91234'),
    ('Tom Harris', 'tomharris@live.com', 'password', '234 Fifth Street, Something, CA 91244'),
    ('Peter Smith', 'petersmith@gmail.com', 'password', '234 Elm Avenue, Apt 3B, Pleasantville, CA 91244'),
    ('Jane Doe', 'janedoe@example.com', 'password', '123 Pine Street, Unit 5C, Sunnydale, CA 91244'),
    ('Tony Luo', 'tonyluo@example.com', 'password', '789 Oak Avenue, Apartment 7D, Meadowville, CA 91240'),
    ('Mary Johnson', 'maryjohnson@example.com', 'password', '890 Cedar Court, Unit 2A, Lakeview, CA 91234')
;

-- Populate items table
INSERT INTO items (name,type, description, image_url, status, condition, owner_id) VALUES
    ('Book', 'BOOK', 'This is a book.', 'https://storage.googleapis.com/item-exchange/item-images/book.jpeg', 'ACTIVE', 'NEW', 1),
    ('Phone', 'ELECTRONICS', 'This is a phone.', 'https://storage.googleapis.com/item-exchange/item-images/phone.jpg', 'ACTIVE', 'USED', 2),
    ('Computer', 'ELECTRONICS', 'This is a computer.', 'https://storage.googleapis.com/item-exchange/item-images/computer.jpeg','ACTIVE', 'NEW', 3),
    ('Car', 'VEHICLE','This is a car.', 'https://storage.googleapis.com/item-exchange/item-images/car.webp', 'ACTIVE', 'NEW', 4),
    ('Sneaker', 'APPAREL', 'Not Adidas', 'https://storage.googleapis.com/item-exchange/item-images/shoes.jpeg','SWAPPED', 'USED', 1)
;
-- Populate item exchange table

INSERT INTO exchange_requests (item_id, requester_item_id, status, address, shipping_type)
VALUES
    (1, 2, 'PENDING', '123 Main Street, Anytown, CA 91234', 'UPS'),
    (2, 3, 'approved', '456 Elm Street, Nowhere, TX 78901', 'FedEx'),
    (3, 1, 'PENDING', '789 Oak Street, Anywhere, FL 32102', 'USPS'),
    (1, 3, 'REJECTED', '789 Oak Street, Anywhere, FL 32102', 'USPS')
;


INSERT INTO comments (content, exchange_request_id, user_id, created_at)
VALUES
  ('Is this new?', 1, 2, CURRENT_TIMESTAMP),
  ('It is used, but condition is like new', 1, 1, CURRENT_TIMESTAMP),
  ('Okay I will take it', 1, 2, CURRENT_TIMESTAMP),
  ('Where are you? ', 1, 2, CURRENT_TIMESTAMP),
  ('I am in San Francisco', 1, 1, CURRENT_TIMESTAMP),
  ('Pending with other exchange', 2, 2, CURRENT_TIMESTAMP)
;

DROP USER IF EXISTS lien_dao;
CREATE USER lien_dao WITH PASSWORD 'dummy';
GRANT ALL PRIVILEGES ON DATABASE hb_item_exchange TO lien_dao;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lien_dao;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO lien_dao;