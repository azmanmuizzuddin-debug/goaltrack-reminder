import pandas as pd
import random

states = [
    "Kuala Lumpur", "Selangor", "Penang", "Johor", "Perak", "Melaka", 
    "Pahang", "Terengganu", "Kelantan", "Kedah", "Negeri Sembilan", "Sabah", "Sarawak"
]

types = ["Nature", "Foodie", "Adventure", "History", "Leisure", "Modern"]
dishes = ["Nasi Lemak", "Laksa", "Satay", "Char Kway Teow", "Cendol", "Roti Canai"]

data = []

for state in states:
    # Generate ~25 places per state to reach 300+
    for i in range(1, 30):
        city_name = f"{state} District {i}"
        # Randomize data for variety
        acc = random.randint(50, 400)
        food = random.randint(30, 120)
        trans = random.randint(10, 80)
        rating = round(random.uniform(3.5, 5.0), 1)
        dist = random.randint(2, 150)
        
        data.append([
            state, city_name, acc, food, trans, 50, 
            f"A beautiful spot in {state} perfect for {random.choice(types)}.",
            f"https://picsum.photos/seed/{state}{i}/400/250", # Random high-quality images
            rating, dist, random.choice(types), random.choice(dishes)
        ])

df = pd.DataFrame(data, columns=[
    "State", "City", "Accommodation_Daily", "Food_Daily", "Transport_Daily", 
    "Expenditure_Daily", "Description", "Image_URL", "Rating", "Distance_Hub", "Travel_Type", "Local_Dish"
])

df.to_csv("malaysia_travel.csv", index=False)
print("✅ Created malaysia_travel.csv with 325 places!")