#cropping the CT data according to the spinal mask (different segments of the spine)
import nibabel as nib
import numpy as np
import os

#path to data
folder = r"E:\modely_final_all\pater_seg_902\prediction" #r"E:\modely_final_all\pater_seg_902\wholeCT"
i = 0

#each file in the folder, path definition
for file in os.listdir(folder):
    path_file = os.path.join(folder, file)
    file_name = os.path.basename(path_file)
    file_name = file_name.lower()
    
    #file loading 
    if "myel" in file_name:
        i += 1
        
        nifti_img = nib.load(path_file)
        nifti_data = nifti_img.get_fdata()
        nifti_shape = nifti_data.shape

        
        
        spine_name = r"E:\modely_final_all\pater_seg_902\hrud\myel_{:03d}_monoe40_ca25_0002.nii.gz_hrud.nii.gz".format(i)#r"E:\modely_final_all\pater_seg_902\bedro\myel_{:03d}_monoe40_ca25_0002.nii.gz_bedro.nii.gz".format(i)
        spine_mask_img = nib.load(spine_name)
        spine_mask_data = spine_mask_img.get_fdata().astype(int)
        spine_mask_shape = spine_mask_data.shape
        
        #if the dimensions are different, fix them
        if nifti_shape != spine_mask_shape:
            spine_mask_data_resized = np.zeros_like(nifti_data)
            min_shape = np.minimum(nifti_shape, spine_mask_shape)
            spine_mask_data_resized[:min_shape[0], :min_shape[1], :min_shape[2]] = spine_mask_data[:min_shape[0], :min_shape[1], :min_shape[2]]
            spine_mask_data = spine_mask_data_resized

        # data cropping according to the mask
        cropped_ct_data = nifti_data * spine_mask_data
        #biinary mask
        cropped_ct_data_bin = (cropped_ct_data > 0).astype(np.uint8)
        
        # saving the data
        nifti_data_cropped = nib.Nifti1Image(cropped_ct_data_bin, nifti_img.affine)
        path_save = os.path.join(r"E:\modely_final_all\pater_seg_902\hrud\prediction", f"{str(i).zfill(3)}_hrud_prediction.nii.gz")
        nib.save(nifti_data_cropped, path_save) 

