import tkinter as tk
from tkinter import filedialog, StringVar
import requests
from PIL import Image, ImageTk
from io import BytesIO
from pytube import YouTube
import pygame
import os

def on_url_change(event):
    url = url_entry.get()
    try:
        youtube = YouTube(url)
        video_thumbnail_url = youtube.thumbnail_url

        # Fetching thumbnail image from youtube
        response = requests.get(video_thumbnail_url)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        preview_label.config(image=photo)
        preview_label.image = photo
        status_label.config(text="Preview loaded.")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        preview_label.config(image=logo_image)


def update_quality_options(youtube):
    #handle video quality from stream
    streams = youtube.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")
    quality_options = ["lowest possible"] + [stream.resolution for stream in streams] + ["highest possible"]
    quality_var.set("highest possible")
    quality_menu["menu"].delete(0, "end")
    for option in quality_options:
        quality_menu["menu"].add_command(label=option, command=lambda value=option: quality_var.set(value))


def on_download():
    url = url_entry.get()
    path = filedialog.askdirectory()
    quality = quality_var.get()
    file_name = filename_entry.get()

    try:
        youtube = YouTube(url)
        video_stream = None
        if quality == "lowest possible":
            video_stream = youtube.streams.filter(progressive=True, file_extension="mp4").first()
        elif quality == "highest possible":
            video_stream = youtube.streams.filter(progressive=True, file_extension="mp4").last()
        else:
            video_stream = youtube.streams.filter(progressive=True, file_extension="mp4", resolution=quality).first()

        if video_stream:
            if not file_name:
                # file_name not specified, video title = file name
                file_name = youtube.title.replace(" ", "_") + ".mp4"
            elif not file_name.lower().endswith(".mp4"):
                # file name is provided but doesn't have ".mp4" extension
                file_name += ".mp4"

            video_stream.download(output_path=path, filename=file_name)
            status_label.config(text="Download completed.")
        else:
            status_label.config(text="No video available for download.")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


def play_preview(video_path):
    pygame.init()
    pygame.display.set_caption("Video Preview")
    screen = pygame.display.set_mode((480, 360))  # Set the screen size to 480x360
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie(video_path)

    # Get original dimensions
    video_width = movie.get_size()[0]
    video_height = movie.get_size()[1]

    # Altering dimensions within 480x360
    if video_width > 480 or video_height > 360:
        aspect_ratio = video_width / video_height
        if aspect_ratio >= 480 / 360:
            new_width = 480
            new_height = int(480 / aspect_ratio)
        else:
            new_width = int(360 * aspect_ratio)
            new_height = 360
        movie.set_display(screen, (240 - new_width // 2, 180 - new_height // 2, new_width, new_height))
    else:
        movie.set_display(screen, (240 - video_width // 2, 180 - video_height // 2, video_width, video_height))

    movie.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        clock.tick(30)

    movie.stop()
    pygame.quit()
    os.remove(video_path)


# Set window title
root = tk.Tk()
root.title("Utµbε   ∆¤ωNL¤aδεr")

# Load youtube logo
logo_image = Image.open("youtube_logo.png")
logo_image.thumbnail((300, 300))
logo_photo = ImageTk.PhotoImage(logo_image)

# Preview label
preview_label = tk.Label(root, image=logo_photo)
preview_label.image = logo_photo  # Store a reference to the logo_photo
preview_label.pack()

# url input
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Quality selection
quality_var = StringVar(root)
quality_options = ["lowest possible", "360p", "480p", "720p", "1080p", "1440p", "highest possible"]
quality_var.set("Choose Quality")
quality_label = tk.Label(root, text="Select Video Quality:")
quality_label.pack()
quality_menu = tk.OptionMenu(root, quality_var, *quality_options)
quality_menu.pack()

url_entry.bind("<KeyRelease>", on_url_change)

# filename input
filename_label = tk.Label(root, text="Filename:")
filename_label.pack()
filename_entry = tk.Entry(root)
filename_entry.pack()

# Download button
download_button = tk.Button(root, text="Download", command=on_download)
download_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# Credit label
credit_label = tk.Label(root, text="Created by G13", fg="gray")
credit_label.pack(side="bottom", padx=10, pady=10)


root.mainloop()
