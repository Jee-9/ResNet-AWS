import numpy as np
import torch
import torch.onnx

import onnxruntime

batch_size = 10
x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)

ort_session = onnxruntime.InferenceSession("new_final_resnet50.onnx")

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}
print("ort_inputs : ", ort_inputs)
# print("ort_inputs size : ", ort_inputs.shape)

ort_outputs = ort_session.run(None, ort_inputs)
print("ort_outputs :", ort_outputs)
print("perfect")