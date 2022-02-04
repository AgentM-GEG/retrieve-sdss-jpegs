'''
Install the SciServer module by unpacking the zip file provided in the repo. 

cd SciServer/py3
python3 setup.py install

Note: I made a small change to the getJpegCutout script that now pings an additional (old) server that hosts <DR12 JPEGs. 

If you download the current module from https://github.com/sciserver/SciScript-Python, it will fail e.g., DR7.
'''

# Import the necessary modules
import SciServer
from SciServer import SkyServer
import matplotlib.pyplot as plt
from astropy.io import ascii

# If the info you are providing is a tuple of (RA, DEC) positions, then use the following. Load a catalog and pass a list of tuples to iteratively 
# fetch the images.
info = [(154.48836231, 41.11430498)]
info_type ='ra_dec'

'''
If you have ObjIDs (unique to each data release), then comment the above and use the following.
'''
# info = [1237671932283322445]
# info_type ='ID'

obj_info_search_DR = "DR16" # Data release to be used to query the ObjID, PetroR90 information
image_data_release = "DR7" # Data release from which the Jpeg should be queried.


for iteration, each_info in enumerate(info): #iterate over the loop
    if info_type == 'ra_dec':
        ra, dec = each_info #unpack the RA and DEC info

        object_search_data =  SciServer.SkyServer.objectSearch(ra= ra, dec = dec, dataRelease=obj_info_search_DR) # Query the object information
        object_id = object_search_data[0]['Rows'][0]['objId'] # grab the ObjID 
        sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s"%(object_id) # set up SQL query to retrieve PetroR50_r
        queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease=obj_info_search_DR) # queried data

        petroR90 = queried_data['PetroR90_r'].values.item() # grab the PetroR90

        print('Petro R90 = %s'%(petroR90))
        print('Arcsec/pix = %s'%(petroR90 * 0.02)) # Scale to be used for cutouts, based on details from Willet et al.,

        required_side_length = 424 # Pixels per side; use round(150/(petroR90 * 0.02)) if in case you want 150 arcsec per side.
        # print('Arcsec per side = %s'%(side_length * petroR90 * 0.02))
        print('Required side length [pix] = %s'%required_side_length)
    elif info_type =='ID':
        sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s" % (each_info) # If we have ObjIDs, directly setup SQL query.
        queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease=obj_info_search_DR) # query from the specified DR above
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
    plt.imshow(img)

    plt.axis('off')
    # save the figures, NOTE: change the paths to save at your locations.
    if info_type == 'ra_dec':
        plt.savefig('/Users/kameswaramantha/Dropbox/bharath/PostDoc_Research/data/GxZoo/Segmentation_Analysis/mosaics/%s_%s.jpg'%(object_id, image_data_release), format='png', bbox_inches='tight', pad_inches=0, overwrite=True)
    elif info_type == 'ID':
        plt.savefig(
            '/Users/kameswaramantha/Dropbox/bharath/PostDoc_Research/data/GxZoo/Segmentation_Analysis/mosaics/%s_%s.jpg' % (
            each_info, image_data_release), format='png', bbox_inches='tight', pad_inches=0, overwrite=True)

    # plt.show()
    print('Done %s'%(iteration))
