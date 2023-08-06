Environment configuration:  pytorch:0.4.1 python:3.6 cuda:9.0
SAINT:  Spatially Aware Interpolation NeTwork for Medical Slice Synthesis
step1:  .nii->.pt 
           from py_SAINT.STAGE1 import nii2pickle
           nii2pickle.nii2pt(ori_dir_path,output_file_path)
eg: nii2pickle.nii2pt("/home1/mksun/xh_data/273data-yscl/1T2/1/002_OCor_T2_FRFSE/","/home1/mksun/SAINT/Data/Stage1_Input/TEST/HR/")

           ori_dir_path:  file path containing .nii
           output_file_path:  file path of the generated .pt
step2:  Interpolate with sag and cor view respectively
           from py_SAINT.STAGE1 import interpolation
           interpolation.get_Stage1_result (scale ='4',save =/path/ ,dir_data ='/path/',n_colors =3 ,n_GPUs =1,rgb_range =4000, view ='sag',gpu='0')
           interpolation.get_Stage1_result (scale ='4',save =/path/ ,dir_data ='/path/',n_colors =3 ,n_GPUs =1,rgb_range =4000, view ='cor',gpu='0')
eg:interpolation.get_Stage1_result (scale ='4',save ="/home1/mksun/SAINT/Data/Stage1_output_sag_cor/" ,dir_data ='/home1/mksun/SAINT/Data/Stage1_Input/',n_colors =3 ,n_GPUs =1,rgb_range =4000, view ='cor',gpu='0')
eg:interpolation.get_Stage1_result (scale ='4',save ="/home1/mksun/SAINT/Data/Stage1_output_sag_cor/" ,dir_data ='/home1/mksun/SAINT/Data/Stage1_Input/',n_colors =3 ,n_GPUs =1,rgb_range =4000, view ='sag',gpu='0')

           scale:  super resolution scale (eg:2,3,4,6)
           save:  file path of save           
           dir_data:  dataset directory (Note that the dir_data path should point to a folder that contains subfolders named  'TEST', each of which needs to have a 'HR' and 'LR' subfolder, 
                       'HR' is high resolution file , 'LR' is low resolution file. Data should go accordingly in this structure.
           n_colors:  number of channels to use
           n_GPUs:  number of GPUs
           rgb_range:  maximum value of RGB
           view:  view of interpolation (Note the --view option performs inference on the volume from either the sagittal or coronal axis. Note that the whether it's actually sagittal or coronal depends on the oritentation of the data.)
step3:  Before going to the RFN stage, sagittal and coronal-wise SR'ed volume needs to be recombine into a single volume for inference. In simple terms just concatenate them in the first dimension, coronal SR goes in channel 0 and             sagittal SR goes in channel 1. 
           from py_SAINT.STAGE1.process import cor_sag_comb_test
           cor_sag_comb_test.comb_cor_sag(files_dir='/path/',input_sag_cor_dir='/path/',out_dir='/path/', scale=4)
           eg:cor_sag_comb_test.comb_cor_sag(files_dir='/home1/mksun/SAINT/Data/Stage1_Input/TEST/HR/',input_sag_cor_dir='/home1/mksun/SAINT/Data/Stage1_output_sag_cor/results/raw/',out_dir='/home1/mksun/SAINT/Data/combine_cor_sag_out/TEST/', scale=4)
           files_dir:  dataset directory
           input_sag_cor_dir:  path to the folder containing sag and cor
           out_dir:  generated combine path
           scale:  super resolution scale
step4:  Residual-Fusion
           from py_SAINT.STAGE2 import fuse
           fuse.get_Stage2_result(save ='/path/',dir_data ='/path/' ,n_GPUs =1 ,rgb_range =4000,gpu='0')
eg: fuse.get_Stage2_result(save ='/home1/mksun/SAINT/Data/out_fuse/',dir_data ='/home1/mksun/SAINT/Data/combine_cor_sag_out/' ,n_GPUs =1 ,rgb_range =4000,gpu='0')
           save:  file path of save  
           dir_data:  step3_out_dir
           n_GPUs:  number of GPUs
           rgb_range:  maximum value of RGB
(option)：.pt->.nii
           from py_SAINT.STAGE1 import pt2nii
           pt2nii.pt2nii(ori_nii_dir_path, pt_dir_path,nii_dir_path)
           nii_dir_path: nii_output_dir
eg：pt2nii.pt2nii(ori_nii_dir_path='/home1/mksun/xh_data/273data-yscl/1T2/1/002_OCor_T2_FRFSE/',pt_dir_path='/home1/mksun/SAINT/Data/out_fuse/results/raw/',nii_dir_path='/home1/mksun/SAINT/Data/final_nii/')