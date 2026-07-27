import os
from PIL import Image, ImageDraw

os.makedirs('static/images', exist_ok=True)

# Create 800x450 dark slate background
img = Image.new('RGB', (800, 450), color=(40, 44, 52))
draw = ImageDraw.Draw(img)

# Draw subtle accent border box
draw.rectangle([30, 30, 770, 420], outline=(75, 85, 99), width=3)
draw.rectangle([50, 50, 750, 400], outline=(13, 110, 253), width=2)

img.save('static/images/default-post.jpg', 'JPEG', quality=90)
print("Created static/images/default-post.jpg successfully")
