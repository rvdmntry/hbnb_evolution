# HBnB API

## Overview

The HBnB API is a RESTful web service for managing a platform similar to AirBnB. It provides endpoints for managing users, places, cities, countries, amenities, and reviews. The API is built using Python, Flask, and Flask-Restx for documentation.

## Features

- **User Management**: Create, retrieve, update, and delete users.
- **Place Management**: Create, retrieve, update, and delete places. Places can be linked to cities and amenities.
- **City Management**: Create, retrieve, update, and delete cities. Cities are linked to countries.
- **Country Management**: Retrieve pre-loaded country data.
- **Amenity Management**: Create, retrieve, update, and delete amenities.
- **Review Management**: Create, retrieve, update, and delete reviews. Reviews are linked to users and places.

## Endpoints

### Users

- **POST /users**: Create a new user.
- **GET /users**: Retrieve a list of all users.
- **GET /users/{user_id}**: Retrieve details of a specific user.
- **PUT /users/{user_id}**: Update an existing user.
- **DELETE /users/{user_id}**: Delete a user.

### Places

- **POST /places**: Create a new place.
- **GET /places**: Retrieve a list of all places.
- **GET /places/{place_id}**: Retrieve detailed information about a specific place.
- **PUT /places/{place_id}**: Update an existing place’s information.
- **DELETE /places/{place_id}**: Delete a specific place.

### Cities

- **POST /cities**: Create a new city.
- **GET /cities**: Retrieve a list of all cities.
- **GET /cities/{city_id}**: Retrieve details of a specific city.
- **PUT /cities/{city_id}**: Update an existing city’s information.
- **DELETE /cities/{city_id}**: Delete a specific city.
- **GET /countries/{country_code}/cities**: Retrieve all cities belonging to a specific country.

### Countries

- **GET /countries**: Retrieve all pre-loaded countries.
- **GET /countries/{country_code}**: Retrieve details of a specific country by its code.

### Amenities

- **POST /amenities**: Create a new amenity.
- **GET /amenities**: Retrieve a list of all amenities.
- **GET /amenities/{amenity_id}**: Retrieve detailed information about a specific amenity.
- **PUT /amenities/{amenity_id}**: Update an existing amenity’s information.
- **DELETE /amenities/{amenity_id}**: Delete a specific amenity.

### Reviews

- **POST /places/{place_id}/reviews**: Create a new review for a specified place.
- **GET /users/{user_id}/reviews**: Retrieve all reviews written by a specific user.
- **GET /places/{place_id}/reviews**: Retrieve all reviews for a specific place.
- **GET /reviews/{review_id}**: Retrieve detailed information about a specific review.
- **PUT /reviews/{review_id}**: Update an existing review.
- **DELETE /reviews/{review_id}**: Delete a specific review.

## Data Format

### User

- **POST and PUT Requests**: JSON payload with `email`, `first_name`, and `last_name`.
- **GET Responses**: Include `id`, `email`, `first_name`, `last_name`, `created_at`, and `updated_at`.

### Place

- **POST and PUT Requests**: JSON payload with `name`, `description`, `address`, `city_id`, `latitude`, `longitude`, `host_id`, `number_of_rooms`, `number_of_bathrooms`, `price_per_night`, `max_guests`, and `amenity_ids` (list of amenity UUIDs).
- **GET Responses**: Include all place fields along with detailed city information, and linked amenities.

### City

- **POST and PUT Requests**: JSON payload with `name` and `country_code`.
- **GET Responses**: Include `id`, `name`, `country_code`, `created_at`, and `updated_at`.

### Country

- **GET Responses**: Include `code` and `name`.

### Amenity

- **POST and PUT Requests**: JSON payload with `name`.
- **GET Responses**: Include `id`, `name`, `created_at`, and `updated_at`.

### Review

- **POST Requests**: JSON payload with `user_id`, `rating`, and `comment`.
- **GET Responses**: Include `id`, `place_id`, `user_id`, `rating`, `comment`, `created_at`, and `updated_at`.

## Validation Rules

- **Ratings**: Must be between 1 and 5.
- **City ID and Country Code**: Must refer to valid existing entities.
- **Amenities**: All provided amenity IDs must exist.
- **Non-Hosts**: Reviews must be made by users who are not the host of the place.

## Running the Application

1. **Clone the repository**:
    bash
    git clone <https://github.com/rvdmntry/holbertonschool-hbnb.git>

2. **Navigate to the project directory**:
    bash
    cd hbnb-api

3.**Install dependencies**:
    bash
    pip install -r requirements.txt
    ```

4.**Run the application**:
    bash
    python3 app.py
    ```

5.**Access API documentation**:
    Navigate to `http://localhost:5000/` to view the interactive API documentation.

## Running Tests

To run the tests, use the following command:

```bash
python3 -m unittest discover -s tests
