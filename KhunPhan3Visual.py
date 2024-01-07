from PIL import Image, ImageDraw

# Formula to transform the enumerated position into matrix coordinates
def getIJ(n) :
    return ((n-1)//4 + 1, (n-1)%4 + 1)

size = 10
padding = size/2
margin = 30
boardlength = size*5 + margin
boardwidth = size*4 + margin
boardsPerRow = 15
piececolor = (191,153,114)
boardcolor = (101,56,24)
imagecolor = (144,96,53)

def drawSolution(solution, index) : 

    im = Image.new('RGB', ((boardsPerRow * boardwidth + 2*size), ((len(solution)+boardsPerRow-1)//boardsPerRow)*boardlength), (50,50,50))
    draw = ImageDraw.Draw(im)

    for i, step in enumerate(solution) :
        fieldULX = (i%boardsPerRow)*boardwidth + padding
        fieldULY = (i//boardsPerRow)*boardlength + padding
        draw.rectangle((fieldULX, fieldULY, fieldULX + 5*size, fieldULY + 6*size), fill=boardcolor)
        
        for type, typePos in enumerate(step) :
            for n in typePos :
                y,x = getIJ(n)
                upLeftX = fieldULX + (x-0.5)*size
                upLeftY = fieldULY + (y-0.5)*size
                match type :
                    case 0 :
                        lowRightX = upLeftX + size
                        lowRightY = upLeftY + size
                        color = (255,255,255)
                    case 1 :
                        lowRightX = upLeftX + size
                        lowRightY = upLeftY + 2*size
                        color = (255,0,0)
                    case 2 :
                        lowRightX = upLeftX + 2*size
                        lowRightY = upLeftY + size
                        color = (255,0,0)
                    case 3 :
                        lowRightX = upLeftX + 2*size
                        lowRightY = upLeftY + 2*size   
                        color = (255,184,28)

                draw.rectangle((upLeftX, upLeftY, lowRightX, lowRightY), fill=color, outline=(0, 0, 0))
                # draw.ellipse((upLeftX + padding, upLeftY + padding, lowRightX - padding, lowRightY - padding), fill=color, outline=(0, 0, 0))

        path = "images/solution" + str(index) + "_" + str(len(solution)) + ".jpg"
        im.save(path, quality=95)
