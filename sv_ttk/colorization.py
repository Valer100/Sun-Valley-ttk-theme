from PIL import Image
import shutil, sys, numpy as np, traceback

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2))**2))

def tint_image(input_image_path, output_image_path, tint_color, white_threshold = 100, black_threshold = 100, whiteish_intensity = 1, blackish_intensity = 1):
    image = Image.open(input_image_path).convert("RGBA")
    data = np.array(image)
    
    r, g, b, a = data[..., 0], data[..., 1], data[..., 2], data[..., 3]

    white_mask = (r > white_threshold) & (g > white_threshold) & (b > white_threshold)
    black_mask = (r < black_threshold) & (g < black_threshold) & (b < black_threshold)
    
    whiteish_mask = ((r > white_threshold) | (g > white_threshold) | (b > white_threshold)) & ~white_mask
    blackish_mask = ((r < black_threshold) | (g < black_threshold) | (b < black_threshold)) & ~black_mask
    
    monochrome_mask = (r == g) & (g == b)

    tint_r, tint_g, tint_b = hex_to_rgb(tint_color)

    tinted_data = data.copy()
    
    # Apply tint color
    tinted_data[..., 0] = np.where(~(white_mask | black_mask | monochrome_mask), tint_r, tinted_data[..., 0])
    tinted_data[..., 1] = np.where(~(white_mask | black_mask | monochrome_mask), tint_g, tinted_data[..., 1])
    tinted_data[..., 2] = np.where(~(white_mask | black_mask | monochrome_mask), tint_b, tinted_data[..., 2])
    
    # Apply intensity to white-ish and black-ish pixels
    tinted_data[..., 0] = np.where(whiteish_mask, tinted_data[..., 0] * whiteish_intensity, tinted_data[..., 0])
    tinted_data[..., 1] = np.where(whiteish_mask, tinted_data[..., 1] * whiteish_intensity, tinted_data[..., 1])
    tinted_data[..., 2] = np.where(whiteish_mask, tinted_data[..., 2] * whiteish_intensity, tinted_data[..., 2])
    
    tinted_data[..., 0] = np.where(blackish_mask, tinted_data[..., 0] * blackish_intensity, tinted_data[..., 0])
    tinted_data[..., 1] = np.where(blackish_mask, tinted_data[..., 1] * blackish_intensity, tinted_data[..., 1])
    tinted_data[..., 2] = np.where(blackish_mask, tinted_data[..., 2] * blackish_intensity, tinted_data[..., 2])
    
    tinted_image = Image.fromarray(tinted_data)
    tinted_image.save(output_image_path, "PNG")

def overlay_images(image1_path, image2_path, output_image_path, position=(0, 0)):
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")
    
    base_image = Image.new("RGBA", image2.size, (0, 0, 0, 0))
    
    base_image.paste(image2, (0, 0))
    base_image.paste(image1, position, image1)
    
    base_image.save(output_image_path, "PNG")

def colorize_controls():
    try:
        if sys.platform == "win32":
            import winaccent

            light_tcl = open(f"{__package__}/theme/light_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light_mode)
            dark_tcl = open(f"{__package__}/theme/dark_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light_mode).replace("#57c8ff", winaccent.accent_dark_mode)

            open(f"{__package__}/theme/light.tcl", "w", encoding = "utf8").write(light_tcl)
            open(f"{__package__}/theme/dark.tcl", "w", encoding = "utf8").write(dark_tcl)

            tint_image(
                f"{__package__}/theme/spritesheet_light_overlay_original.png",
                f"{__package__}/theme/spritesheet_light_overlay.png",
                winaccent.accent_light_mode
            )
            tint_image(
                f"{__package__}/theme/spritesheet_dark_overlay_original.png",
                f"{__package__}/theme/spritesheet_dark_overlay.png",
                winaccent.accent_dark_mode
            )

            overlay_images(
                f"{__package__}/theme/spritesheet_light_overlay.png", 
                f"{__package__}/theme/spritesheet_light_original.png",
                f"{__package__}/theme/spritesheet_light.png"
            )

            overlay_images(
                f"{__package__}/theme/spritesheet_dark_overlay.png", 
                f"{__package__}/theme/spritesheet_dark_original.png",
                f"{__package__}/theme/spritesheet_dark.png"
            )
        else:
            shutil.copyfile(f"{__package__}/theme/light_original.tcl", f"{__package__}/theme/light.tcl")
            shutil.copyfile(f"{__package__}/theme/dark_original.tcl", f"{__package__}/theme/dark.tcl")
            shutil.copyfile(f"{__package__}/theme/spritesheet_light_original.png", f"{__package__}/theme/spritesheet_light.png")
            shutil.copyfile(f"{__package__}/theme/spritesheet_dark_original.png", f"{__package__}/theme/spritesheet_dark.png")
    except Exception as e:
        print(traceback.format_exc())

        shutil.copyfile(f"{__package__}/theme/light_original.tcl", f"{__package__}/theme/light.tcl")
        shutil.copyfile(f"{__package__}/theme/dark_original.tcl", f"{__package__}/theme/dark.tcl")
        shutil.copyfile(f"{__package__}/theme/spritesheet_light_original.png", f"{__package__}/theme/spritesheet_light.png")
        shutil.copyfile(f"{__package__}/theme/spritesheet_dark_original.png", f"{__package__}/theme/spritesheet_dark.png")
