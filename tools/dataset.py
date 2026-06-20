from glob import glob
from pathlib import Path
import shutil
import random

def add_source(source, target, mapping, max_labels=None):
    for dir in ["train", "valid"]:
        source_dir = Path(source) / dir
        target_dir = Path(target) / dir
        target_dir.mkdir(exist_ok=True)

        Path(target_dir / "labels").mkdir(exist_ok=True)
        Path(target_dir / "images").mkdir(exist_ok=True)

        paths = [Path(x) for x in glob(str(source_dir / "images" / "*"))]
        random.shuffle(paths)

        label_count = 0
        
        for path in paths:
            if(max_labels != None and label_count > max_labels): break
            label_name = f"{path.stem}.txt"
            f = open(source_dir / "labels" / label_name, "r")
            labels = [x.strip().split(" ") for x in f.readlines()]
            f.close()

            f = open(target_dir / "labels" / label_name, "w")
            for label in labels:
                id = int(label[0])
                if(id in mapping):
                    label[0] = str(mapping[id])
                    f.write(" ".join(label) + "\n")
                    label_count += 1
            f.close()

            shutil.copy(path, target_dir / "images" / path.name)

add_source("datasets/deer", "datasets/main", {
    0: 0, # antlerless
    2: 0, # buck
    4: 1, # human
    5: 2  # raccoon
})

add_source("datasets/people", "datasets/main", {
    0: 1
}, max_labels=200)