import cv2
import matplotlib.pyplot as plt
import os
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Setup
image_folder = 'images/'  # Your folder name
image_names = [f'img{i}.jpg' for i in range(1, 11)]  # img1.jpg to img10.jpg

# Dictionary to store image name and item count
image_counts = {}

# Step 2: Process each image
for image_name in image_names:
    image_path = os.path.join(image_folder, image_name)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error loading {image_name}. Skipping...")
        continue

    # Convert BGR to RGB for displaying original
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    canny = cv2.Canny(blur, 30, 150, 3)
    dilated = cv2.dilate(canny, (1, 1), iterations=2)
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Save count to dictionary
    object_count = len(cnt)
    image_counts[image_name] = object_count

# Step 3: Sorting Algorithms
def sort_and_display_results(self):

    # Counting Sort for dictionary
    def counting_sort_dict(d):
        if not d:
            return {}
        max_val = max(d.values())
        count = [[] for _ in range(max_val + 1)]
        for key in d:
            count[d[key]].append(key)
        sorted_dict = {}
        for i in range(len(count)):
            for key in count[i]:
                sorted_dict[key] = i
        return sorted_dict

    # Merge Sort for dictionary
    def merge_sort_dict(d):
        items = list(d.items())
        if len(items) <= 1:
            return dict(items)
        mid = len(items) // 2
        left = merge_sort_dict(dict(items[:mid]))
        right = merge_sort_dict(dict(items[mid:]))
        return merge_dicts(left, right)

    def merge_dicts(left, right):
        sorted_items = []
        left_items = list(left.items())
        right_items = list(right.items())
        i = j = 0
        while i < len(left_items) and j < len(right_items):
            if left_items[i][1] <= right_items[j][1]:
                sorted_items.append(left_items[i])
                i += 1
            else:
                sorted_items.append(right_items[j])
                j += 1
        sorted_items.extend(left_items[i:])
        sorted_items.extend(right_items[j:])
        return dict(sorted_items)

    # Selection Sort for dictionary
    def selection_sort_dict(d):
        items = list(d.items())
        n = len(items)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if items[j][1] < items[min_idx][1]:
                    min_idx = j
            items[i], items[min_idx] = items[min_idx], items[i]
        return dict(items)

    # Timing and Sorting
    start = time.perf_counter()  # Use perf_counter for better accuracy rather than time.time() as it gives 0.00000000
    sorted_counting = counting_sort_dict(image_counts.copy())
    end = time.perf_counter()
    time_counting = end - start

    start = time.perf_counter()
    sorted_merge = merge_sort_dict(image_counts.copy())
    end = time.perf_counter()
    time_merge = end - start

    start = time.perf_counter()
    sorted_selection = selection_sort_dict(image_counts.copy())
    end = time.perf_counter()
    time_selection = end - start

    # Results Display
    results = f"--- Sorted Dictionaries ---\n\n" \
              f"Counting Sort Result:\n{sorted_counting}\n\n" \
              f"Merge Sort Result:\n{sorted_merge}\n\n" \
              f"Selection Sort Result:\n{sorted_selection}\n\n" \
              f"--- Timing ---\n" \
              f"Counting Sort Time: {time_counting:.10f} seconds\n" \
              f"Merge Sort Time: {time_merge:.10f} seconds\n" \
              f"Selection Sort Time: {time_selection:.10f} seconds\n\n" \
              f"--- Conclusion ---\n" \
              f"The fastest sorting algorithm for this problem is **{min({'Counting Sort': time_counting, 'Merge Sort': time_merge, 'Selection Sort': time_selection}, key={'Counting Sort': time_counting, 'Merge Sort': time_merge, 'Selection Sort': time_selection}.get)}**."

    # Create a new top-level window to show results
    result_window = tk.Toplevel(self)
    result_window.title("Sorting Results")
    result_window.geometry("1500x800")  # Set the window size

    # Create a text widget to display the results
    result_text = tk.Text(result_window, height=100, width=200, font=('Helvetica', 14))
    result_text.insert(tk.END, results)
    result_text.pack(side=tk.TOP, padx=10, pady=10)

    # Button to hide the output and return to the image display
    hide_button = ttk.Button(result_window, text="Hide Output", command=result_window.destroy)
    hide_button.pack(side=tk.BOTTOM, pady=20)

# Add this functionality to the ImageNavigator class
class ImageNavigator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processing GUI")
        self.geometry("1920x1080")  # Set the window size to 1920x1080
        
        # Index to track current image
        self.index = 0
        
        # Frame for buttons (side by side, at the bottom)
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        # Create navigation buttons (positioned side by side)
        # Button to navigate to the previous image
        self.prev_button = ttk.Button(self.button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        
        # Button to open sorting window
        self.sort_button = ttk.Button(self.button_frame, text="Sort Images", command=self.sort_and_display_results)
        self.sort_button.pack(side=tk.LEFT, padx=10)
        
        # Button to navigate to the next image
        self.next_button = ttk.Button(self.button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Label for displaying current image information
        self.label = ttk.Label(self, text="")
        self.label.pack(side=tk.TOP, pady=20)
        
        # Plot images (matplotlib canvas)
        self.canvas = None
        
        # Start displaying first image
        self.display_image(self.index)

    # Add the sort_and_display_results function to this class
    def sort_and_display_results(self):
        # Call the function to handle sorting and display results in a new window
        sort_and_display_results(self)

    def display_image(self, index):
        image_name = image_names[index]
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Error loading {image_name}. Skipping...")
            return

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)
        canny = cv2.Canny(blur, 30, 150, 3)
        dilated = cv2.dilate(canny, (1, 1), iterations=2)
        (cnt, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Clear previous canvas
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Create a new matplotlib canvas for displaying images
        fig, axs = plt.subplots(2, 3, figsize=(18, 10))  # 2 rows, 3 columns

        # Hide all axes initially
        for ax_row in axs:
            for ax in ax_row:
                ax.axis('off')

        # Show Original Image (1st subplot)
        axs[0, 0].imshow(rgb)
        axs[0, 0].set_title("Original Image")
        axs[0, 0].axis('on')

        # Show Grayscale Image (2nd subplot)
        axs[0, 1].imshow(gray, cmap='gray')
        axs[0, 1].set_title("Grayscale Image")
        axs[0, 1].axis('on')

        # Show Blurred Image (3rd subplot)
        axs[0, 2].imshow(blur, cmap='gray')
        axs[0, 2].set_title("Blurred Image")
        axs[0, 2].axis('on')

        # Show Dilated Image (4th subplot)
        axs[1, 0].imshow(dilated, cmap='gray')
        axs[1, 0].set_title("Dilated Image")
        axs[1, 0].axis('on')

        # Show Contoured Image (5th subplot)
        contour_img = rgb.copy()
        cv2.drawContours(contour_img, cnt, -1, (255, 0, 0), 2)
        axs[1, 1].imshow(contour_img)
        axs[1, 1].set_title("Contours Image")
        axs[1, 1].axis('on')

        # Leave axs[1, 2] (bottom-right) empty

        # Count and display number of objects
        object_count = len(cnt)
        self.label.config(text=f"Image: {image_name}, Object Count: {object_count}")

        # Adjust layout
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

    def next_image(self):
        self.index = (self.index + 1) % len(image_names)
        self.display_image(self.index)

    def prev_image(self):
        self.index = (self.index - 1) % len(image_names)
        self.display_image(self.index)

# Start the GUI
if __name__ == "__main__":
    app = ImageNavigator()
    app.mainloop()
