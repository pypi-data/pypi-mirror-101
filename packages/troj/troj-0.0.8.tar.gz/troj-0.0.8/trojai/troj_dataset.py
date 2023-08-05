import pandas as pd
import json
import numpy as np
import os
import cv2
import torch


class TrojDataLoader:
    def __init__(
        self,
        dataframe,
        data_structure,
        root_folder,
        transforms=None,
        channel_first=True,
    ):
        self.dataframe = dataframe
        self.transforms = transforms
        self.data_structure = data_structure
        self.root_folder = root_folder
        self.index_list = self.dataframe.index.tolist()
        self.channel_first = channel_first

    def __len__(self):
        return len(set(self.dataframe["file_name"]))

    def __getitem__(self, index):
        # print(self.dataframe.loc[index]["file_name"].compute())
        index = self.index_list[index]
        example_row = self.dataframe.loc[index]
        file_name = example_row["file_name"]
        annotation = example_row["label"]
        if "imagenet" == self.data_structure:
            class_folder = example_row["class_name"]
            stage_folder = example_row["stage"]
            relative_path = self.root_folder + stage_folder + "/" + class_folder + "/" + file_name
        elif "coco" == self.data_structure:
            relative_path = self.root_folder + file_name

        # need to add the stage to path along with the class
        # return dask_image.imread.imread(relative_path)
        img = cv2.imread(relative_path)
        if self.transforms != None:
            img = self.transforms(img)
        if self.channel_first is True:
            img = np.moveaxis(img, -1, 0)

        
        return img, annotation, index


class TrojDataset:
    def __init__(self):
        """
        We initialize the dataframe as None so that if the client does not wish to use our methods they can
        create their own dataframe and pass it to this class. We just specify that the dataframe
        must have the expected basic columns for our methods to function properly.
        """
        self.dataframe = None
        # saves the main folder to look in to recreate the relative links to the images for loading
        self.root_folder = None
        # saves whether or not the data is in coco format or imagenet folders
        self.data_structure = None

    def CreateDF(self, folder_path, annotations_file_path=None, partitions_count=1):
        # TODO method for building dataframes
        """
        This method should take in the folder containing all the datapoints in the imagenet style folder structure
        if the class is classification, or it can take in the coco format folder+annotation structure.

        It should create a dataframe using dask, with the possibility for choosing the number of partitions of the dataframe
        (probably going to want to use **kwargs to take arguments for dask functions). Should construct a dataframe with
        columns (index, file_location, split, label, *metadata) for classification where split is whether the image
        associated to the file is either train, test, val, or unlabeled (assume the input folders have this structure).
        Assume metadata is given as a list containing dictionaries all with the same keys, with one dictionary
         for each image. The keys form columns and the metadata for each image is stored in those columns.

        If they pass an annotations file, we construct a dataframe with columns
        (index, file_location, split, bounding boxes, bounding box labels, metadata) where for each image,
        we save in the dataframe a list containing lists with the four bounding box coordinates for each box.
        the bounding box labels contain a list of the labels for the bounding boxes associated to the image.


        :return: should just do something like self.dataframe = new_dataframe
        """

        if annotations_file_path is None:
            try:
                # if no annotations are included, the annotation information is embedded in the folder structure
                # load it in to dataframe
                accumulator = 0
                out_dict = dict()
                class_list = list()
                for root, d_names, f_names in sorted(os.walk(os.path.normpath(folder_path))):
                    if f_names != []:
                        # replace the double slash with forward slash for consistency
                        # root = os.path.join(root).replace("\\", "/")
                        # split out each part of the root
                        root = os.path.realpath(root)
                        class_name = root.split(os.path.sep)[-1]
                        stage = root.split(os.path.sep)[-2]
                        base = root.split(os.path.sep)[-3]
                        if class_name not in class_list:
                            class_list.append(class_name)
                        for i, f_name in enumerate(f_names):
                            i = i + accumulator
                            out_dict[i] = {
                                "stage": stage,
                                "class_name": class_name,
                                "file_name": f_name,
                                "label": class_list.index(class_name),
                            }
                        # the accumulator tracks the index of the dictionary across folder loops
                        accumulator = i + 1
                df = pd.DataFrame(out_dict).transpose()
                # df = dd.from_pandas(pdf, npartitions=partitions_count)
                self.data_structure = "imagenet"
            except Exception as ex:
                print(ex)
                print("Creating dataframe from imagefolders failed!")
        else:
            """
            partitions are automatically applied through the read functions with dask
            determine the file type of the annotation file
            if annotations are included as json, load the images from the json
            """
            if "json" in annotations_file_path:
                try:
                    """
                    have to reorient the dataframe, right now it's one row with each key as a column with the entire array below
                    solved the orientation problem by stealing a script online that transforms coco style annos to a csv
                    loaded the csv from there
                    """
                    convert_coco_json_to_csv(annotations_file_path)
                    df = pd.read_csv(annotations_file_path[:-5] + ".csv")
                    self.data_structure = "coco"

                except:
                    print("Loading JSON failed!")
            elif "csv" in annotations_file_path:
                try:
                    df = pd.read_csv(annotations_file_path)
                except:
                    print("Loading CSV failed!")

        self.dataframe = df
        self.root_folder = folder_path

    # def LoadDF(self, file_loc, **kwargs):
    #     '''
    #     :param file_loc: Location of the file
    #     :param kwargs: arguments for the read_table function
    #     :return:
    #     uses dask.dataframes.read_table to read generic delimited tables. file_loc can be a globstring
    #     if data is distributed over multiple tables.
    #     '''
    #     df = dd.read_table(file_loc, **kwargs)
    #     self.dataframe = df

    def SaveDF(self, path, **kwargs):
        """

        :param path: the save path. This can be a globstring.
        :param kwargs: args for to_csv
        :return:
        """
        self.dataframe.to_csv(path, **kwargs)


