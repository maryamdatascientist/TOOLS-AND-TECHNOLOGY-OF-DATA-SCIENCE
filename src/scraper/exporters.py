import csv
from collections import defaultdict


def export_products(products, filename="data/products.csv"):

    if not products:
        return

    keys = products[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)


def export_category_summary(products, duplicates_removed,
                            filename="data/category_summary.csv"):

    stats = defaultdict(list)

    for p in products:
        stats[p["subcategory"]].append(p)

    rows = []

    for subcat, items in stats.items():

        prices = [i["price"] for i in items if i["price"] is not None]

        avg_price = sum(prices) / len(prices) if prices else 0
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0

        missing_desc = sum(
            1 for i in items if not i["description"]
        )

        rows.append({
            "subcategory": subcat,
            "total_products": len(items),
            "average_price": round(avg_price, 2),
            "min_price": min_price,
            "max_price": max_price,
            "missing_descriptions": missing_desc,
            "duplicates_removed": duplicates_removed
        })

    with open(filename, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "subcategory",
                "total_products",
                "average_price",
                "min_price",
                "max_price",
                "missing_descriptions",
                "duplicates_removed"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)