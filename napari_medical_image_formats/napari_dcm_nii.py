# -*- coding: utf-8 -*-
__version__ = "0.1"

import numpy as np
from napari_plugin_engine import napari_hook_implementation
import pydicom as dicom
import SimpleITK as sitk

def dcm_nii_reader(path: str):
	if path.endswith(".dcm"):
		
		dcm_read = dicom.dcmread(path)
		dcm_array = dcm_read.pixel_array
		return [(dcm_array,)]
	elif path.endswith(".nii") or path.endswith(".nii.gz") :
		
		nii_read = sitk.ReadImage(path)
		nii_array = sitk.GetArrayFromImage(nii_read)
		return [(nii_array,)]

@napari_hook_implementation
def napari_get_reader(path):
	if isinstance(path, str) and path.endswith((".dcm", ".nii", ".nii.gz")):
		return dcm_nii_reader
	
	return None

