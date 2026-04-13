import os
from PIL import Image

def compress_images(input_dir, output_dir, max_size=(1024, 1024), quality=85):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            filepath = os.path.join(input_dir, filename)
            try:
                with Image.open(filepath) as img:
                    # Convert to RGB if it's RGBA (PNG)
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            bg.paste(img, mask=img.split()[3])
                        else:
                            bg.paste(img)
                        img = bg
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    new_filename = os.path.splitext(filename)[0] + '.jpg'
                    new_filepath = os.path.join(output_dir, new_filename)
                    
                    img.save(new_filepath, 'JPEG', quality=quality)
                    print(f"Compressed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    input_directory = r"c:\Users\Administrator\Desktop\PinGPT\Tiktok ready"
    output_directory = r"c:\Users\Administrator\Desktop\PinGPT\Tiktok ready compressed"
    
    compress_images(input_directory, output_directory)
    print("Optimization complete!")
