@app.get("/api/last-price-file")
async def get_last_price_file():
    import json
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"price": data.get("price")}
    except Exception as e:
        print(f"Error reading price file: {e}")
        return {"price": None}
