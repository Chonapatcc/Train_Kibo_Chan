import cv2
import random
import os
def random_place_image(id,i,time,background_image, image_to_place, resize_factor=1.0):
  """
  Randomly places the image_to_place onto the background_image with optional resizing.

  Args:
      background_image: A NumPy array representing the background image.
      image_to_place: A NumPy array representing the image to be placed.
      resize_factor: A float between 0.0 and 1.0 to scale the placed image (optional).

  Returns:
      A NumPy array representing the modified background image with the placed image.
  """

  # Get image dimensions
  background_height, background_width, background_channels = background_image.shape
  image_height, image_width, image_channels = image_to_place.shape

  # Scale the image to place if necessary
  if resize_factor > 0.0 and resize_factor < 1.0:
    new_width = int(image_width * resize_factor)
    new_height = int(image_height * resize_factor)
    image_to_place = cv2.resize(image_to_place, (new_width, new_height))
    image_height, image_width, _ = image_to_place.shape

  # Ensure image to place fits within the background after potential resize
  if image_height > background_height or image_width > background_width:
    raise ValueError("Image to place is larger than background image even after resizing.")

  # Generate random coordinates for top-left corner of placed image
  max_y = background_height - image_height
  max_x = background_width - image_width
  random_y = random.randint(0, max_y)
  random_x = random.randint(0, max_x)

  # Extract region of interest from background image
  roi = background_image[random_y:random_y + image_height, random_x:random_x + image_width]
  writeFile(id,i,time,random_x,random_y,random_x+image_width,random_y+image_height)
  # Create a mask for the image to place (alpha channel with transparency)
  mask = cv2.cvtColor(image_to_place, cv2.COLOR_BGR2BGRA)[:, :, 3:4] / 255.0  # Isolate and normalize alpha channel
  mask_inverted = 1.0 - mask  # Invert mask for background transparency

  # Combine the placed image and background using weighted addition
  roi = cv2.addWeighted(mask * image_to_place[:, :, :3], 1.0, mask_inverted * roi, 1.0, 0)

  # Update the background image with the placed image
  background_image[random_y:random_y + image_height, random_x:random_x + image_width] = roi

  return background_image

def rotatePicture(image):
  # Load the image (replace with your image path)
  image = image.copy()

  # Define the rotation angle in degrees (positive for clockwise)
  rotation_angle = random.randrange(0,360) # You can change this value

  # Get image dimensions
  image_height, image_width, _ = image.shape

  # Create a rotation matrix for the specified angle
  rotation_matrix = cv2.getRotationMatrix2D((image_width / 2, image_height / 2), rotation_angle, 1.0)

  # Rotate the image using the rotation matrix
  rotated_image = cv2.warpAffine(image, rotation_matrix, (image_width, image_height))

  # Display the original and rotated images
  return rotated_image
def writeFile(id,i,time,x_min,y_min,x_max,y_max):
  with open("D:/trainKibo/code/data.txt", 'a') as file:
    # Write the content to the file
    file.write(f"lost_item {id}, Pic {i}, place_times {time}, position {x_min},{y_min},{x_max},{y_max}\n")
  return 
def changeSize(image):
  # Load the image (replace with your image path)
  image = image.copy()

  # Define the new width and height for the resized image
  size = random.randrange(50,200)
  new_width = size
  new_height = size

  # Resize the image using interpolation (optional)
  resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)  # You can change the interpolation method

  return resized_image
# Load the blank image (replace with your path to a 200x200 image)
#####
# Specify the folder path

folder_path = "lost_item_images/"

# Get all filenames in the folder
filenames = os.listdir(folder_path)

# Filter for image files (optional)
image_files = [f for f in filenames if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))]

print("Image files in", folder_path, ":")
id =0 
for f in image_files:
  id+=1
  blank_image = cv2.imread("D:/trainKibo/images.jpg")
  # Load the image to place (replace with your image path)
  image_to_place = cv2.imread(f"D:/trainKibo/lost_item_images/{f}")
  
  # Create a list to store the final images
  
  placed_images = []


  # Randomly place the image 200 times and create new images
  for i in range(1,10+1):
    placed_image = random_place_image(id,i,1,blank_image.copy(),changeSize(rotatePicture(image_to_place)))
    for i2 in range(1,random.randrange(0,5)+1):
      placed_image = random_place_image(id,i,1+i2,placed_image,changeSize(rotatePicture(image_to_place)))
    placed_images.append(placed_image)


  # (Optional) Save the placed images (replace with your desired filenames and output path)
  for i, image in enumerate(placed_images):
    cv2.imwrite(f"{id}_placed_image_{i+1}.jpg", image)

  print("Image placement complete!")
