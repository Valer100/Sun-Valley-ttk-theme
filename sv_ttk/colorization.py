from PIL import Image
import shutil, sys, traceback

def tint_image(image_path, output_path, hex_color):
    image = Image.open(image_path).convert("RGBA")

    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)

    solid_color_image = Image.new("RGBA", image.size, (r, g, b, 255))

    final_image = Image.composite(solid_color_image, Image.new("RGBA", image.size, (0, 0, 0, 0)), image)
    final_image.save(output_path)

def overlay_images(image1_path, image2_path, output_image_path, position=(0, 0)):
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")
    
    base_image = Image.new("RGBA", image2.size, (0, 0, 0, 0))
    
    base_image.paste(image2, (0, 0))
    base_image.paste(image1, position, image1)
    
    base_image.save(output_image_path, "PNG")

def use_default_colors():
    shutil.copyfile(f"{__package__}/theme/original/light.tcl", f"{__package__}/theme/light.tcl")
    shutil.copyfile(f"{__package__}/theme/original/dark.tcl", f"{__package__}/theme/dark.tcl")
    shutil.copyfile(f"{__package__}/theme/original/spritesheet_light.png", f"{__package__}/theme/spritesheet_light.png")
    shutil.copyfile(f"{__package__}/theme/original/spritesheet_dark.png", f"{__package__}/theme/spritesheet_dark.png")

def colorize_controls():
    try:
        if sys.platform == "win32":
            import winaccent

            light_tcl = open(f"{__package__}/theme/light_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light_mode)
            dark_tcl = open(f"{__package__}/theme/dark_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light_mode).replace("#57c8ff", winaccent.accent_dark_mode)

            open(f"{__package__}/theme/light.tcl", "w", encoding = "utf8").write(light_tcl)
            open(f"{__package__}/theme/dark.tcl", "w", encoding = "utf8").write(dark_tcl)

            tint_image(
                f"{__package__}/theme/original/mask.png",
                f"{__package__}/theme/mask_light.png",
                winaccent.accent_light_mode
            )
            tint_image(
                f"{__package__}/theme/original/mask.png",
                f"{__package__}/theme/mask_dark.png",
                winaccent.accent_dark_mode
            )

            overlay_images(
                f"{__package__}/theme/original/mask_light.png", 
                f"{__package__}/theme/original/spritesheet_light.png",
                f"{__package__}/theme/spritesheet_light.png"
            )

            overlay_images(
                f"{__package__}/theme/original/mask_dark.png", 
                f"{__package__}/theme/original/spritesheet_dark.png",
                f"{__package__}/theme/spritesheet_dark.png"
            )
        else:
            use_default_colors()
    except Exception as e:
        print(traceback.format_exc())
        use_default_colors()

import winaccent

tint_image(
        f"{__file__.replace('colorization.py', '')}theme/original/mask.png",
        f"{__file__.replace('colorization.py', '')}theme/mask_light.png",
        winaccent.accent_light_mode
)
            
tint_image(
        f"{__file__.replace('colorization.py', '')}theme/original/mask.png",
        f"{__file__.replace('colorization.py', '')}theme/mask_dark.png",
        winaccent.accent_dark_mode
)