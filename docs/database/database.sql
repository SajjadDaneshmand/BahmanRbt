-- create database
CREATE DATABASE IF NOT EXISTS parts;


-- select database
USE parts;


-- create tables

CREATE TABLE IF NOT EXISTS Site(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Company(
    id INT PRIMARY KEY AUTO_INCREMENT,
    site_id INT NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY(site_id) REFERENCES Site(id)
);

CREATE TABLE IF NOT EXISTS Model(
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    name VARCHAR (255) UNIQUE NOT NULL,
    FOREIGN KEY(company_id) REFERENCES Company(id)
);

CREATE TABLE IF NOT EXISTS Product(
    id VARCHAR(255),
    model_id INT  NOT NULL,
    name VARCHAR(255) NOT NULL,
    number VARCHAR(128),
    price INT NOT NULL,
    PRIMARY KEY(id, model_id),
    FOREIGN KEY(model_id) REFERENCES Model(id)
);
