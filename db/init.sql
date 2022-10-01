CREATE TABLE orders (
    id int PRIMARY KEY UNIQUE,
    order_id text,
    usd_cost int,
    rub_cost int,
    delivery_date date
)