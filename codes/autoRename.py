#script for automatical renaming of files
import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2

#file definition
folder = 'E:\Cropped_data'
i = 0
#each file in the folder, path definition
for file in os.listdir(folder):
    i = i + 1
    file_path = os.path.join(folder, file)
    file_name = os.path.basename(file_path)
    file_name = file_name
    file_name_2 = os.path.splitext(os.path.basename(file_path))[0]
    file_name_2 = os.path.splitext(os.path.basename(file_name_2))[0]
    
    
    format_i = "{:03d}".format(i)

    #rename
    new_name = "{}_{}".format(file_name_2, format_i+"_0000"+".nii.gz")
    data_img = nib.load(file_path)
    nifti_data = data_img.get_fdata()
    data = nifti_data
    cropped_data_img_auto = nib.Nifti1Image(data, data_img.affine)
    #save
    path_save = os.path.join('E:\DatasetConvCroped600_Myel',new_name )
    nib.save(cropped_data_img_auto, path_save)