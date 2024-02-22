# pip install -q transformers
import torch
import os
from torch import nn
from PIL import Image
from transformers import AutoTokenizer, AutoModelForCausalLM
from torchvision import transforms
from ViT_Classifier import VisionTransformer
from functools import partial
from openai import OpenAI
from datasetClass import TD_dataset
from training import start_training

if __name__ == '__main__':
    device = 'cpu'
    im_size = 256
    dataset_path = "onepiece_dataset/"

    dataset = TD_dataset(im_size=im_size, dataset_path=dataset_path)
    dataloader = torch.utils.data.DataLoader(dataset,batch_size=64,shuffle=True)
    num_classes = dataset.getNumClasses()

    ViT_Classifier = VisionTransformer(
        img_size=im_size, patch_size=16, embed_dim=512, depth=6, num_heads=8, num_classes=num_classes,
        mlp_ratio=4, qkv_bias=True,
        norm_layer=partial(nn.LayerNorm, eps=1e-6))  # embed_dim / num_heads should be integer

    lr = 0.005
    epochs = 10
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(ViT_Classifier.parameters(), lr=lr, weight_decay=0.001)

    start_training(epochs, dataloader, ViT_Classifier, loss_function, optimizer, device)



    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Please write verilog code that describes an AND gate module."},
        ]
    )

    #print(completion.choices[0].message.content)
