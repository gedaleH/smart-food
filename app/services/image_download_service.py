
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_first_image(keyword, output_path):
    try:
        # URL Bing Images
        url = f"https://www.bing.com/images/search?q={keyword}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        # Les images sont dans des balises <img class="mimg">
        img = soup.find("img", {"class": "mimg"})
        if not img:
            print("Aucune image trouvée.")
            return False

        img_url = img.get("src")

        # Si URL relative
        img_url = urljoin(url, img_url)

        # Téléchargement
        img_data = requests.get(img_url, headers=headers).content
        with open(output_path, "wb") as f:
            f.write(img_data)

        print("Image téléchargée :", output_path)
        return True

    except Exception as e:
        print(e)

def generate_image_for_req(name, id):
    img_name = f"{str(id)}.png"
    path = f"app/static/images/requirements/{img_name}"
    download_first_image(f"{name} nourriture image", path)

def generate_image_for_ci(name, id):
    img_name = f"{str(id)}.png"
    path = f"app/static/images/cis/{img_name}"
    download_first_image(f"{name} nourriture image", path)
