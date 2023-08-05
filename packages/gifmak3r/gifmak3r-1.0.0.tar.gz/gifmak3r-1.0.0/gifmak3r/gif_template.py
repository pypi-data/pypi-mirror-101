"""Classes used for management and storage of pre-defined
gif templates. Instances of these classes are to be
used in gif generation (inputted into generation
functions) and saved

Classes
-------
Gif
  An existing gif online
GifTemplate
  An existing gif online with methods for formatting
  that inherits from Gif
"""
from PIL import Image, ImageFont, ImageSequence
from io import BytesIO
from urllib.request import urlopen
from typing import List
from gifmak3r.generator import create_caption

class Gif:
  """Basic representation of an online gif

  Fields
  ------
  name : str
    a user-given title for an online gif
  frames : List[Image]
    a List of Image objects that represent the frames
    of the gif

  """
  def __init__(self, name: str, frames: List[Image.Image]) -> None:
    """Creates a Gif object

    Parameters
    ----------
    name : str
      a user-given title of the template
    frames : List[Image]
      a List of Image objects taht represent the frames of the gif

    Methods
    -------
    GifTemplate : GifTemplate
      creates a GifTemplate object
    open_image : Image
      returns an Image instance corresponding to the link field
    """
    self.name = name
    self.frames = frames

  def save_gif(self) -> BytesIO:
    """Saves a GIF to BytesIO"""
    gif_bytes = BytesIO()
    self.frames[0].save(
      gif_bytes,
      format='GIF',
      save_all=True,
      append_images=self.frames[1:]
    )
    return gif_bytes
  def save_gif_fs(self, file_name) -> None:
    """Saves a GIF to the filesystem

    Parameters
    ----------
    file_name : str
      the name the file should be set as
    """
    self.frames[0].save(
      file_name,
      format='GIF',
      save_all=True,
      append_images=self.frames[1:]
    )

class GifTemplate(Gif):
  """An existing gif online for use in formatting

  Fields
  ------
  link : str
    a user-given image url for an online gif

  Methods
  -------
  GifTemplate : GifTemplate
    creates a new GifTemplate object
  generate_white_bg_black_impact(caption, font_size) : Image
    returns an Image (gif) with the format mentioned in the method name
  """
  def __init__(self, name: str, link: str):
    self.link = link
    super().__init__(
      name,
      [frame for frame in ImageSequence.Iterator(self.open_image())]
    )

  def open_image(self) -> Image.Image:
    """Returns an Image instance corresponding to the link field

    Returns
    -------
    Image
      an Image grabbed from this object's link field
    """
    return Image.open(urlopen(self.link))

  def generate_white_bg_black_impact(
    self, name: str, caption : str, font_size=42
  ) -> Gif:
    """Returns a List of Images (GIF) with the white background, black impact
    font format

    Parameters
    ----------
    name : str
      title for gif
    caption : str
      text to put on a white background in Impact font
    font_size : str
      size of the Impact font to be rendered onto the GIF

    Returns
    -------
    List[Image]
      a list of frames with each frame having been molded
      into the desired format
    """
    frames = []
    for frame in ImageSequence.Iterator(self.open_image()):
      frame = create_caption(
        caption,
        ImageFont.truetype('fonts/impact.ttf', font_size),
        self.open_image()
      )
      frames.append(frame)

    return Gif(name, frames)
