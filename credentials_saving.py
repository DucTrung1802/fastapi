import os

# To save environment variables permanently

# Linux/macOS
# Save in ~/.bashrc
# export API_KEY="your_api_key"

# Windows
# Open Command Line
# setx API_KEY "your_api_key"

# IMPORTANT: Restart IDE after set variables

api_key = os.getenv("API_KEY")  # Fetch the API key from environment variables
print(api_key)
if api_key:
    print(api_key)
    print("API Key found!")
else:
    print("API Key not found.")
