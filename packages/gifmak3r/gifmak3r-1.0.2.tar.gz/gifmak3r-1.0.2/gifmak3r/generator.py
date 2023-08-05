"""Entry point for generating gifs in "meme" format

Functions in the module are used in the process of
generating gifs in the format of white background
and black impact font given a pre-existing gif.

Functions are specific to gif creation, and must
be done in a specific order to get the desired
result.

Functions
---------
create_caption_background(lines, img) : Image
  Returns a new Image object with a white
  background with size corresponding to the amount of lines
get_text_wrap(text, font, max_width) : List[str]
  Returns a List of str, with the number of words per element
  being dependent on the rendered size of the font and the
  desired max width
create_caption(img):
  Returns a final Image with the caption
  Doesn't return an entire gif. If a gif is inputted, the
  function would only return the first frame of the gif.

"""
from PIL import Image, ImageDraw, ImageFont
from typing import List

def create_caption_background(
  lines: int, line_height: int, img: Image.Image
) -> Image.Image:
  """Returns a new Image object with a white
  background with size corresponding to the amount of lines

  Parameters
  ----------
  lines : int
    the number of lines to render on top of the white background
  line_height : int
    the maximum height that a line in a desired font would take
  img : Image
    the starting Image to format

  Returns
  -------
  Image
    a new Image with a white background on top
  """
  result = Image.new(
    'RGBA', (img.width, img.height + lines * line_height), (255, 255, 255)
  )
  result.paste(img, (0, lines * line_height + 20))
  return result

def get_text_wrap(
  text: str, font: ImageFont.FreeTypeFont, max_width: int
) -> List[str]:
  """Returns a List of str, with the number of words per element
  being dependent on the rendered size of the font and the
  desired max width

  Parameters
  ----------
  text : str
    a string of text to split up into lines
  font : FreeTypeFont
    a TrueType or OpenType font that determines words for each line
  max_width : int
    an int specifying the absolute max length, in pixels, that a line
    can take up

  Returns
  -------
  List[str]
    a List of strings separated by rendered size of the text
  """
  lines = []

  if font.getsize(text)[0] <= max_width:
    lines.append(text)
  else:
    words = text.split(' ')
    i = 0
    while i < len(words):
      line = ''
      while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
        line = line + words[i] + ' '
        i += 1
      if not line:
        line = words[i]
        i += 1

      lines.append(line)
    return lines

def create_caption(
  caption: str, font: ImageFont.FreeTypeFont, img: Image.Image
) -> Image.Image:
  """Returns a final Image with the caption
  Doesn't return an entire gif. If a gif is inputted, the
  function would only return the first frame of the gif.

  Parameters
  ----------
  caption : str
    text to use as caption on top of image
  img : Image
    the starting Image to format

  Returns
  -------
  Image
    a new Image with a completed caption on top
  """
  text_lines = get_text_wrap(caption, font, img.width * 0.8)

  img = create_caption_background(len(text_lines), font.getsize('hg')[1], img)

  canvas = ImageDraw.Draw(img)
  image_width = img.width
  margin = 10
  for line in text_lines:
    font_width = canvas.textsize(line, font=font)[0]
    canvas.text(((image_width-font_width) / 2, margin), line,
     font=font, fill=(0,0,0))
    margin += font.getsize('hg')[1]
  del canvas

  return img
