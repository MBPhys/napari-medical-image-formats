# -*- coding: utf-8 -*-

"""
This module provides itk-based file writing functionality in the reader/writer plugin for napari.
"""
from pathlib import Path
import numpy as np
import itk
from itk_napari_conversion import image_layer_from_image
from napari_plugin_engine import napari_hook_implementation
import os
from typing import Any, List, Optional, Union
import napari
import os
import tempfile
import datetime

import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset


@napari_hook_implementation
def napari_get_writer():
    pass


@napari_hook_implementation
def napari_write_image(path: str, data: Any, meta: dict) -> Optional[str]:
   ext = os.path.splitext(path)[1]
   layer=napari.layers.Image(data, rgb=meta['rgb'], metadata=meta, scale=meta['scale'], translate=meta['translate'])  
   if not ext:
      pass  
  
   if ext=='.dcm':
      #ds= dicom_from_image_layer(layer) 
      #print(ds)
      #ds.save_as(path)
      #return path
      pass  
   if ext in ['.nii.gz','.nii','.gz']:
        image=image_from_image_layer(layer)
        itk.imwrite(image, path)
        return path
 
def image_from_image_layer(image_layer):
    """Convert a napari.layers.Image to an itk.Image."""
    if image_layer.rgb and image_layer.data.shape[-1] in (3, 4):
        if image_layer.data.shape[-1] == 3:
            PixelType = itk.RGBPixel[itk.UC]
        else:
            PixelType = itk.RGBAPixel[itk.UC]
        image = itk.image_view_from_array(image_layer.data, PixelType)

    else:
        image = itk.image_view_from_array(image_layer.data)

    if image_layer.metadata is not None:
        for k, v in image_layer.metadata.items():
            image[k] = v

    if image_layer.scale is not None:
        image["spacing"] = image_layer.scale.astype(np.float64)

    if image_layer.translate is not None:
        image["origin"] = image_layer.translate.astype(np.float64)

    return image    
    

def dicom_from_image_layer(image_layer):
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    filename_big_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"
    ds = FileDataset(filename_little_endian, {},
                 file_meta=file_meta, preamble=b"\0" * 128)
    
    ds.PatientName = "Test^Firstname"
    ds.PatientID = "123456"
    ds.PixelData = image_layer.data.tostring()
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
    ds.ContentTime = timeStr
    
    return ds
