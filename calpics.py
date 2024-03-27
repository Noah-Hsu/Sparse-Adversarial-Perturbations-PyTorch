from PIL import Image
import torch
from torchvision.transforms import transforms
import os

b_dir = "pic/before/0"
a_dir = "pic/after/0"
before = os.listdir(b_dir)
after = os.listdir(a_dir)


def savedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


transform = transforms.ToTensor()
to_pil = transforms.ToPILImage()
mag = 50
for i in range(len(before)):
    image1 = Image.open(f"{b_dir}/{i}.jpg")
    image_tensor1 = transform(image1).unsqueeze(0)  # 添加一个批次维度
    for batch in range(100):
        image2 = Image.open(f"{a_dir}/{batch}/{i}.jpg")
        image_tensor2 = transform(image2).unsqueeze(0)  # 添加一个批次维度
        diff = image_tensor1 - image_tensor2
        posi = torch.clamp(diff, min=0)[0] * mag
        nege = torch.clamp(diff, max=0).abs()[0] * mag
        savedir(f"pic/diff/0/{batch}")
        to_pil(posi).save(f"pic/diff/0/{batch}/posi_{i}.jpg")
        savedir(f"pic/diff/0/{batch}")
        to_pil(nege).save(f"pic/diff/0/{batch}/nege_{i}.jpg")
    print(str(i + 1) + "/40")
