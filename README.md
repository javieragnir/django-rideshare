# django-rideshare

This project implements the Rideshare coding assignment for Wingz.

## Installation
- `uv install` to install dependencies.
- `uv run python manage.py migrate` to set up the database. This project uses SQLite by default.

## Usage
- `uv run python manage.py createsuperuser [--help]` To create a superuser that you can use in the Django admin. 
- `uv run python manage.py runserver` to start the Django server.
- By default, the server runs on `127.0.0.1:8000/`.
- Visit the Django admin site at `127.0.0.1:8000/admin/`.

## API
### Routes
- Root: `127.0.0.1:8000/api/`
- Users: `127.0.0.1:8000/api/users/`
- Rides: `127.0.0.1:8000/api/rides/`
- Ride Events: `127.0.0.1:8000/api/ride-events/`


### Ride List
- The Ride List is viewable at `127.0.0.1:8000/api/rides/`.
- Filters and ordering of the Ride List are implemented with query parameters.
- e.g. `ride-events/?<param1>&<param2>

### Ride List Pagination
- By default, pagination uses `rest_framework.pagination.LimitOffsetPagination` with a page size of 100.
- Pagination can be set by using `limit=<int>` to set the page size and `offset=<int>` to the index of where to start the page.

### Ride List Filters
- Email: `email=<value>` (uses substring match)
- Status: `status=[En-route, Pickup, Dropoff]` (must be an exact string match of one of the statuses) 

### Ride List Ordering
- Use ordering like `o=pickup_time,distance` Can choose either or both pickup time or distance.
- Pickup Time: `o=pickup_time` (ascending) or `o=-pickup_time` (descending)
- Distance: `o=distance`
    - When using distance, must additionally set query parameters `longitude=<float>` and `latitude=<float>`
    - There will be an error if asking for distance and both longitude and latitude are not defined
    - The backend will calculate the distance from existing pickup latitude/longitudes from the input latitude/longitudes
    - There will be errors if using distance without `longitude` and `latitude`, as well as errors as if only one of `longitude` or `latitude` are defined, or if either value is not a float.

### Ride List Example
`http://127.0.0.1:8000/api/rides/?limit=10&offset=0&o=-pickup_time,distance&latitude=20.0&longitude=20.0&email=john&gmail.com&status=Pickup`

## Bonus SQL
```
WITH Pickup_Event AS (
    SELECT
        id_ride,
        created_at AS pickup_time.
    FROM
        ride_events
    WHERE
        description = 'Status changed to pickup'
    GROUP BY
        id_ride
),
Dropoff_Event AS (
    SELECT
        id_ride,
        created_at AS dropoff_time
    FROM
        ride_events
    WHERE
        description = 'Status changed to dropoff'
),
Ride_Durations AS (
    SELECT
        rides.id_ride,
        rides.id_rider,
        rides.id_driver,
        users.first_name || ' ' ||
            substr(users.last_name, 1, 1) AS driver,
        Pickup_Event.pickup_time,
        (
            strftime('%s', Dropoff_Event.dropoff_time) -
            strftime('%s', Pickup_Event.pickup_time)
        ) / 3600.0 AS duration_hours
    FROM
        rides
    LEFT JOIN Pickup_Event
        ON rides.id_ride = Pickup_Event.id_ride
    LEFT JOIN Dropoff_Event
        ON rides.id_ride = Dropoff_Event.id_ride
    LEFT JOIN users
        ON rides.id_driver = users.id_user
)
SELECT
    strftime('%Y-%m', pickup_time) AS Month,
    driver AS Driver,
    COUNT(*) AS "Count of Trips > 1 hr"
FROM
    Ride_Durations
WHERE
    duration_hours > 1
GROUP BY
    strftime('%Y-%m', pickup_time),
    driver
ORDER BY
    Month,
    Driver;
```