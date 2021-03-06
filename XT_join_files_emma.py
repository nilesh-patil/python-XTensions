# Imaris XTension
#
#  Copyright (C) 2018 Nilesh patil <nilesh.patil@rochester.edu>, MIT license
#
#    <CustomTools>
#      <Menu name = "Python plugins">
#          <Submenu name = "Data processing">
#               <Item name="Combine 2 datasets - Emma" icon="Python" tooltip="Combine two datasets to create a single output">
#                 <Command>PythonXT::XT_join_files_emma(%i)</Command>
#               </Item>
#           </Submenu>
#      </Menu>
#    </CustomTools>


import time
import ImarisLib
import os

import pandas as pd
from cvbi.gui import *

# Get All Statistics


def XT_join_files_emma(aImarisId):

    print('''
    #####################################################
    ###########     Extension started     ###############
    #####################################################
    ''')
    time.sleep(3)

    vImarisLib = ImarisLib.ImarisLib()
    vImaris = vImarisLib.GetApplication(aImarisId)

    imaris_file = vImaris.GetCurrentFileName()
    imaris_dir = os.path.dirname(imaris_file)
    imaris_name = os.path.basename(imaris_file)

    print('''
                    ************************************************
                    ************************************************
                    ************************************************
          All the rows from 1st file are going to be copied to the final dataset. 
          Only rows that match selected columns 'll be copied from 2nd dataset.
                    ************************************************
                    ************************************************
                    ************************************************
          ''')

    print('\nSelect first file to combine : Protrusions file \n')
    time.sleep(2)

    file_01 = get_file( window_title= 'Select File 01 to read :' ,
                        initial_dir = imaris_dir ,
                        filetypes = (("txt files","*.txt"),
                                     ("csv files","*.csv"),
                                     ("all files","*.*")),
                        w = 600 , h=400 )
    time.sleep(2)
    sep_01 = ','

    data_left = pd.read_csv(file_01, sep =sep_01)

    print('\nSelect second file to combine : Tracks file \n')
    time.sleep(2)

    file_02 = get_file( window_title= 'Select File 02 to read :' ,
                        initial_dir = imaris_dir ,
                        filetypes = (("txt files","*.txt"),
                                     ("csv files","*.csv"),
                                     ("all files","*.*")),
                        w = 600 , h=400 )
    time.sleep(2)
    sep_02 = ','

    data_right = pd.read_csv(file_02, sep =sep_02)

    time.sleep(2)
    join_type = 'left'
    data_out = pd.merge(left = data_left,
                        right = data_right,
                        how = join_type,
                        on=['frame','cell_id'],
                        suffixes = ('_first', '_second'))
    data_out.sort_values(by=['trackid', 'frame'], inplace = True)

    output_dir = get_dir( window_title = 'Select folder to save output' , initial_dir = imaris_dir )
    output_file = 'combined'
    output_file = create_window_for_input( default = output_file ,
                                           w = 700 , h = 200 ,
                                           window_text = 'Modify the file name for any changes' ,
                                           window_title = 'Provide your output file name' )

    try:
        print('Saving complete dataset.')
        time.sleep(1)
        output_path = output_dir+'/'+output_file+'.csv'
        data_save = data_out.copy()
        data_save.to_csv(output_path, index=False, sep=',')

        print('Saving subset of the dataset.')
        time.sleep(1)
        output_path = output_dir+'/'+output_file+'_subset.csv'
        data_save = data_out.loc[~data_out.trackid.isnull(),:].copy()
        data_save.to_csv(output_path, index=False, sep=',')

    except:
        print('''
        Calculations finished successfully but there was an error in saving your dataset. \n
        Try closing other open Imaris applications and then run this XTension. \n 
        Please do not forget to save your work.\n
        Please contact Nilesh Patil : nilesh.patil@rochester.edu if this problem persists \n
        ''')
        time.sleep(5)
        return

    print('''
    #####################################################
    ######          Extension finished             ######
    ######  Wait for 5s to close automatically     ######
    #####################################################
    ''')
    time.sleep(5)
