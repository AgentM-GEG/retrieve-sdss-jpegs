import SciServer
from SciServer import SkyServer
import matplotlib.pyplot as plt
from astropy.io import ascii, fits
from PIL import Image
from multiprocessing.pool import Pool
import itertools
import time
import tqdm
import numpy as np

def download_image(info):
    info_type ='ra_dec'
    obj_info_search_DR = "DR16" # Data release to be used to query the ObjID, PetroR90 information
    image_data_release = "DR7" 
    try:
        if info_type == 'ra_dec':
            ra, dec = info #unpack the RA and DEC info

            object_search_data =  SciServer.SkyServer.objectSearch(ra= ra, dec = dec, dataRelease=obj_info_search_DR) # Query the object information
            object_id = object_search_data[0]['Rows'][0]['objId'] # grab the ObjID 
            sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s"%(object_id) # set up SQL query to retrieve PetroR50_r
            queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease=obj_info_search_DR) # queried data

            petroR90 = queried_data['PetroR90_r'].values.item() # grab the PetroR90

    #         print('Petro R90 = %s'%(petroR90))
    #         print('Arcsec/pix = %s'%(petroR90 * 0.02)) # Scale to be used for cutouts, based on details from Willet et al.,

            required_side_length = 424 # Pixels per side; use round(150/(petroR90 * 0.02)) if in case you want 150 arcsec per side.
            # print('Arcsec per side = %s'%(side_length * petroR90 * 0.02))
    #         print('Required side length [pix] = %s'%required_side_length)
        elif info_type =='ID':
            sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s" %(info) # If we have ObjIDs, directly setup SQL query.
            queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease=image_data_release) # query from the specified DR above
            print(queried_data)
            petroR90 = queried_data['PetroR90_r'].values.item() # retrive RA, DEC, and PetroR90
            ra = queried_data['ra'].values.item()
            dec = queried_data['dec'].values.item()
            print('Petro R90 = %s' % (petroR90))
            print('Arcsec/pix = %s' % (petroR90 * 0.1))

            required_side_length = 424 #round(150/(petroR90 * 0.02)); same comment as above
            print('Required side length [pix] = %s' % required_side_length)


        img = SkyServer.getJpegImgCutout(ra = ra, dec = dec,
                                         scale = 0.02 *petroR90,
                                         width = required_side_length, height = required_side_length,
                                         dataRelease = image_data_release) # we have all the needed information, generate a cutout.

        im = Image.fromarray(img)
        im.save('/home/fortson/manth145/data/GZ1_Images/%s_%s.jpg'%(object_id, image_data_release))
    except:
        pass
    return

catalog = ascii.read('/home/fortson/manth145/data/GZ2-GAN/catalogs/GZ1_Converted_Information_Table3.csv', format='csv')

info = np.array(catalog[['RA_deg', 'DEC_deg']])[150000:200000]

pl = Pool(processes=24)
result = list(tqdm.tqdm(pl.imap(download_image,  list(info),chunksize=1), total=len(info), ascii=True))