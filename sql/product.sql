SELECT prod_name, prod_measure, prod_price 
FROM product 
JOIN categories ON categories.cat_id = product.prod_category
WHERE categories.cat_name = $prod_category
