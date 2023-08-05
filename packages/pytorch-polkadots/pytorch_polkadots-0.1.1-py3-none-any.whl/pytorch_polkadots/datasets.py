from random import randint, choice
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from torch import Tensor
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor, transforms


class MakeImages:
    def __init__(self,
                 min_width: int = 1024, min_height: int = 768,
                 max_width: int = 1024, max_height: int = 768,
                 seed: int = None):

        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        if seed is not None:
            from random import seed
            seed(seed)

    def draw_color(self):
        colors = ("red", "blue", "green", "yellow", "orange")
        c = choice(colors)
        return c

    def new_image(self, num_dots: int, class_index: int, dot_size: int = 16) -> Image:
        width = randint(self.min_width, self.max_width)
        height = randint(self.min_height, self.max_height)
        # get an image

        # make a blank image for the text, initialized to transparent text color
        image = Image.new("RGB", (width, height), (55, 55, 55))
        draw = ImageDraw.Draw(image)
        for _ in range(num_dots):
            color = self.draw_color()

            xy = self.draw_bounding_box(width, height, size=dot_size)
            draw.pieslice(xy, 0, 360, fill=color, width=10)
        if class_index:
            # get a font
            fnt = ImageFont.truetype('Arial Unicode', size=40)
            xy = self.draw_bounding_box(width // 4 * 3, height // 4 * 3, size=dot_size)
            draw.text(xy[0:2], text=f"{class_index}", font=fnt, color="black")
        return image

    def draw_bounding_box(self, width, height, size):
        x = randint(0, width)
        y = randint(0, height)
        return (x, y, x + size, y + size)


class PolkaDotDataset(Dataset):

    def __init__(self, num_classes: int,
                 length: int,
                 max_dots: int = 32,
                 min_width: int = 1024, min_height: int = 768,
                 max_width: int = 1024, max_height: int = 768,
                 ):
        self.num_classes = num_classes
        self.image_maker = MakeImages(
            min_width=min_width, max_width=max_width,
            min_height=min_height, max_height=max_height)
        self.max_dots = max_dots
        self.to_tensor = ToTensor()
        self.item_to_class_index = {}
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                              std=[0.229, 0.224, 0.225])
        self.length = length

    def __getitem__(self, item) -> Tuple[Tensor, int]:
        # draw a random class index for each image, memorize the class index,
        if item in self.item_to_class_index:
            class_index = self.item_to_class_index[item]
        else:
            class_index = randint(0, self.num_classes - 1)
            self.item_to_class_index[item] = class_index
        # Generate the polkadot image:
        num_dots = randint(0, self.max_dots)
        image = self.image_maker.new_image(num_dots=num_dots, class_index=class_index)
        return self.normalize(self.to_tensor(image)), class_index

    def __len__(self):
        return self.length
