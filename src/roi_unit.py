class roi:
    def __init__(self, line, conf):
        information = line.rstrip().split('_')
        self.initStartX = int(information[0])
        self.initStartY = int(information[1])
        self.initEndX = self.initStartX + int(information[2])
        self.initEndY = self.initStartY + int(information[3])

        self.startX = int(int(information[0]) * conf['width_ratio'])
        self.startY = int(int(information[1]) * conf['height_ratio'])
        self.width = int(int(information[2]) * conf['width_ratio'])
        self.height = int(int(information[3]) * conf['height_ratio'])
        self.endX = self.startX + self.width
        self.endY = self.startY + self.height
        self.side = str(information[4])
        self.element = str(information[5])
        self.number = str(information[6])

    def getArea(self):
        return (self.initStartX, self.initStartY), (self.initEndX, self.initEndY)

def readROI(path, conf) :
    print('# Get ROI Information:', path)
    file = open(path, "r+")
    index = 0
    info = {}
    info['all'] = []
    for line in file:
        print(line)
        temp = roi(line, conf)
        if temp.side not in info : info[temp.side] = []
        info[temp.side].append(temp)
        info['all'].append(temp)
        index +=1

    return info