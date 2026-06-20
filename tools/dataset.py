from glob import glob
from pathlib import Path
import shutil

source = Path("into-the-vale")
target = Path("dataset")

mapping = {
    0: 0,
    2: 1,
    4: 2,
    5: 3
}

dirs = ["train", "valid"]

for dir in dirs:
    source_dir = source / dir
    target_dir = target / dir
    target_dir.mkdir(exist_ok=True)

    target_image_dir = target_dir / "images"
    target_image_dir.mkdir(exist_ok=True)
    for image_path in glob(str(source_dir / "images" / "*")):
        image_path = Path(image_path)
        shutil.copy(image_path, target_dir / "images")
    
    target_label_dir = target_dir / "labels"
    target_label_dir.mkdir(exist_ok=True)
    for label_path in glob(str(source_dir / "labels" / "*")):
        label_path = Path(label_path)
        f = open(label_path, "r")
        labels = f.readlines()
        f.close()

        new_labels = []

        f = open(target_label_dir / label_path.name, "w")
        for label in labels:
            label = label.split(" ")
            if(int(label[0]) in mapping):
                label[0] = str(mapping[int(label[0])])
                label = " ".join(label).strip("\n")
                f.write(label + "\n")
        f.close()
