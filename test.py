from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# Function to clean up the database before tests
def cleanup_products():
    response = client.get("/products/")
    for product in response.json():
        client.delete(f"/products/{product['id']}")

# Positive Test Case 1: Create a product successfully
def test_create_product_success():
    cleanup_products()  # Clean up before running the test

    response = client.post("/products/", json={
        "name": "Valid Product",
        "price": 29.99,
        "quantity": 150,
        "description": "A valid product for testing.",
        "category": "Valid Category"
    })
    
    if response.status_code == 200:
        product = response.json()
        print(f"Success: Product created successfully - ID: {product['id']}, Name: {product['name']}, Price: {product['price']}")
    else:
        print(f"Failure: Product creation failed with status {response.status_code} - Detail: {response.json()}")

# Negative Test Case 1: Create a product with a duplicate name
def test_create_product_duplicate_name():
    cleanup_products()  # Clean up before running the test

    client.post("/products/", json={
        "name": "Duplicate Product",
        "price": 20.99,
        "quantity": 200
    })
    
    response = client.post("/products/", json={
        "name": "Duplicate Product",
        "price": 25.99,
        "quantity": 150
    })
    
    if response.status_code == 400:
        assert response.json()["detail"] == "Product creation failed due to duplicate name."
        print(f"Success: Duplicate product creation handled correctly - Status: {response.status_code}, Detail: {response.json()}")
    else:
        print(f"Failure: Duplicate product creation failed with status {response.status_code} - Detail: {response.json()}")

# Positive Test Case 2: Get a product successfully
def test_get_product_success():
    cleanup_products()  # Clean up before running the test

    create_response = client.post("/products/", json={
        "name": "Product for Get",
        "price": 15.99,
        "quantity": 50
    })

    if create_response.status_code == 200:
        product_id = create_response.json()["id"]
        response = client.get(f"/products/{product_id}")
        
        if response.status_code == 200:
            product = response.json()
            print(f"Success: Product retrieved successfully - ID: {product['id']}, Name: {product['name']}")
        else:
            print(f"Failure: Retrieval of product {product_id} failed with status {response.status_code} - Detail: {response.json()}")
    else:
        print(f"Failure: Product creation failed with status {create_response.status_code} - Detail: {create_response.json()}")

# Negative Test Case 2: Get a non-existent product
def test_get_non_existent_product():
    cleanup_products()  # Clean up before running the test

    response = client.get("/products/99999")  # Assuming this ID does not exist
    if response.status_code == 404:
        print(f"Success: Non-existent product retrieval handled correctly - Status: {response.status_code}, Detail: {response.json()}")
    else:
        print(f"Failure: Attempt to get non-existent product failed with status {response.status_code} - Detail: {response.json()}")

# Positive Test Case 3: Update a product successfully
def test_update_product_success():
    cleanup_products()  # Clean up before running the test

    create_response = client.post("/products/", json={
        "name": "Product to Update",
        "price": 15.99,
        "quantity": 60
    })
    
    if create_response.status_code == 200:
        product_id = create_response.json()["id"]
        response = client.put(f"/products/{product_id}", json={
            "price": 20.99,
            "quantity": 80
        })
        
        if response.status_code == 200:
            updated_product = response.json()
            print(f"Success: Product updated successfully - ID: {updated_product['id']}, New Price: {updated_product['price']}, New Quantity: {updated_product['quantity']}")
        else:
            print(f"Failure: Product update failed with status {response.status_code} - Detail: {response.json()}")
    else:
        print(f"Failure: Product creation failed with status {create_response.status_code} - Detail: {create_response.json()}")

# Negative Test Case 3: Update a non-existent product
def test_update_non_existent_product():
    cleanup_products()  # Clean up before running the test

    response = client.put("/products/99999", json={"price": 30.00})  # Assuming this ID does not exist
    if response.status_code == 404:
        print(f"Success: Attempt to update non-existent product handled correctly - Status: {response.status_code}, Detail: {response.json()}")
    else:
        print(f"Failure: Attempt to update non-existent product failed with status {response.status_code} - Detail: {response.json()}")

# Negative Test Case 4: Delete a non-existent product
def test_delete_non_existent_product():
    cleanup_products()  # Clean up before running the test

    response = client.delete("/products/99999")  # Assuming this ID does not exist
    if response.status_code == 404:
        print(f"Success: Attempt to delete non-existent product handled correctly - Status: {response.status_code}, Detail: {response.json()}")
    else:
        print(f"Failure: Attempt to delete non-existent product failed with status {response.status_code} - Detail: {response.json()}")

# Positive Test Case 5: List products with a price filter
def test_list_products_with_price_filter():
    cleanup_products()  # Clean up before running the test

    client.post("/products/", json={
        "name": "Product A",
        "price": 30.99,
        "quantity": 10
    })
    client.post("/products/", json={
        "name": "Product B",
        "price": 40.99,
        "quantity": 20
    })

    response = client.get("/products/?price_gte=35")
    if response.status_code == 200:
        products = response.json()
        if len(products) == 1 and products[0]["name"] == "Product B":
            print(f"Success: Product list retrieved with price filter successfully - Filtered product name: {products[0]['name']}")
        else:
            print(f"Failure: Price filter did not return expected results - Status: {response.status_code}, Detail: {products}")
    else:
        print(f"Failure: Attempt to list products with price filter failed with status {response.status_code} - Detail: {response.json()}")

# Run these test cases
if __name__ == "__main__":
    import pytest
    pytest.main()
