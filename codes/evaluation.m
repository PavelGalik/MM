%script for data evaluation

clc, close all, clear all

%Data loading
Label = niftiread("E:\modely_final_all\nnunet_metacentrum_example_902_monoE40_Ca25_MM\results\predict\Dataset902_monoE40_Ca25_MM\myel_070_monoE40.nii.gz");
Predict = niftiread("E:\modely_final_all\nnunet_metacentrum_example_901_monoE40_Conv_MM\results\predict\Dataset901_monoE40_Conv_MM\myel_070_monoE40.nii.gz");
Label = uint8(Label);

% Ensure the volumes have the same size
if size(Label) ~= size(Predict)
    error('Label and Predict volumes must have the same size.');
end


Label = double(Label);
Predict = double(Predict);

% DICE computation
dice_coef = dice(Predict(:), Label(:));


% binary mask - labeled data
groundTruthBinary = Label > 0;

% binary mask - predicted data
segmentedMaskBinary = Predict > 0;


% True Negative Count
TN = sum(groundTruthBinary(:) == 0 & segmentedMaskBinary(:) == 0);

% False Positive Count
FP = sum(groundTruthBinary(:) == 0 & segmentedMaskBinary(:) == 1);

% True Positive Count (TP)
TP = sum(groundTruthBinary(:) == 1 & segmentedMaskBinary(:) == 1);

% False Negative Count (FN) 
FN = sum(groundTruthBinary(:) == 1 & segmentedMaskBinary(:) == 0);

%specificity
specificity = TN / (TN + FP);
% sensitivity
sensitivity = TP / (TP + FN);


FPR = (FP)/(FP + TN);

FNR = 1 - sensitivity;

