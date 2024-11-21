import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from photutils import DAOStarFinder



def get_data(filename):
    with fits.open(filename) as hdul:
        image_data = hdul[0].data
    return image_data

def starfind(image_data):
    mean = np.mean(image_data)
    std = np.std(image_data)
    daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)  
    data2 = image_data.copy()

    try: 
        sources = daofind(image_data - mean)
        x_positions = sources['xcentroid'].astype(int)
        y_positions = sources['ycentroid'].astype(int)
        for x, y in zip(x_positions, y_positions):
            if 0 <= x < data2.shape[1] and 0 <= y < data2.shape[0]: 
                data2[y, x] = 0
            else:
                pass
    except:
        pass
    return data2


def get_contour_levels(image_data, num_levels):
    percentiles = np.linspace(0, 30, num_levels)
    contour_levels = np.percentile(image_data, percentiles)
    return contour_levels


def draw_contours(image_data, contour_levels):
    contours = plt.contour(image_data, levels=contour_levels, colors='r')
    contour_coords = []
    for collection in contours.collections:
        for path in collection.get_paths():
            coords = path.vertices
            coords = coords[:, [1, 0]]  # Swap columns to change from (x, y) to (y, x)
            contour_coords.append(coords)
    plt.close() 
    return contour_coords

def contour_to_region_string(contour_coords):
    region_strings = []
    for coords in contour_coords:
        # Convert the coordinates to a region string (polygon format)
        coords = coords[:, ::-1]  # Swap x and y if necessary
        region_string = f'polygon({",".join(f"{x},{y}" for x, y in coords)})'
        region_strings.append(region_string)
    return "\n".join(region_strings)

def save_regions_to_file(contour_coords):
    region_string = contour_to_region_string(contour_coords)
    with open("125gauss4.reg", 'w') as reg_file:
        reg_file.write(region_string)

# Main execution
filename = '125wgauss5_trimmed.fits'
data = get_data(filename)
modified_data = starfind(data)
contour_levels = get_contour_levels(modified_data, 5)
contour_coords = draw_contours(modified_data, contour_levels)
save_regions_to_file(contour_coords)
