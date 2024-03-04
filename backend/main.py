import json
import os
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import face_recognition

# Define directory for unknown face images
dataset_path = "dataset/unknown_faces"

# Known faces (replace with your actual images and names)
known_images = [
    face_recognition.load_image_file("dataset/Sanyam.jpg"),
    face_recognition.load_image_file("dataset/alia.png"),
    face_recognition.load_image_file("dataset/ranbir.png"),
    face_recognition.load_image_file("dataset/kim.jpg"),
]
known_names = ["Sanyam", "Alia", "Ranbir", "Kim"]  # Replace with actual names
known_encodings = [face_recognition.face_encodings(image)[0] for image in known_images]

# Create the main GUI window
root = tk.Tk()
root.title("Face Recognition GUI")

# Define video width and height
video_width = 600
video_height = 420

# Create Labels to display the webcam feed and the results
video_label = tk.Label(root)
result_label = tk.Label(root)

window_width = root.winfo_width()
horizontal_offset = (window_width - video_width) // 2

video_label.place(x=horizontal_offset, y=0, width=video_width, height=video_height)
result_label.place(x=window_width//2, y=video_height+20, width=200, height=30)

webcam_displaying = False
detected_names = ""
detected_names_list = []

# Define a function to display the webcam feed
def display_webcam():
    global video_capture, webcam_displaying, result_label, detected_names, detected_names_list  # Access global variable

    # Capture video from webcam
    video_capture = cv2.VideoCapture(0)
    webcam_displaying = True

    unique_face_id = 0  # Track unique ID for unknown faces

    while webcam_displaying:
        ret, frame = video_capture.read()
        if ret:
            rgb_frame = frame[:, :, ::-1]

            # Detect faces in the RGB frame
            face_locations = face_recognition.face_locations(rgb_frame)

            # Common processing for face detected or not
            # Draw rectangles and handle recognition (if desired)
            for (top, right, bottom, left) in face_locations:
                try:
                    # Recognition logic with error handling
                    face_image = frame[top:bottom, left:right]
                    face_encoding = face_recognition.face_encodings(face_image)[0]
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_names[first_match_index]
                        print(name)  # Print recognized name (optional)
                        if name not in detected_names_list:
                            detected_names += name + " "
                            detected_names_list.append(name)

                    else:
                        if unique_face_id <= len(face_locations):
                            # Save unknown face image
                            unique_face_id += 1  # Increment unique ID
                            unknown_image_name = f"unknown_{unique_face_id}.jpg"

                            # Create the directory if it doesn't exist
                            if not os.path.exists(dataset_path):
                                os.makedirs(dataset_path)

                            # Attempt to save the image
                            cv2.imwrite(os.path.join(dataset_path, unknown_image_name), frame)
                            print(f"Saved unknown face: {unknown_image_name}")
                            if name not in detected_names_list:
                                detected_names += "Unknown "
                                detected_names_list.append("Unknown")

                    # Draw rectangle and name (optional)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                    cv2.imwrite("display.png", frame)

                except:
                    print("No face encoding found!")

            recognized_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            video_frame = ImageTk.PhotoImage(Image.fromarray(recognized_frame))

            window_width = root.winfo_width()
            horizontal_offset = (window_width - video_width) // 2
            video_label.place(x=horizontal_offset, y=20, width=video_width, height=video_height)
            result_label.place(x=window_width//2, y=video_height+20, width=200, height=30)

            if len(detected_names_list) > 0:
                if "Unknown" in detected_names:
                    if detected_names.count("Unknown") == len(detected_names.split(" ")):
                        result_label.config(text=f"Unknown Face(s) Detected")
                    else:
                        result_label.config(text=f"Recognized: {detected_names.replace('Unknown ', '')} and Unknown Face(s) Detected")
                else:
                    result_label.config(text=f"Recognized: {name}")
            else:
                result_label.config(text=f"No Face Detected")

            video_label.config(image=video_frame)
            video_label.image = video_frame 

            if len(detected_names_list) > 0:
                with open("detected.json", 'w') as file:
                    json.dump({"names": detected_names_list}, file)

            root.update()

    video_capture.release()

# Set window size
width = 1000
height = 600
root.geometry(f"{width}x{height}")

# Load and resize alarm icon image
alarm_image = Image.open("bell.png") 
resized_image = alarm_image.resize((75, 75))

# Convert image to PhotoImage for Tkinter
alarm_icon = ImageTk.PhotoImage(resized_image)

# Create a button with the image, larger size, and rounded corners
capture_button = tk.Button(
    root,
    image=alarm_icon,
    compound=tk.CENTER, 
    command=display_webcam,
    width=100, 
    height=100, 
    borderwidth=0, 
    highlightthickness=0, 
    activebackground="black",
    background="black",
    foreground="black",
    relief=tk.FLAT,
)

# Calculate button position coordinates
button_x = (width - capture_button.winfo_reqwidth()) // 2
button_y = height - capture_button.winfo_reqheight() - 20

# Place the button at the bottom center
capture_button.place(x=button_x, y=button_y)

# Run the main event loop
root.mainloop()