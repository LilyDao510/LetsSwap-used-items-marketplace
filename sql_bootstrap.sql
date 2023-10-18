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
    ('Lien Dao', 'lien.dao90@gmail.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw' , '123 Main Street, Anytown, CA 91234'),
    ('Tom Harris', 'tomharris@live.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw', '234 Fifth Street, Something, CA 91244'),
    ('Peter Smith', 'petersmith@gmail.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw', '234 Elm Avenue, Apt 3B, Pleasantville, CA 91244'),
    ('Jane Doe', 'janedoe@example.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw', '123 Pine Street, Unit 5C, Sunnydale, CA 91244'),
    ('Tony Luo', 'tonyluo@example.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw', '789 Oak Avenue, Apartment 7D, Meadowville, CA 91240'),
    ('Mary Johnson', 'maryjohnson@example.com', '$pbkdf2-sha256$12000$RQhhLKWU0vq/l3LOuffeew$FBx/PL2wdIYD0aOEIsTa8iHxNYLMMeKsrlDrDVJRrqw', '890 Cedar Court, Unit 2A, Lakeview, CA 91234')
;

-- Populate items table
INSERT INTO items (name,type, description, image_url, status, condition, owner_id) VALUES
    ('Cooking Book', 'BOOK', 'This is a cooking book.', 'https://i.pinimg.com/564x/03/e0/22/03e0223f197e133cbcfc72b9b7866b41.jpg', 'ACTIVE', 'NEW', 1),
    ('Harry Potter Book Set', 'BOOK', 'This is a set of harry potter book.', 'https://i.pinimg.com/564x/a9/f0/f0/a9f0f0e0e3c17f4cf9b8ec1e46ac68b9.jpg', 'ACTIVE', 'USED', 1),
    ('Jogging Sneaker', 'CLOTHING', 'shoes, not Adidas', 'https://i.pinimg.com/564x/fe/e4/e3/fee4e33a6f8bdaac26568bd6249d3447.jpg','SWAPPED', 'USED', 1),
    ('Iphone 13 Pro', 'ELECTRONICS', 'This is 13 apple iphone.', 'https://i.pinimg.com/564x/0b/2f/e6/0b2fe66fd8d50acfb6046ca449e1e517.jpg', 'ACTIVE', 'USED', 2),
    ('Nike T-shirt', 'CLOTHING', 'sport nike t-shirt', 'https://i.pinimg.com/564x/ce/94/aa/ce94aa53d98510e2d617a3cf6c1daed8.jpg','SWAPPED', 'NEW', 2),
    ('Banana Republic Dress', 'CLOTHING', 'beautiful dress', 'https://i.pinimg.com/564x/a4/1a/71/a41a71cc235276c8fb09309c8c0ef57b.jpg','ACTIVE', 'NEW', 3),
    ('Personal Computer HP', 'ELECTRONICS', 'This is a computer with powerful GPU.', 'https://i.pinimg.com/564x/26/31/16/263116ff7f3d5af1e08a47f4a8231a73.jpg','ACTIVE', 'NEW', 3),
    ('Sedan Car', 'VEHICLE','This is a 4 seat gasoline car.', 'https://i.pinimg.com/564x/92/99/c0/9299c0ccf6943c9db1d03bcfc1cbad1f.jpg', 'ACTIVE', 'NEW', 4),
    ('Electric Car', 'VEHICLE','This is an electric car.', 'https://i.pinimg.com/564x/02/58/36/0258361d5a6ae9be52797f52cfb5978e.jpg', 'SWAPPED', 'NEW', 4),
    ('Electric Bike', 'VEHICLE','This is a eletric bicycle.', 'https://i5.walmartimages.com/seo/Jetson-Bolt-Folding-Electric-Ride-On-with-Twist-Throttle-Cruise-Control-Up-to-15-5-mph-Black_f838c4da-51f3-48e8-87ce-930124b70a84_1.8e261ad9def3ce4769bea3fc019065ca.jpeg?odnHeight=640&odnWidth=640&odnBg=FFFFFF', 'ACTIVE', 'USED', 4),
    ('Toy Car', 'TOY', 'This is a toy car.', 'https://i.pinimg.com/564x/56/f2/c3/56f2c37b32d95aee5370db7bd1b22897.jpg', 'ACTIVE', 'NEW', 5),
    ('Toy Truck', 'TOY', 'This is a toy truck.', 'https://i.pinimg.com/564x/c8/8c/ad/c88cade5613543198127947f40631b42.jpg', 'ACTIVE', 'USED', 5),
    ('Toy Stuffed Animal', 'TOY', 'This is a toy stuffed animal.', 'https://i.pinimg.com/564x/37/15/50/371550e17d6b8d9c8f8ea35826c0c850.jpg', 'SWAPPED', 'NEW', 6),
    ('Sony Laptop', 'ELECTRONICS', 'This is a  sony laptop.', 'https://i.pinimg.com/564x/e6/ae/41/e6ae41659267f1683b575f96f38d5d9e.jpg', 'SWAPPED', 'USED', 6),
    ('Android Tablet', 'ELECTRONICS', 'This is a tablet.', 'https://i.pinimg.com/564x/49/b7/11/49b711e9a5809f30e35c9578b786f1a1.jpg', 'ACTIVE', 'NEW', 6),
    ('Samsung Smart TV', 'ELECTRONICS', 'This is a smart TV.', 'https://i.pinimg.com/564x/4f/52/4d/4f524d41e1c0c97cda47d61adf99a911.jpg', 'ACTIVE', 'NEW', 1),
    ('Nvidia Gaming Console', 'ELECTRONICS', 'This is a gaming console.', 'https://i.pinimg.com/736x/33/79/36/337936ea8f7aa3aaae9a95ea3399d959.jpg', 'ACTIVE', 'NEW', 1)

;
-- Populate item exchange table

INSERT INTO exchange_requests (item_id, requester_item_id, status, address, shipping_type)
VALUES
    (1, 9, 'PENDING', '123 Main Street, Anytown, CA 91234', 'UPS'),
    (3, 10, 'ACCEPTED', '456 Elm Street, Nowhere, TX 78901', 'FedEx'),
    (3, 11, 'PENDING', '789 Oak Street, Anywhere, FL 32102', 'USPS'),
    (9, 2, 'REJECTED', '7819 Oak Street, Anywhere, FL 32102', 'USPS'),
    (5, 2, 'PENDING', '789 Oak Street, Anywhere, FL 32102', 'FedEx')

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