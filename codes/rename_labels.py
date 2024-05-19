#script for automatical labels rename
import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import re

#path to data
pattern = r"m.+\.nii"
folder = "E:\leze_temp"

i = 0
j=0
#each file in the folder, path definition
for file in os.listdir(folder):
    if re.match(pattern, file):
        path_to_file = os.path.join(folder, file)
        
    i = i + 1
    
    path_file = os.path.join(folder, file)
    name_file = os.path.basename(path_file)
    mask_path = os.path.join(path_to_file)
    
    name = os.path.splitext(os.path.basename(mask_path))[0]
    name = os.path.splitext(os.path.basename(name))[0]
    name = name.lower()
    

   # data rename
    format_i = "{:03d}".format(i)
    if i <= 10:
        
        new_name = "{}_{}".format("healthy", format_i+"_monoE40_Ca25"+".nii.gz")#myel, healthy
        data_img = nib.load(mask_path)
        nifti_data = data_img.get_fdata()
        data = nifti_data
        #binary data
        binary_mask = np.where(nifti_data > 0, 1, 0).astype(np.uint8)
        cropped_data_img_auto = nib.Nifti1Image(binary_mask, data_img.affine)
        #data save
        path_save = os.path.join('E:\Dataset886_monoE40_Ca25',new_name )
        nib.save(cropped_data_img_auto, path_save)
    else:
        
        j=j+1
        format_j = "{:03d}".format(j)
        new_name = "{}_{}".format("myel", format_j+"_monoE40_Ca25"+".nii.gz")
        data_img = nib.load(mask_path)
        nifti_data = data_img.get_fdata()
        data = nifti_data
        #binary data
        binary_mask = np.where(nifti_data > 0, 1, 0).astype(np.uint8)
        cropped_data_img_auto = nib.Nifti1Image(binary_mask, data_img.affine)
        #data save
        path_save = os.path.join('E:\Dataset886_monoE40_Ca25',new_name )
        nib.save(cropped_data_img_auto, path_save)
    
    