
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"

response = requests.get(url, timeout=15)
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")
data = []

for book in books:
    title = book.h3.a["title"]
    price_text = book.find(
        "p", class_="price_color"
    ).text
    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag["class"][1] if rating_tag else "Unknown"
   
    price = float(
        price_text.replace("£", "").replace("Â", "")
    )

    data.append({
        "Title": title,
        "Price (£)": price,
        "Rating": rating
    })

df = pd.DataFrame(data)
df.to_csv("books.csv", index=False)

print("\n===== BOOK DATA ANALYSIS =====")
print("Total books:", len(df))
print("Average price: £", round(df["Price (£)"].mean(), 2))
print("Highest price: £", round(df["Price (£)"].max(), 2))
print("Lowest price: £", round(df["Price (£)"].min(), 2))

print("\nData saved successfully to books.csv")

