import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import pyregion

def trim_fits_to_region(fits_file, region_file, output_file):
    # Open the FITS file and load the data and header
    hdul = fits.open(fits_file)
    # Assuming the image is in the primary HDU (index 0)
    data = hdul[0].data
    header = hdul[0].header
    wcs = WCS(header)
    
    # Read the region file (.reg)
    region = pyregion.open(region_file)

    # Convert region coordinates to pixel coordinates using WCS
    mask = region.get_mask(hdu=hdul[0])  # Using the hdu object while still open

    # Find the bounding box of the region mask
    y, x = np.where(mask)  # Get the indices of the mask
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Use the bounding box to trim the image
    trimmed_data = data[y_min:y_max+1, x_min:x_max+1]

    # Update the header with the new WCS for the trimmed region
    trimmed_wcs = wcs.slice((slice(y_min, y_max+1), slice(x_min, x_max+1)))
    header.update(trimmed_wcs.to_header())

    # Save the trimmed image to a new FITS file
    fits.writeto(output_file, trimmed_data, header, overwrite=True)

    # Close the HDU
    hdul.close()

    print(f"Trimmed image saved to {output_file}")

fits_file = '/Users/research/Desktop/ContourCode/n4418_f125w_gauss5.fits'
region_file = 'only_galaxy.reg'
output_file = '125wgauss5_trimmed.fits'

trim_fits_to_region(fits_file, region_file, output_file)
 