import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# Step 1: Setup
image_folder = 'images/'  # Your folder name
image_names = [f'img{i}.jpg' for i in range(1, 11)]  # img1.jpg to img10.jpg

# Dictionary to store image name and item count
image_counts = {}

# Step 2: Process each image
for image_name in image_names:
    image_path = os.path.join(image_folder, image_name)
    print(f"Loading {image_name}...")
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error loading {image_name}. Skipping...")
        continue

    print(f"\nProcessing {image_name}...")

    # Convert BGR to RGB for displaying original
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Show Original Image
    plt.figure(figsize=(5,5))
    plt.title("Original Image")
    plt.imshow(rgb)
    plt.show()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.figure(figsize=(5,5))
    plt.title("Grayscale Image")
    plt.imshow(gray, cmap='gray')
    plt.show()

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    plt.figure(figsize=(5,5))
    plt.title("Blurred Image")
    plt.imshow(blur, cmap='gray')
    plt.show()

    # Detect edges using Canny
    canny = cv2.Canny(blur, 30, 150, 3)
    plt.figure(figsize=(5,5))
    plt.title("Canny Edges")
    plt.imshow(canny, cmap='gray')
    plt.show()

    # Dilate the edges
    dilated = cv2.dilate(canny, (1, 1), iterations=2)
    plt.figure(figsize=(5,5))
    plt.title("Dilated Image")
    plt.imshow(dilated, cmap='gray')
    plt.show()

    # Find contours
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw contours on the RGB image
    contour_img = rgb.copy()
    cv2.drawContours(contour_img, cnt, -1, (255, 0, 0), 2)
    plt.figure(figsize=(5,5))
    plt.title("Contours Detected")
    plt.imshow(contour_img)
    plt.show()

    # Step 3: Save count to dictionary
    object_count = len(cnt)
    image_counts[image_name] = object_count

# Step 4: Final Output
print("\n--- Final Image Counts Dictionary ---")
print(image_counts)

# Step 5: Sorting Algorithms
# -------------------------------
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

# -------------------------------
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

# -------------------------------
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

# -------------------------------
# Timing and Sorting

# Counting Sort
start = time.time()
sorted_counting = counting_sort_dict(image_counts.copy())
end = time.time()
time_counting = end - start

# Merge Sort
start = time.time()
sorted_merge = merge_sort_dict(image_counts.copy())
end = time.time()
time_merge = end - start

# Selection Sort
start = time.time()
sorted_selection = selection_sort_dict(image_counts.copy())
end = time.time()
time_selection = end - start

# -------------------------------
# Results
print("\n--- Sorted Dictionaries ---")
print("\nCounting Sort Result:")
print(sorted_counting)

print("\nMerge Sort Result:")
print(sorted_merge)

print("\nSelection Sort Result:")
print(sorted_selection)

print("\n--- Timing ---")
print(f"Counting Sort Time: {time_counting:.10f} seconds")
print(f"Merge Sort Time: {time_merge:.10f} seconds")
print(f"Selection Sort Time: {time_selection:.10f} seconds")

# -------------------------------
# Conclusion based on timings
times = {
    'Counting Sort': time_counting,
    'Merge Sort': time_merge,
    'Selection Sort': time_selection
}

fastest_algorithm = min(times, key=times.get)

print("\n--- Conclusion ---")
print(f"The fastest sorting algorithm for this problem is **{fastest_algorithm}**.")
