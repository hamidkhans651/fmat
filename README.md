# Project 6: Postgres Inside Kafka with Protobuf Integration

## Overview

This project demonstrates the integration of PostgreSQL, Apache Kafka, and Protobuf in a FastAPI application. The system provides a basic mart API where products can be added, ordered, and managed. The project is containerized using Docker and orchestrated with Docker Compose.

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Protobuf Overview](#protobuf-overview)
- [Project Structure](#project-structure)

## Introduction

This project showcases a microservices architecture where the following components interact:
- **PostgreSQL**: A relational database for storing product and order information.
- **Apache Kafka**: A distributed event streaming platform used for building real-time data pipelines.
- **Protobuf**: A method developed by Google for serializing structured data, used for communication between services.

## Technologies Used

- FastAPI
- PostgreSQL
- Apache Kafka
- Protobuf
- Docker
- Docker Compose

## Prerequisites

Make sure you have the following installed on your machine:
- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/iamshoaibxyz/mart-projects.git
    cd 6-postgres-inside-kafka-protobuf
    ```

2. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Running the Application

The application consists of several services:
- **API Service**: FastAPI application providing endpoints for managing products and orders.
- **Postgres Service**: PostgreSQL database for persisting data.
- **Kafka Broker**: Apache Kafka broker for message streaming.
- **Kafka UI**: A UI to monitor Kafka topics and messages.

## API Endpoints

- `GET /`: Root endpoint with a welcome message.
- `POST /add-product`: Add a new product.
- `POST /order`: Place a new order.
- `GET /get-all-products`: Retrieve all products.
- `GET /get-products-by-category/{product_category}`: Retrieve products by category.
- `GET /get-product/{product_id}`: Retrieve a single product by ID.
- `GET /get-orders`: Retrieve all orders.
- `PATCH /increment_product_item/{product_id}`: Increment product quantity.
- `PATCH /update_product/{product_id}`: Update product details.

## Protobuf Overview

**Protobuf (Protocol Buffers)** is a language-neutral and platform-neutral mechanism for serializing structured data. Protobuf messages are defined in `.proto` files, which are compiled to generate source code in various languages.

In this project, Protobuf is used for defining the structure of messages exchanged between the FastAPI application and Kafka topics.

### Example: `mart.proto`

```proto
syntax="proto3";

message Product {
    string id = 1;
    string name = 2;
    string category = 3;
    int32 price = 4;
    int32 quantity = 5;
}

message Order {
    string product_id = 1;
    string order_id = 2;
    string product_name = 3;
    string product_category = 4;
    int32 quantity = 5;
    int32 product_price = 6;
    int32 totle_price = 7;
} 

message UpdateProduct {
    string id = 1;
    optional string name = 2;
    optional string category = 3;
    optional int32 price = 4;
    optional int32 quantity = 5;
}

message IncrementProductItem {
    string id = 1;
    int32 add_product = 2;
}
```

## Project Structure

- `app/`: Contains the main FastAPI application.
  - `main.py`: The main application logic.
  - `schema.py`: SQLModel schemas for product and order data.
  - `setting.py`: Configuration settings.
  - `mart_pb2.py`: Protobuf generated code.
- `mart.proto`: Protobuf definitions.
- `Dockerfile`: Dockerfile for building the API service.
- `.env`: Environment variables configuration file.

By following this guide, you should be able to set up and run the project successfully. For more information on specific components or issues, please refer to the respective documentation of FastAPI, PostgreSQL, Kafka, and Protobuf.