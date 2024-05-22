import subprocess



        
def dependencies():
    dependencies = ['pygame', 'cv2', 'ffmpeg-python','import argparse','os']
    for package in dependencies:
        try:
            subprocess.check_call(['pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")

import argparse
import pygame
import cv2
import os
import ffmpeg


## VARIABLE INIT#######################################################################################################################

class AsciiArt:
    ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    def __init__(self,file_path=None,font_size=12)->None:
        print("use '--init' to install all dependecies")
        
        if os.path.exists("./temp"):
            "/home/prince/Videos/birds.mov"
            pass
        else:
            os.mkdir("temp")
            
        self.file_path = file_path
        self.font_size = font_size
        
        if self.file_path==0:
            self.is_video=True
            self.vid = cv2.VideoCapture(self.file_path)
        else:            
            _, extension = os.path.splitext(self.file_path)
            if extension.lower() in (".jpg",".jpeg",".png",".tif"):
                self.is_video=False
            else:
                self.is_video=True
                self.compress()
                self.file_path="./temp/temp.mp4"
                self.vid = cv2.VideoCapture(self.file_path)
            
        pygame.init()
        self.screen = pygame.display.set_mode([1920,1080])
        self.font=pygame.font.SysFont('monospace',size=self.font_size)

    def compress(self):
        input_video = ffmpeg.input(self.file_path)
        output_video = ffmpeg.output(input_video, "./temp/temp.mp4", vf='scale=426:240', r=24)
        ffmpeg.run(output_video)
    
    def clear(self):
        try:
            os.remove("./temp/temp.mp4")
        except:
            print("WebCam Mode")
        
    def process(self,img,grayscale):
        """Process the image by enhancing sharpness and contrast, then apply Gaussian blur."""

        # img = ImageEnhance.Contrast(img).enhance(1.0)
        img =cv2.resize(img, (140,80))
        img =cv2.convertScaleAbs(img , alpha=1.5, beta=-30)

        num_colors = 25 # Adjust the number of colors as needed
        img = img // (256 // num_colors) * (256 // num_colors)
        
        return img


    def render(self, img, grayscale=False):
        height, width, _ = img.shape  # Get image dimensions
        lumen=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        for y in range(height):
            for x in range(width):
                char = self.ASCII_CHARS[int(lumen[y][x]/255 *69)]
                color = tuple(img[y, x]) if not grayscale else (255, 255, 255)  # Use pixel color or white for grayscale rendering
                text = self.font.render(char, True, color)
                self.screen.blit(text, (x * self.font_size + 8, y * self.font_size + 10))

 
    def run(self,grayscale):
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.clear()
                    pygame.quit()
                    exit(0)
                    
            self.screen.fill((0,0,0)) 
             
            if self.is_video:
                ret, frame = self.vid.read()
                
                if not ret:
                    break
                frame=self.process((cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)),grayscale=grayscale)
                cv2.imshow("lele",frame)
                cv2.waitKey(1)
                cv2.destroyAllWindows()
            else:
                frame = self.process(cv2.imread(self.file_path),grayscale=grayscale)
            self.render(frame,grayscale)
            
            pygame.display.update()



def main()->None:
    
    parser = argparse.ArgumentParser(description='Ascii Art')

    parser.add_argument('file_path', metavar='FILE', type=str, nargs='?',
                        help='path to the input image file')
    parser.add_argument('--GRAY', dest='grayscale', action='store_true',default=0,
                        help='Grayscale mode')
    parser.add_argument('--font-size', type=int, default=12,
                        help='font size for text overlay (default: 12)')
    parser.add_argument('--init', dest='init', action='store_true',default=0,
                        help='Install all  dependencies ')
    args = parser.parse_args()
    
    if args.init:
         dependencies()

    file_path= args.file_path if args.file_path!=None else 0


    obj=AsciiArt(file_path,font_size=args.font_size)
    obj.run(grayscale=args.grayscale)

if __name__=="__main__":
    main()
