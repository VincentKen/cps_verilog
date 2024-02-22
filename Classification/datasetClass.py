import glob
import torch
import cv2
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as tf
import matplotlib.pyplot as plt
from training import calculate_mean_std

class TD_dataset(Dataset):
    def __init__(self, im_size: int, dataset_path: str, transform=None):
        self.folderpath = dataset_path
        file_list = glob.glob(self.folderpath + "*")
        print(file_list)
        self.img_size = (im_size, im_size)
        self.data = []
        self.images = []
        self.classnames = []
        self.transform = transform

        for class_path in file_list:
            class_name = class_path.split("\\")[-1]
            self.classnames.append(class_name)
            for img_path in (glob.glob(class_path + "/*.jpg") + glob.glob(class_path + "/*.png")):
                img = cv2.resize(cv2.imread(img_path), self.img_size)
                self.data.append([img, class_name])
                self.images.append(img)
        mean, std = calculate_mean_std(self.images)
        self.normalize = tf.Normalize(mean, std)
        print(self.classnames)
    def __len__(self):
        return (len(self.data))

    def __getitem__(self, id):
        img, class_name = self.data[id]
        img = img[..., ::-1]/255
        img_tensor = torch.from_numpy(img.copy())
        img_tensor = img_tensor.permute(2,1,0)
        img_tensor = self.normalize(img_tensor)
        label = self.classnames.index(class_name)
        return img_tensor.float(), label

    def getNumClasses(self):
        return len(self.classnames)

    def getClassNames(self):
        return self.classnames

if __name__ == '__main__':
    im_size = 256
    dataset = TD_dataset(im_size= im_size, transform=None)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    fig = plt.figure()
    num_classes = dataset.getNumClasses()

    for i, data in enumerate(dataset):
        sample = data[0]
        print(i, sample.shape)
        sample = sample.permute(2, 1, 0) * 255
        sample = sample.int()
        ax = plt.subplot(1, 4, i + 1)
        plt.tight_layout()
        ax.set_title('Sample #{}'.format(i))
        ax.axis('off')
        plt.imshow(sample, cmap="gray")
        if i == 3:
            plt.show()
            break
    print(data_loader)
