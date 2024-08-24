import shutil, winaccent, sys, os

def colorize_controls():
    try:
        os.remove(f"{__package__}/theme/light.tcl")
        os.remove(f"{__package__}/theme/dark.tcl")
    except: pass

    try:
        if sys.platform == "win32":
            light_tcl = open(f"{__package__}/theme/light_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light)
            dark_tcl = open(f"{__package__}/theme/dark_original.tcl", "r", encoding = "utf8").read().replace("#005fb8", winaccent.accent_light).replace("#57c8ff", winaccent.accent_dark)

            open(f"{__package__}/theme/light.tcl", "w", encoding = "utf8").write(light_tcl)
            open(f"{__package__}/theme/dark.tcl", "w", encoding = "utf8").write(dark_tcl)
        else:
            shutil.copyfile(f"{__package__}/theme/light_original.tcl", f"{__package__}/theme/light.tcl")
            shutil.copyfile(f"{__package__}/theme/dark_original.tcl", f"{__package__}/theme/dark.tcl")
    except Exception as e:
        print(e)

        shutil.copyfile(f"{__package__}/theme/light_original.tcl", f"{__package__}/theme/light.tcl")
        shutil.copyfile(f"{__package__}/theme/dark_original.tcl", f"{__package__}/theme/dark.tcl")
