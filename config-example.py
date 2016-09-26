import os

# Giphy API key
giphy = dict(
    key = os.environ.get('GIPHY_KEY', 'dc6zaTOxFJmzC')
)

# FB Page Access Token
fb = dict(
    access_token = os.environ.get('FB_TOKEN', '')
)
