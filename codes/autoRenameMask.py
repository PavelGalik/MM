#script for automatical rename of mask files
import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2


# define the path to data
folder = 'E:\Data'
i = 0
j=0
#each file in the folder, path definition
for file in os.listdir(folder):
    i = i + 1
    
    path_to_file = os.path.join(folder, file)
    file_name = os.path.basename(path_to_file)
    mask_path = os.path.join(path_to_file, "Spine_labels","NN_Unet", file_name + "_spine_seg_nnUNet.nii.gz")
    
    name2 = os.path.splitext(os.path.basename(mask_path))[0]
    name2 = os.path.splitext(os.path.basename(name2))[0]
    name2 = name2.lower()
    

   #file rename
    format_i = "{:03d}".format(i)
    if i <= 10:
        new_name = "{}_{}".format("healthy", format_i+"_Ca25"+"_0001"+".nii.gz")
        data_img = nib.load(mask_path)
        nifti_data = data_img.get_fdata()
        data = nifti_data
        cropped_data_img_auto = nib.Nifti1Image(data, data_img.affine)
        
        path_save = os.path.join('E:\Dataset777_Ca25',new_name )
        nib.save(cropped_data_img_auto, path_save)
    else:
        
        j=j+1
        format_j = "{:03d}".format(j)
        new_name = "{}_{}".format("myel", format_j+"_Ca25"+"_0001"+".nii.gz")
        data_img = nib.load(mask_path)
        nifti_data = data_img.get_fdata()
        data = nifti_data
        cropped_data_img_auto = nib.Nifti1Image(data, data_img.affine)
        
        path_save = os.path.join('E:\Dataset777_Ca25',new_name )
        nib.save(cropped_data_img_auto, path_save)
    
    