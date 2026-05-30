@app.get("/api/last-price")
async def get_last_price():
    import json
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = json.load(f)
            return {"price": data.get("price")}
    except:
        return {"price": None}
