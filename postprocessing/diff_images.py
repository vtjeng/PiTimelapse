#!/usr/bin/env python3

import glob
import os
from enum import Enum
from typing import List

import click
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tqdm


def calculate_diffs(file_list: List[str]) -> List[float]:
    # calculates the differences between successive images

    this_image = cv2.imread(file_list[0], cv2.IMREAD_COLOR)
    height, width = this_image.shape[:2]
    diffs = []
    for path in tqdm.tqdm(file_list[1:]):
        next_image = cv2.imread(path, cv2.IMREAD_COLOR)
        try:
            diffs.append(cv2.norm(this_image, next_image) / (height * width))
        except cv2.error as e:
            # https://stackoverflow.com/a/792163/1404966
            raise ValueError(f"Could not compute norm with image {path}") from e
        this_image = next_image
    return diffs


def exponential_moving_average(values: List[float], window: int = 20) -> np.array:
    weights = np.exp(np.linspace(-1.0, 0.0, window))
    weights /= weights.sum()

    # here, we will just allow the default since it is an EMA
    a = np.convolve(values, weights)[: len(values)]
    a[:window] = a[window]
    return a


def moving_average(values: List[float], window: int = 20) -> np.array:
    weights = np.repeat(1.0, window) / window
    # specifying "valid" to convolve requires that there are enough data points.
    return np.convolve(values, weights, "valid")


SmoothingOption = Enum("SmoothingOption", "NO MA EMA")


def smooth_values(values: List[float], smoothing_option: SmoothingOption) -> np.array:
    if smoothing_option == SmoothingOption.NO:
        return np.array(values)
    if smoothing_option == SmoothingOption.MA:
        return moving_average(values)
    if smoothing_option == SmoothingOption.EMA:
        return exponential_moving_average(values)


@click.command(
    help="Computes the differences between consecutive images in a directory."
)
@click.option(
    "-i",
    "--image-directory",
    required=True,
    type=click.Path(exists=True),
    help="Directory where images are stored. Expected to be .jpg files, and will be processed in lexicographic order.",
)
@click.option(
    "-d",
    "--diff-file",
    type=click.File("w"),
    help=".csv file to store diffs. If not specified, diffs will not be stored.",
)
@click.option(
    "-p", "--show-plot", is_flag=True, default=False, help="Show diffs as plot."
)
@click.option(
    "-s",
    "--smoothing-option",
    type=click.Choice(
        list(map(lambda x: x.name, SmoothingOption)), case_sensitive=False
    ),
    default=SmoothingOption.NO.name,
    help="Smoothing options for values shown on plot.",
)
def main(
    image_directory: str,
    diff_file: click.utils.LazyFile,
    show_plot: bool,
    smoothing_option: str,
):
    print("Computing diffs...")
    file_list = glob.glob(os.path.join(image_directory, "*.jpg"))
    diffs = calculate_diffs(file_list)
    if diff_file is not None:
        print(f"Writing diffs to {diff_file.name}")
        for diff in diffs:
            diff_file.write(f"{diff}\n")
    else:
        print(f"Diffs are {np.array(diffs)}")
    if show_plot:
        smoothed_diffs = smooth_values(diffs, SmoothingOption[smoothing_option])
        plt.plot(diffs)
        plt.plot(smoothed_diffs)
        plt.show()


if __name__ == "__main__":
    main()
