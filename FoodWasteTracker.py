import streamlit as st
import datetime

# Waste disposal recommendations
disposal_methods = {
    "Vegetables": "Compost or use for broth-making.",
    "Cooked Foods": "Donate if safe, otherwise compost.",
    "Meat & Seafood": "Freeze to extend shelf life or use in pet food.",
    "Dairy Products": "Use in baked goods or compost if spoiled."
}

# Function to check if food is spoiled
def is_spoiled(expiry_date):
    return datetime.datetime.now() > expiry_date

# Food categories
food_categories = {
    "Vegetables": ["Spinach", "Carrots", "Broccoli", "Bell Peppers", "Mushrooms"],
    "Cooked Foods": ["Rice", "Soup", "Pasta", "Grilled Chicken", "Stew"],
    "Meat & Seafood": ["Chicken", "Beef", "Pork", "Fish", "Shrimp"],
    "Dairy Products": ["Milk", "Cheese", "Yogurt", "Butter", "Cream"]
}

# Streamlit UI
st.title("🌱 Smart Kitchen Food Waste Tracker")

# User input for adding food items
category = st.selectbox("Food Category", list(food_categories.keys()))
name = st.selectbox("Food Item", food_categories[category])
quantity = st.number_input("Quantity (grams/kg)", min_value=1, step=1)
expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())

if st.button("Add Food Item"):
    expiry_date_obj = datetime.datetime.combine(expiry_date, datetime.datetime.min.time())
    st.session_state.setdefault("inventory", []).append(
        {"category": category, "name": name, "quantity": quantity, "expiry_date": expiry_date_obj}
    )
    st.success(f"{name} added to inventory under {category}!")

# Display complete inventory with expiry status
st.subheader("📋 Inventory List & Expiry Status")
if "inventory" in st.session_state and st.session_state["inventory"]:
    for item in st.session_state["inventory"]:
        expired = is_spoiled(item["expiry_date"])
        status = "⚠ Expired!" if expired else "✅ Still Good"
        st.write(f"{item['name']}** ({item['category']}) - {item['quantity']} units | Expiry: {item['expiry_date'].date()} | Status: {status}")
else:
    st.info("No food items added yet.")

# Track total waste per category
st.subheader("🗑 Total Waste Breakdown")
total_waste = {cat: 0 for cat in food_categories.keys()}
for item in st.session_state.get("inventory", []):
    if is_spoiled(item["expiry_date"]):
        total_waste[item["category"]] += item["quantity"]

for cat, qty in total_waste.items():
    if qty > 0:
        st.write(f"{cat}:** {qty} grams/kg")

# Provide disposal recommendations
st.subheader("♻ Waste Handling & Disposal Tips")
for cat, qty in total_waste.items():
    if qty > 0:
        st.info(f"{cat}:** {disposal_methods[cat]}")