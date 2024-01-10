import pandas as pd import numpy as npimport torch from glob import globimport cv2from torch import nnimport torchvisionfrom torch.utils.data import Datasetfrom torchvision import transformsimport osdef mkdir(path):    try :        os.makedirs(path)    except:        pass    mkdir("./resnet_set/Train")  mkdir("./resnet_set/test")  TARGET_SIZE=(256,256)     train_data=glob("./data/Train/**/*.JPG")+glob("./data/Train/**/*.jpg")test_data=glob("./data/test/**/*.JPG")+glob("./data/test/**/*.jpg")     # train_data=glob("./data/Train/**/*.JPG")# test_data=glob("./data/test/**/*.JPG")train_dataset=pd.DataFrame(train_data,columns=["file_name"])train_dataset["label"]=train_dataset["file_name"].apply(lambda x : x.rsplit("/")[-2])train_dataset["name"]=train_dataset["file_name"].apply(lambda x : x.rsplit("/")[-1][:-4])test_dataset=pd.DataFrame(test_data,columns=["file_name"])test_dataset["label"]=test_dataset["file_name"].apply(lambda x : x.rsplit("/")[-2])test_dataset["name"]=test_dataset["file_name"].apply(lambda x : x.rsplit("/")[-1][:-4])train_dataset=train_dataset.sample(frac=1 , ignore_index=True)train_dataset=train_dataset.drop_duplicates(["label","name"],ignore_index=True)test_dataset=test_dataset.sample(frac=1 , ignore_index=True)test_dataset=test_dataset.drop_duplicates(["label","name"],ignore_index=True)class MyDataset(Dataset):    def __init__(self, df_data,transform=None):        super().__init__()        self.df = df_data        self.transform = transform    def __len__(self):        return len(self.df)            def __getitem__(self, index):        img_path,lbl,name = self.df[["file_name","label","name"]].iloc[index]        img = cv2.imread(img_path)        img = cv2.resize(img, TARGET_SIZE)        if self.transform:            img=self.transform(img)        img=torch.unsqueeze(img,0).float()        return img,lbl, name    trans = transforms.Compose([transforms.ToTensor()])   train_set=MyDataset(train_dataset,trans)test_set=MyDataset(test_dataset,trans)class costum_model(nn.Module):    def __init__(self):        super(costum_model,self).__init__()        self.resnet=torchvision.models.resnet34(pretrained=True)    def forward(self,x):        x=self.resnet(x)        return(x)     resnet_model=costum_model() for index in range(train_set.__len__()):     img,lbl,name=train_set.__getitem__(index)     img=resnet_model(img)     img=img.detach().numpy()     np.save(f"./resnet_set/Train/{lbl}_{name}.npy",img)     print(f"Train {index+1}/{train_set.__len__()} : Done!")                    for index in range(test_set.__len__()):     img,lbl,name=test_set.__getitem__(index)     img=resnet_model(img)     img=img.detach().numpy()     np.save(f"./resnet_set/test/{lbl}_{name}.npy",img)     print(f"test {index+1}/{test_set.__len__()} : Done!")