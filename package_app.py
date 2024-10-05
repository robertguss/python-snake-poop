import os
import sys

import PyInstaller.__main__


def package_pygame_app(script_name, icon_file=None, additional_data=None):
    # Ensure the script exists
    if not os.path.isfile(script_name):
        raise FileNotFoundError(f"Script '{script_name}' not found.")

    # Base PyInstaller command
    command = [
        script_name,
        "--onefile",
        "--windowed",
        f"--name={os.path.splitext(os.path.basename(script_name))[0]}",
        "--add-data=assets:assets",  # Adjust this path for your assets
    ]

    # Add icon if provided
    if icon_file:
        if not os.path.isfile(icon_file):
            raise FileNotFoundError(f"Icon file '{icon_file}' not found.")
        command.append(f"--icon={icon_file}")

    # Add Pygame hook
    command.extend(
        [
            "--add-data=pygame:pygame",
            "--hidden-import=pygame",
            "--hidden-import=pygame.mixer",
        ]
    )

    # Add additional data files
    if additional_data:
        for src, dest in additional_data.items():
            command.append(f"--add-data={src}:{dest}")

    # Determine the correct path separator
    path_separator = ";" if sys.platform.startswith("win") else ":"

    # Add all local modules
    local_modules = [
        f for f in os.listdir(".") if f.endswith(".py") and f != script_name
    ]
    for module in local_modules:
        command.append(f"--add-data={module}{path_separator}.")

    # Add audio and image files
    for file in os.listdir("."):
        if file.endswith((".mp3", ".png")):
            command.append(f"--add-data={file}{path_separator}.")

    # Run PyInstaller
    PyInstaller.__main__.run(command)


if __name__ == "__main__":
    package_pygame_app(
        "snake_poo.py",
        icon_file="icon.png",  # Changed to .png
        additional_data={
            "fonts": "fonts",
            "sounds": "sounds",
            "images": "images",
        },
    )
