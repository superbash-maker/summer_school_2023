#########################################################################
#                           Dr Krishna Govender                         #
#                         Senior Lecturer - UJ (DFC)                    #
#                               20 October 2022                         #
#                           Script to pull ligand                       #
#                           entries from PUBCHEM                        #
#                           Downloads SDF files to disk                 #
#                           Also gets CIDs of ligands                   #
# If you starting fresh then you need to do the following               #
# Install Anaconda3                                                     #
# Use anaconda cmd to install pubchem with following options            #
# conda install -c bioconda pubchem -y                                  #
#########################################################################
import fileinput
import glob
import os
import pandas as pd
import pubchempy as pcp


# Read data from list of ligands
df = pd.read_csv('list.txt', sep=";", names=['Ligand Name','CID'])

# Check if sdfs directory exists
# If not create it
if os.path.exists('sdfs'):
   print('sdfs directory already exists')
else:
    os.mkdir('sdfs')

for index, rows in df.iterrows():
    print('Downloading', rows['Ligand Name'])
    # Download enteries based on the CID
    pcp.download('SDF', 'sdfs/'+rows['Ligand Name']+'.sdf', rows['CID'], 'cid', overwrite=True)

# Check if combined file already exists.
# If it does remove it
if os.path.exists('sdfs/ligand_library.sdf'):
    os.remove('sdfs/ligand_library.sdf')
    print('Removing existing ligand_library.sdf file')
else:
    print('Creating new ligand_library.sdf file')

with open('sdfs/ligand_library.sdf', 'w') as file:
    for index, rows in df.iterrows():
        read_files = glob.glob('sdfs/'+rows['Ligand Name']+'.sdf')
        input_lines = fileinput.input(read_files)
        file.writelines(input_lines)
print('DONE')