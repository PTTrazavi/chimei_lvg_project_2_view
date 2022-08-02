# Chimei LVG EF and RWMA project
## BiSeNetV2 model檔更新
跑05_BiSeNetV2-segmentation_tf2.3_transpose.ipynb時，把model改為transpose conv等修改:  
option 1. git clone後，可直接在colab內照註解修改model.py檔  
option 2. git clone後，把gitlab 的 colab_code/BiSeNetV2_model_update/model.py 檔案覆蓋上去 
## colab_code folder  
The code in this folder works on google colab.  
00_confusion matrix calculation.ipynb: 輔助計算cm, sesitivity, speicificity等metrics的工具  
01_U-Net_segmentation.ipynb: 訓練切割心臟部分的UNet模型  
01_U-Net_segmentation_transpose.ipynb: 訓練切割心臟部分的UNet模型 不使用upsampling 用transpose conv  
02_classification_3c_lateral_tf1_+EV.ipynb: 訓練RWMA lateral view 模型  
03_classification_4c_AP_tf1_+EV.ipynb 訓練RWMA AP view 模型  
04_inference.ipynb: 結合前三個訓練好的模型，做inference的流程(用.h5檔)  
04_inference_TensorFlow_SavedModel.ipynb: 結合前三個訓練好的模型，做inference的流程(用TensorFlow SavedModel檔)  
05_BiSeNetV2-segmentation.ipynb: 訓練切割心臟部分的BiSeNetV2模型(和UNet比較用)  
05_BiSeNetV2-segmentation_tf2.3.ipynb:訓練切割心臟部分的BiSeNetV2模型(和UNet比較用) 用tensorflow 2.3.2版本訓練  
05_BiSeNetV2-segmentation_tf2.3_transpose.ipynb:訓練切割心臟部分的BiSeNetV2模型(和UNet比較用) 用tensorflow 2.3.2版本訓練 並且修改model  
06_inference_BiSeNetV2.ipynb: 結合三個訓練好的模型，做inference的流程(用.h5檔)  
06_inference_BiSeNetV2_TensorFlow_SavedModel.ipynb: 結合三個訓練好的模型，做inference的流程(用TensorFlow SavedModel檔)  
convert_BiSeNetV2_h5_to_TensorFlow_SavedModel.ipynb: 把BiSeNetV2 h5檔轉換為TensorFlow SavedModel  
convert_h5_to_TensorFlow_SavedModel.ipynb: 把h5檔轉換為TensorFlow SavedModel  
## checkpoints folder  
UNet folder: UNet模型檔，包含h5和TensorFlow SavedModel格式  
BiSeNetV2 folder: BiSeNetV2模型檔，包含h5和TensorFlow SavedModel格式  
classification folder: RWMA的分類模型檔，包含h5和TensorFlow SavedModel格式  
## 202111_chimei_2_view  
image preprocess code for segmentation model  
## 202112_chimei_classification_2_view  
image preprocess code for classification model  
## dataset source  
奇美醫院上傳原始影片檔: dl03:/mnt/data/chrisjan/upload/chimei  
影片檔切割出的圖片檔集: dl01:/mnt/data/jeremy/chimei  
## note  
jupyter notebook內，預先上傳到Azure供下載的檔案，路徑皆為 https://djangocolab3.blob.core.windows.net/aidatacolab2/......  
若發現不能下載，把路徑更新就好，舊的版本為 https://djangocolab.blob.core.windows.net/aidatacolab2/......(前面漏掉3)  
