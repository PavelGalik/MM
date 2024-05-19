#script for automatical cropping and saving the MM images, labels, and masks
import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import re

#path to data
folder = "E:/Data"
minimum_vec = []
maximum_vec = []
#each file in the folder, path definition
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    file_name = os.path.basename(file_path)
    file_name = file_name.lower()
    file_path2 = os.path.join(file_path, "CaSupp_data_nifti", file_name + "_CaSupp_25.nii.gz")
    file_path3 = os.path.join(file_path, "CaSupp_data_nifti", file_name + "_CaSupp_25.nii.gz")
    mask_path = os.path.join(file_path, "Spine_labels","NN_Unet", file_name + "_spine_seg_nnUNet.nii.gz")
    #maska_cesta = os.path.join(cesta_k_souboru, "Spine_labels","Spine_analyzer", nazev_souboru + "_spine_seg_SA.nii.gz")
    
    
    #data loading
    data_img = nib.load(file_path2)
    nifti_data = data_img.get_fdata()
    data = nifti_data
    data_img2 = nib.load(file_path3)
    nifti_data2 = data_img2.get_fdata()
    nifti_mask = nib.load(mask_path)
    nifti_data_mask = nifti_mask.get_fdata()
    uint8_array = nifti_data_mask.astype(np.uint8)
    mask = uint8_array
    # mask[mask > 0] = 1
  
   
    
    
    #boundaries detection
    white_pixel_coords = np.transpose(np.nonzero(mask))
    
    
    mid_x = mask.shape[1] // 2
    left_coords = white_pixel_coords[white_pixel_coords[:, 1] < mid_x]
    right_coords = white_pixel_coords[white_pixel_coords[:, 1] >= mid_x]
    # left_coords = left_coords[19:]
    # left_coords = left_coords[:-19]
    # right_coords = right_coords[19:]
    # right_coords = right_coords[:-19]
    if len(left_coords) == 0 or len(right_coords) == 0:
        mid_x = (mask.shape[1] // 2) + 1
        left_coords = white_pixel_coords[white_pixel_coords[:, 1] < mid_x]
        right_coords = white_pixel_coords[white_pixel_coords[:, 1] >= mid_x]
        # left_coords = left_coords[19:]
        # left_coords = left_coords[:-19]
        # right_coords = right_coords[19:]
        # right_coords = right_coords[:-19]
    
    if len(left_coords) == 0 or len(right_coords) == 0:
        mid_x = (mask.shape[1] // 2) - 1
        left_coords = white_pixel_coords[white_pixel_coords[:, 1] < mid_x]
        right_coords = white_pixel_coords[white_pixel_coords[:, 1] >= mid_x]
        # left_coords = left_coords[19:]
        # left_coords = left_coords[:-19]
        # right_coords = right_coords[19:]
        # right_coords = right_coords[:-19]
    
    if len(left_coords) == 0 or len(right_coords) == 0:
        mid_x = mask.shape[1] // 3
        left_coords = white_pixel_coords[white_pixel_coords[:, 1] < mid_x]
        right_coords = white_pixel_coords[white_pixel_coords[:, 1] >= mid_x]
        # left_coords = left_coords[19:]
        # left_coords = left_coords[:-19]
        # right_coords = right_coords[19:]
        # right_coords = right_coords[:-19]
    
    left_lowest_point = np.min(left_coords, axis=0)
    left_highest_point = np.max(left_coords, axis=0)
    
    right_lowest_point = np.min(right_coords, axis=0)
    right_highest_point = np.max(right_coords, axis=0)
    
    maximum = 0
    minimum = 0
    left_lowest_point = left_lowest_point[1]
    right_lowest_point = right_lowest_point[1]
    left_highest_point = left_highest_point[1]
    right_highest_point = right_highest_point[1]
    
    if left_lowest_point < right_lowest_point:
        minimum = left_lowest_point
    else:
        minimum = right_lowest_point
            
    if left_highest_point >right_highest_point:
        maximum = left_highest_point
    else:
        maximum = right_highest_point
    minimum_vec.append(minimum)
    maximum_vec.append(maximum)
    
    
    #image saving
    cropped_data_img_auto = nifti_data[0:data.shape[0], minimum-10:maximum+10, 0:data.shape[2]]
    cropped_data = nib.Nifti1Image(cropped_data_img_auto, data_img.affine)
    
    
    mask_cropped = nifti_data_mask[0:data.shape[0], minimum-10:maximum+10, 0:data.shape[2]]
    mask_cropped_nifti = nib.Nifti1Image(mask_cropped, data_img.affine)
    mask_save = os.path.join(r"E:\modely_final_all\pater_seg_902\temp",file_name+'_Conv_Ca25_0002.nii.gz' )
    nib.save(mask_cropped_nifti, mask_save)
    


#cropping of ground true data
pattern = r"m.+\.nii"

#path definition
folder_lesions = "E:\Data_validace_Valek"
k=0
#data loading
for file in os.listdir(folder_lesions):
    if re.match(pattern, file):
        
        path_to_files = os.path.join(folder_lesions, file)
        name = os.path.basename(path_to_files)
        file_name = os.path.splitext(os.path.basename(name))[0]
        file_name = os.path.splitext(os.path.basename(file_name))[0]
        file_name = file_name.lower()
        
        data_img = nib.load(path_to_files)
        nifti_data = data_img.get_fdata()
         
        #data cropping
        cropped_data_img_auto_lesions = nifti_data[0:nifti_data.shape[0], minimum_vec[k]-10:maximum_vec[k]+10, 0:nifti_data.shape[2]]
        cropped_data_img_auto_leze = nib.Nifti1Image(cropped_data_img_auto_lesions, data_img.affine)
        
        #data saving
        path_save = os.path.join("E:\leze_temp",file_name+'_monoE40.nii.gz' )
        nib.save(cropped_data_img_auto_leze, path_save)
        k = k+1
        
