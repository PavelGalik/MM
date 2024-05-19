#script for defining each spinal segment according to numbers of vertebrae in the CT scans
import os
import numpy as np
import nibabel as nib

#path to data
folder = r"E:\modely_final_all\pater_seg_902"
minimum_vec = []
maximum_vec = []

#each file in the folder, path definition
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    file_name = os.path.basename(file_path)
    file_name = file_name.lower()
    
    #data loading loading
    if "myel" in file_name:
        data_path = os.path.join(file_path)#, nazev_souboru + ".nii.gz")
        
        data_img = nib.load(data_path)
        nifti_data = data_img.get_fdata()
        data = nifti_data
        nifti_img = data_img
        nifti_data = nifti_img.get_fdata()
        uint8_array = nifti_data.astype(np.uint8)
        mask = nifti_data
             

        #getting the spinal segment               
        mask = np.logical_and(nifti_data >= 20, nifti_data <= 24) #according to the number of vertebrae for each spinal segment                   
        nifti_data[mask] = nifti_data[mask]
        nifti_data[~mask] = 0
            
        mask = (nifti_data > 0).astype(np.uint8)        
        nifti_data_s =  nib.Nifti1Image(mask, nifti_img.affine)
        
        #saving data 
        path_save = os.path.join(r"E:\modely_final_all\pater_seg_902\bedro",file_name+"_bedro.nii.gz")
        nib.save(nifti_data_s, path_save)




