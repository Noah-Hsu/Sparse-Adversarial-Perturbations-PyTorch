from torch.utils.data import DataLoader

import dataset
from dataset import *

# Normalization parameters for pre-trained PyTorch models
mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('Device: ' + str(device))
test_dataset = Dataset(dataset_path="../../0Dataset/UCF101/UCF-101-frames",
                       split_path="../../0Dataset/UCF101/ucfTrainTestlist",
                       split_number=1,
                       input_shape=(3, 112, 112),
                       sequence_length=40,
                       training=False,
                       )
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True, num_workers=0)
for batch_index, (input_image, input_label) in enumerate(test_dataloader):
    input_image, input_label = input_image.to(device), input_label.to(device)
    to_pil = transforms.ToPILImage()
    for i in range(40):
        image = dataset.denormalize(input_image[0][i].cpu())
        pil_image = to_pil(image.byte())
        pil_image.show()
