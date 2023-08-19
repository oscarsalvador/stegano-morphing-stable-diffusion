import imageio
from skimage.transform import PiecewiseAffineTransform, warp

# Load the source and destination images
src_image = imageio.imread('source_image.jpg')
dst_image = imageio.imread('destination_image.jpg')

# Define the control points for the morphing
src_points = [(0, 0), (0, src_image.shape[0]), (src_image.shape[1], 0), (src_image.shape[1], src_image.shape[0])]
dst_points = [(0, 0), (0, dst_image.shape[0]), (dst_image.shape[1], 0), (dst_image.shape[1], dst_image.shape[0])]

# Compute the affine transformation between the control points
tform = PiecewiseAffineTransform()
tform.estimate(src_points, dst_points)

# Morph the source image towards the destination image
morphed_image = warp(src_image, tform)

# Save the morphed image
imageio.imwrite('morphed_image.jpg', morphed_image)


