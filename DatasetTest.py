from torch.utils.data import DataLoader

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
    input_image = input_image[0]  # 取出批次中的第一个样本
    # input_image = input_image.to(torch.float32)  # 将数据类型转换为浮点型
    to_pil = transforms.ToPILImage()
    # 执行逆归一化操作
    for i in range(40):  # 遍历每个图像序列中的每一帧
        for j in range(3):  # 遍历每个通道
            input_image[i, j] = (input_image[i, j] * std[j]) + mean[j]

    # 将张量转换为 PIL 图像并显示
    for i in range(40):  # 遍历每个图像序列中的每一帧
        pil_image = to_pil(input_image[i])  # 转换为字节张量并转换为 PIL 图像
        pil_image.show()  # 显示图像
