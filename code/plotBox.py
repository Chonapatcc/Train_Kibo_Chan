import cv2

def draw_box(image, x, y, width, height, color=(0, 255, 0), thickness=2):
  """
  Draws a box on an image with specified coordinates, width, height, color, and thickness.

  Args:
      image: A NumPy array representing the image.
      x: The x-coordinate of the top-left corner of the box.
      y: The y-coordinate of the top-left corner of the box.
      width: The width of the box in pixels.
      height: The height of the box in pixels.
      color: A tuple representing the BGR color of the box (default green).
      thickness: The thickness of the box lines in pixels (default 2).

  Returns:
      A NumPy array representing the image with the box drawn on it.
  """

  # Ensure coordinates and dimensions are within image boundaries
  image_height, image_width, _ = image.shape
  x = max(0, min(x, image_width - width))  # Clamp x within image width
  y = max(0, min(y, image_height - height))  # Clamp y within image height

  # Draw the rectangle on the image
  top_left = (x, y)
  bottom_right = (x + width, y + height)
  cv2.rectangle(image, top_left, bottom_right, color, thickness)

  return image

def read_file_per_line(filename):
  """
  Reads a text file line by line and processes each line.

  Args:
      filename: The name of the file to read from (including .txt extension).
  """

  # Open the file in read mode
  with open(filename, 'r') as file:
    # Read each line using a for loop
    for line in file:
      # Process the line (replace 'print(line.strip())' with your desired processing)
      lost_item , pic , time , position = line.split(", ")
      lost_item = lost_item.split(" ")[1]
      pic = pic.split(" ")[1]

      image = cv2.imread(f"D:/trainKibo/{lost_item}_placed_image_{pic}.jpg")
      x_min,y_min,x_max,y_max = [int(x) for x in (position.split(" ")[1]).split(",")]
      # Define box coordinates, width, height, and color (optional)
      box_x = x_min # Adjust these values as needed
      box_y = y_min
      box_width = x_max - x_min 
      box_height = y_max - y_min
      box_color = (255, 0, 0)  # Optional: Change color to blue

      # Draw the box on the image
      image_with_box = draw_box(image.copy(), box_x, box_y, box_width, box_height, color=box_color)
      # Save the image with the box
      cv2.imwrite(f"D:/trainKibo/{lost_item}_placed_image_{pic}.jpg", image_with_box)
# Example usage
filename = "D:/trainKibo/code/data.txt"

read_file_per_line(filename)


# Load the image (replace with your image path)

