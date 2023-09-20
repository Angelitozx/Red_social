CREATE DATABASE ordinario;

--@block
USE ordinario;

--@block
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    correo VARCHAR(30),
    username VARCHAR(15) NOT NULL,
    name VARCHAR(20) NOT NULL,
    apellido_paterno VARCHAR(20),
    apellido_materno VARCHAR(20),
    password VARCHAR(15) NOT NULL,
    telefono VARCHAR(15),
    cumpleanos DATE
);

--@block
CREATE TABLE imagenes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    imagen LONGBLOB
);

--@block
CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(40) NOT NULL,
    content VARCHAR(100) NOT NULL
);

--@block
DESCRIBE users
--@block
SELECT * FROM users;

--@block
SELECT * FROM imagenes

--@block
INSERT INTO users (id, name, apellido_paterno, apellido_materno, telefono, cumpleanos, correo, username, password ) VALUES (1, 'user1@gmail.com', 'user1', '1234');

--@block
DROP TABLE users;

--@block
DESCRIBE articles
--@block
SELECT * FROM articles
--@block
Drop table articulo
--@block
Drop table users

--@block
Drop DATABASE ordinario;
