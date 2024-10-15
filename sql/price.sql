SELECT prod_name, prod_measure, prod_price
FROM product
WHERE prod_price >= $min_price AND prod_price <= $max_price
