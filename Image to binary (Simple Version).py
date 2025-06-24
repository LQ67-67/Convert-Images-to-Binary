from PIL import Image

def main( ):
    name= '1.jpg'

    img= Image.open (name);
    for pixel in iter(img.getdata()):
        print(pixel)

    img.convert("1").show();

if __name__=='__main__':
    main()