import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, Image

# --- Configuration ---
# Your Google Cloud Project ID
PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
# The Google Cloud region to use
LOCATION = "us-central1"
# The output directory for images
OUTPUT_DIR = "www/images"

# --- Image Prompts ---
IMAGE_PROMPTS = {
    "logo.png": "A logo for a MUD (Multi-User Dungeon) game called 'Barsoom MUD'. The style should be a blend of retro 1990s video game logos and a futuristic, slightly art deco feel. The main text 'BARSOOM' should be prominent, with 'MUD' smaller underneath or integrated. The font should be metallic, with a weathered, coppery or reddish texture, reminiscent of the red planet Mars. It could be framed by Martian-inspired elements, like the tusks of a Green Martian, or the sleek lines of a Martian airship. The overall mood should be epic, adventurous, and hint at a classic sci-fi fantasy world. The logo should be on a transparent background.",
    "background.jpg": "A wide, panoramic background image for a website about a fantasy MUD set on Barsoom (Mars). The scene should depict a vast, ochre-colored desert landscape under a pale, thin Martian sky with two moons visible. In the distance, the gleaming, jeweled towers of a fantastical city (Helium) rise up, connected by graceful bridges. The style should be epic and painterly, with a sense of ancient mystery and adventure. The lighting should be dramatic, perhaps a low sun casting long shadows. The image should have areas of relatively low detail where text can be overlaid without being too busy. The aspect ratio should be wide, 16:9.",
    "creature_plant_man.png": "A full-body digital painting of a terrifying Plant Man from Barsoom. The creature is 10 feet tall with a trunk-like, limbless body covered in mossy, bark-like skin. It hops on a single, large foot. From its torso writhe multiple, powerful tentacles. Its head is a mass of leafy fronds with a single, large, malevolent white eye in the center. Its mouth is filled with needle-like fangs dripping with green poison. The setting is the lush but deadly Valley Dor at night, with strange, glowing flora in the background. The style is realistic horror, with dynamic lighting.",
    "creature_white_ape.png": "A digital painting of a ferocious Great White Ape of Barsoom in a dynamic action pose. This massive, 15-foot-tall beast has four powerful arms and is covered in shaggy white fur. It has a snarling, ape-like face with intelligent, rage-filled red eyes and large fangs. It's lunging forward in a ruined, ancient Martian city, with crumbling stone architecture in the background. The style is realistic and highly detailed, emphasizing its immense strength and savagery.",
    "creature_banth.png": "A digital painting of a majestic and deadly Banth, the ten-legged lion of Barsoom. It's the size of a large horse, with a powerful, tawny-furred feline body and ten muscular legs. It's depicted stalking gracefully across the ochre moss of a dead Martian sea bottom. Its head has fierce, intelligent eyes and large fangs. The background is a vast, empty Martian landscape under a pale sky with two moons. The style is realistic and captures both the beauty and predatory nature of the creature.",
    "zone_helium.png": "A breathtaking digital painting of the twin cities of Helium on Barsoom. The image shows two magnificent cities with impossibly tall, slender, jeweled towers, connected by massive, elegant bridges spanning a 75-mile gap. The architecture is a beautiful, ornate, and slightly alien art nouveau style. Martian airships fly silently between the towers. The scene is bathed in the warm light of a Martian sunset, under a pale sky with two moons. The style is epic, fantastical, and highly detailed.",
    "zone_valley_dor.png": "A digital painting of the beautiful but treacherous Valley Dor on Barsoom. The valley is filled with lush, vibrant, and bizarre alien flowers and plants in a riot of color. Golden cliffs rise hundreds of feet on either side. A serene, sparkling river (the River Iss) flows through the middle. The beauty is deceptive, with a subtle undertone of wrongness and danger. The style is fantastical and painterly, capturing a paradise that is secretly a trap.",
    "zone_sea_of_omean.png": "A digital painting of the subterranean Sea of Omean on Barsoom. The view is from a dark, rocky shore looking out over a vast, black, underground ocean. The only light comes from glowing phosphorescent rocks on the cavern ceiling and the dim, eerie radium lamps of a sleek, black First Born submarine gliding silently through the water in the distance. The mood is dark, oppressive, and mysterious, with a sense of immense, hidden scale. The style is dark fantasy with a touch of sci-fi horror.",
    "tech_airship.png": "A digital painting of a Red Martian airship in flight over the dead sea bottoms of Barsoom. The vessel is sleek and boat-like, with a hull of polished red metal, decorated with the insignia of Helium. It has an open-air deck where a few Red Martian warriors in ornate harnesses can be seen. There are no visible propellers or engines, as it is propelled by silent, gravity-defying ray technology. The style is a mix of Jules Verne-esque adventure and elegant, advanced technology.",
    "tech_radium_pistol.png": "A detailed digital illustration of a Martian Radium Pistol, resting on a leather harness. The pistol is an elegant, almost artistic weapon, with a long barrel and an ornate, curved grip. The metal has a coppery sheen. A faint, soft glow emanates from the radium power cell within the weapon. The style is realistic and focuses on the craftsmanship of the weapon, blending advanced technology with an almost antique aesthetic.",
    "tech_brain_transplant.png": "A digital painting depicting the 'Master Mind of Mars', Ras Thavas, performing a brain transplantation. The scene is a sterile, advanced laboratory lit by floating radium lamps. In the center, a brain is being carefully moved by delicate, precise machinery from one body to another. In the background, shelves are lined with jars containing preserved heads and organs, their eyes open and aware. The mood is a mix of scientific wonder and clinical horror. The style is realistic with a dark, sci-fi aesthetic.",
}

def generate_images():
    """
    Generates images using Vertex AI based on the predefined prompts.
    """
    if PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("ERROR: Please update the PROJECT_ID in the script before running.")
        return

    print(f"Initializing Vertex AI for project '{PROJECT_ID}' in '{LOCATION}'...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    print("Loading image generation model...")
    # See: https://cloud.google.com/vertex-ai/docs/generative-ai/image/image-generation-diffusion
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    if not os.path.exists(OUTPUT_DIR):
        print(f"Creating output directory: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR)

    for filename, prompt in IMAGE_PROMPTS.items():
        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(output_path):
            print(f"Skipping '{filename}', file already exists.")
            continue

        print(f"\nGenerating '{filename}'...")
        print(f"  Prompt: {prompt[:80]}...")

        try:
            # The 'number_of_images' parameter determines how many images to generate.
            # The 'seed' parameter helps ensure reproducibility.
            # The 'aspect_ratio' can be '1:1', '16:9', '9:16', '4:3', '3:4'.
            # The 'output_file_format' can be 'png' or 'jpeg'.

            aspect_ratio = "16:9" if filename == "background.jpg" else "1:1"
            output_format = "png" if ".png" in filename else "jpeg"

            images = model.generate_images(
                prompt=prompt,
                number_of_images=1,
                seed=42,
                aspect_ratio=aspect_ratio,
                output_file_format=output_format,
            )

            if images:
                images[0].save(location=output_path, include_generation_parameters=True)
                print(f"  Successfully saved image to '{output_path}'")
            else:
                print(f"  ERROR: Image generation failed for '{filename}'. No image was returned.")

        except Exception as e:
            print(f"  An error occurred while generating '{filename}': {e}")

    print("\nImage generation process complete.")


if __name__ == "__main__":
    generate_images()