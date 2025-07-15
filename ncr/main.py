import simpleimageio as sio
import json

# ------------------------------------------
# For development / testing only: add parent directory to python path so we can load the package without installing it
# DO NOT use this if you have installed figuregen via pip
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# -------------------------------------------

import figuregen
from figuregen.util.templates import CropComparison
from figuregen.util.image import Cropbox


def gen_figure(scene_names, methods, reference_name="pt.exr", crop_name="crops.json"):
    """
    Generates a figure for the given scenes and methods.
    Args:
        scene_names (list[str]): Name of the scene.
        methods (dict): Dictionary mapping method names to their image filenames.
        reference_name (str): Filename of the reference image.
    """

    rows = []

    for i, scene_name in enumerate(scene_names):
        print(f"Generating figure for scene: {scene_name}")
        crops = json.load(open(os.path.join("images", scene_name, crop_name), 'r'))
        c = crops["closeups"]
        sq = crops["square_offset"]

        figure = CropComparison(
            reference_image=sio.read(os.path.join("images", scene_name, reference_name)),
            method_images=[
                sio.read(os.path.join("images", scene_name, methods[m])) for m in methods.keys()
            ],
            crops=[
                Cropbox(
                    top=c[0]['top'], left=c[0]['left'],
                    height=c[0]['height'], width=c[0]['width'],
                    scale=c[0]['scale'], color=[255, 110, 0]
                ),
                Cropbox(
                    top=c[1]['top'], left=c[1]['left'],
                    height=c[1]['height'], width=c[1]['width'],
                    scale=c[1]['scale'], color=[0, 200, 100]
                )
            ],
            square_offset=sq,
            hide_title=(i != 0),  # Hide title for all but the first row
            scene_name=scene_name,
            method_names=["Reference"] + list(methods.keys()),
            metric_name="MAPE",
        )

        rows.append(figure.figure_row)

    figuregen.figure(rows, width_cm=17.7, filename=os.path.join("figures", "figure" + ".pdf"))

    print(f"Figure generated and saved to 'figures/figure.pdf'.")


if __name__ == "__main__":
    scenes = [
        "bathroom",
        "cornell-box",
        "kitchen",
        "living-room",
        "veach-ajar",
    ]
    methods = {
        "Ours": "ncr.exr",
        "NR": "nr.exr",
        "Oidn (4spp)": "oidn.exr",
        "PT (16spp)": "pt16.exr",
    }
    reference = "pt.exr"
    crops = "crops.json"

    gen_figure(scenes, methods, reference, crops)