def convert_coco_json_to_csv(filename):
    # COCO2017/annotations/instances_val2017.json
    s = json.load(open(filename, "r"))
    out_file = filename[:-5] + ".csv"
    out = open(out_file, "w")
    out.write("id,annotation_id,x1,y1,x2,y2,label,class_name,file_name\n")

    all_category_ids = []
    all_category_strings = []
    for category in s["categories"]:
        all_category_ids.append(category["id"])
        all_category_strings.append(category["name"])

    all_ids = []
    all_filenames = []
    for im in s["images"]:
        all_ids.append(im["id"])
        all_filenames.append(im["file_name"])

    all_ids_ann = []
    accumulator = 0
    for ann in s["annotations"]:
        image_id = ann["image_id"]
        all_ids_ann.append(image_id)
        x1 = ann["bbox"][0]
        x2 = ann["bbox"][0] + ann["bbox"][2]
        y1 = ann["bbox"][1]
        y2 = ann["bbox"][1] + ann["bbox"][3]
        label = ann["category_id"]
        class_name = all_category_strings[label - 1]
        file_name = all_filenames[image_id - 1]
        out.write(
            "{},{},{},{},{},{},{},{},{}\n".format(
                accumulator, image_id, x1, y1, x2, y2, label, class_name, file_name
            )
        )
        accumulator = accumulator + 1

    all_ids = set(all_ids)
    all_ids_ann = set(all_ids_ann)
    no_annotations = list(all_ids - all_ids_ann)
    # Output images without any annotations
    for image_id in no_annotations:
        out.write(
            "{},{},{},{},{},{},{},{},{}\n".format(
                accumulator, image_id, -1, -1, -1, -1, -1, -1, -1
            )
        )
    out.close()

    # Sort file by image id
    s1 = pd.read_csv(out_file)
    s1.sort_values("id", inplace=True)
    s1.to_csv(out_file, index=False)



def collate_wrapper(batch):
    transposed_data = list(zip(*batch))
    inp = np.ascontiguousarray(np.stack(transposed_data[0], 0).astype(np.float32))
    tgt = np.stack(transposed_data[1], 0).astype(np.int64)
    idx = np.stack(transposed_data[2], 0)
    return (inp, tgt, idx)

def BuildBatchIterator(dataloader, batch_size, shuffle=True):
    #TODO add other arguments for Pytorch dataloader if desired
    loader =  torch.utils.data.DataLoader(dataloader,
                                           batch_size=batch_size,
                                           shuffle=shuffle, collate_fn=collate_wrapper)
    return loader