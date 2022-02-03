import SciServer
from SciServer import SkyServer
import matplotlib.pyplot as plt
from astropy.io import ascii

#
info = [(154.48836231, 41.11430498)]
info_type ='ra_dec'

# info = [1237671932283322445]
# info_type ='ID'

for iteration, each_info in enumerate(info):
    if info_type == 'ra_dec':
        ra, dec = each_info

        object_search_data =  SciServer.SkyServer.objectSearch(ra= ra, dec = dec, dataRelease='DR16')
        object_id = object_search_data[0]['Rows'][0]['objId']
        sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s"%(object_id)
        queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease=None)

        petroR90 = queried_data['PetroR90_r'].values.item()

        print('Petro R90 = %s'%(petroR90))
        print('Arcsec/pix = %s'%(petroR90 * 0.02))

        required_side_length = round(150/(petroR90 * 0.02))
        # print('Arcsec per side = %s'%(side_length * petroR90 * 0.02))
        print('Required side length [pix] = %s'%required_side_length)
    elif info_type =='ID':
        sql_query = "SELECT p.ra, p.dec, p.ObjID, p.PetroR90_r from PhotoPrimary p WHERE p.objID = %s" % (each_info)
        queried_data = SciServer.SkyServer.sqlSearch(sql_query, dataRelease='DR16')
        print(queried_data)
        petroR90 = queried_data['PetroR90_r'].values.item()
        ra = queried_data['ra'].values.item()
        dec = queried_data['dec'].values.item()
        print('Petro R90 = %s' % (petroR90))
        print('Arcsec/pix = %s' % (petroR90 * 0.1))

        required_side_length = 424 #round(150/(petroR90 * 0.02))
        print('Required side length [pix] = %s' % required_side_length)

    image_data_release = "DR16"
    img = SkyServer.getJpegImgCutout(ra = ra, dec = dec,
                                     scale = 0.02 *petroR90,
                                     width = required_side_length, height = required_side_length,
                                     dataRelease = image_data_release)
    plt.imshow(img)

    plt.axis('off')
    if info_type == 'ra_dec':
        plt.savefig('/Users/kameswaramantha/Dropbox/bharath/PostDoc_Research/data/GxZoo/Segmentation_Analysis/mosaics/%s_%s.jpg'%(object_id, image_data_release), format='png', bbox_inches='tight', pad_inches=0, overwrite=True)
    elif info_type == 'ID':
        plt.savefig(
            '/Users/kameswaramantha/Dropbox/bharath/PostDoc_Research/data/GxZoo/Segmentation_Analysis/mosaics/%s_%s.jpg' % (
            each_info, image_data_release), format='png', bbox_inches='tight', pad_inches=0, overwrite=True)

    # plt.show()
    print('Done %s'%(iteration))
