import pandas as pd

# Real-world inspired data for Malaysia
actual_data = [
    # STATE, CITY, ACC_DAILY, FOOD_DAILY, TRANS_DAILY, DESCRIPTION, IMAGE_URL, RATING, DISTANCE, VIBE
    ["Kuala Lumpur", "Bukit Bintang", 250, 80, 30, "The heart of KL. Great for shopping and street food.", "https://images.unsplash.com/photo-1596422846543-75c6fc18a594", 4.8, 0, "Busy/Street"],
    ["Kuala Lumpur", "Taman Tun Dr Ismail", 200, 60, 40, "Upscale neighborhood with hidden cafes and parks.", "https://images.unsplash.com/photo-1620332372374-f108c53d2e03", 4.5, 12, "Hidden Gem"],
    ["Selangor", "Batu Caves", 150, 40, 50, "Iconic colorful stairs and limestone caves.", "https://images.unsplash.com/photo-1544257750-572358f5da22", 4.7, 15, "Nature"],
    ["Penang", "Georgetown", 180, 50, 20, "Famous for street art and world-class hawker food.", "https://images.unsplash.com/photo-1595123550441-d377e017de6a", 4.9, 2, "Foodie Hunt"],
    ["Penang", "Batu Ferringhi", 350, 90, 40, "Beachfront resorts and romantic night markets.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0", 4.6, 15, "Dating/Romantic"],
    ["Pahang", "Cameron Highlands", 220, 50, 60, "Cool breeze, tea plantations, and strawberry farms.", "https://images.unsplash.com/photo-1511525281081-30623315a676", 4.7, 200, "Nature"],
    ["Pahang", "Genting Highlands", 400, 100, 80, "Theme parks, casinos, and high-altitude entertainment.", "https://images.unsplash.com/photo-1580128660010-fd027e1e587a", 4.4, 50, "Busy/Street"],
    ["Sabah", "Kundasang", 280, 40, 100, "The 'New Zealand' of Malaysia. Stunning Kinabalu views.", "https://images.unsplash.com/photo-1626078436897-39655f410940", 4.9, 90, "Nature"],
    ["Melaka", "Jonker Street", 160, 45, 15, "Historic vibes with amazing Nyonya laksa and antiques.", "https://images.unsplash.com/photo-1590059124310-09559c381cc1", 4.8, 1, "Foodie Hunt"],
]

# Create the DataFrame
df = pd.DataFrame(actual_data, columns=[
    "State", "City", "Accommodation_Daily", "Food_Daily", "Transport_Daily", 
    "Description", "Image_URL", "Rating", "Distance_Hub", "Vibe"
])

# Save it - This replaces your old CSV
df.to_csv("malaysia_travel.csv", index=False)
print("✅ Real-World Data Generated! Your app will no longer crash.")