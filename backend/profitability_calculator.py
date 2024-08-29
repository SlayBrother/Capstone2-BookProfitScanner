def analyze_profitability(product, buy_price):
    # Extract the sale price from the product details, converting it from a string (e.g., "$19.99") to a float.
    sale_price = float(product['price']['display'].replace('$', ''))

    # Calculate the Amazon referral fee, which is 15% of the sale price.
    referral_fee = 0.15 * sale_price
    
    # The closing fee is a fixed cost of $1.80, typically applied to media items like books.
    closing_fee = 1.80
    
    # Calculate the Fulfillment by Amazon (FBA) fee, which is 40% of the sale price.
    fba_fee = 0.40 * sale_price
    
    # Calculate the inventory charge, which is 0.25% of the sale price.
    inventory_charge = 0.0025 * sale_price
    
    # Calculate the shipping fee, which is 2.67% of the sale price.
    shipping_fee = 0.0267 * sale_price

    # Calculate the total profitability by subtracting all the fees and the buy price from the sale price.
    profitability = sale_price - (referral_fee + closing_fee + fba_fee + inventory_charge + shipping_fee + buy_price)

    # Return the profitability as a formatted string, rounding to two decimal places.
    return {
        'profitability': f"${profitability:.2f}"
    }

