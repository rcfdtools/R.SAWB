import glob
from PIL import Image

def make_gif(frame_folder):
    frame_len = len(glob.glob(f'{frame_folder}/*.png'))
    print('Frames: %d' %frame_len)
    seconds_frame = 2
    duration = frame_len * seconds_frame * 60  # miliseconds

    frames = [Image.open(image) for image in glob.glob(f'{frame_folder}/*.png')]
    frame_one = frames[0]
    frame_one.save('my_awesome.gif', format='GIF', append_images=frames,
                   save_all=True, duration=duration, loop=0)


if __name__ == '__main__':
    make_gif('../../.ppoi/1/spi/era5')


# References
# https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/