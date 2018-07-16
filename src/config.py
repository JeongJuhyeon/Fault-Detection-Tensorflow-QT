import os

'''
<카메라 설정>
CAMERA_NUMBER : 현재 연결된 카메라 개수
AUTO_FOCUS : 카메라가 자동초점 모드로 연결되어 있다면 True, 수동초점 모드로 연결되어 있다면 False
TESTWINDOW_SIZE : 영역 선택 화면의 크기 WIDTH, HEIGHT는 가로 및 세로 픽셀 수(WINDOW_SIZE의 절반 혹은 1/4 권장)
WINDOW_SIZE : 실제 카메라 캡쳐화면의 크기
* IPEVO ZIGGI 같은 경우는 (3264 X 2448) 이 최대 해상도 입니다.
'''

CAMERA_NUMBER = 1
AUTO_FOCUS = False
TESTWINDOW_SIZE = {'width' : 700, 'height' : 700}
WINDOW_SIZE = {'width' : 700, 'height' : 700}
WINDOW_RATIO = {
    'width_ratio' : WINDOW_SIZE['width'] / TESTWINDOW_SIZE['width'],
    'height_ratio' : WINDOW_SIZE['height'] / TESTWINDOW_SIZE['height']
}

'''
<학습 설정>
IMAGE_SIZE : 학습에 사용되는 이미지 가로 및 세로 픽셀수, 512 이상 권장
ITERATION : 학습 시 반복 횟수, 30000 이상 권장
NUM_CHANNEL : 추후 수정
'''
# 30% of the data will automatically be used for validation
VALIDATION_SIZE = 0.3
DROPOUT = 0.3
IMAGE_SIZE = 128
ITERATION = 25
BATCH_SIZE = 16
NUM_CHANNEL = 3

'''
<이미지 잡음 설정>
NOISE_TRAIN : 트레이닝 이미지의 잡음 최저-최고 값
NOISE_TEST : 테스트 이미지의 잡음 최저-최고 값
값은 0~ 200사이가 적당합니다.

실제 작업 환경의 빛에 따라 최저-최고값을 조절해주는 것이 좋습니다.
MIN 값이 작을 수록 잡음이 커져 세세한 윤곽까지 표시하게 됩니다.
트레이닝에는 어느정도 세세한 윤곽을 많이 잡아주어 특징점을 어느정도 가질 수 있도록 하는 것이 좋습니다.
테스트 환경에서는 나사의 윤곽특징을 확인할 수 있을 정도로만 MIN 값을 올려주는 것이 좋습니다.
이미지는 아래 폴더에서 확인하실 수 있습니다.
트레이닝 : RES/ 디바이스 이름 / T_IMAGES
테스팅  : RES/ 디바이스 이름 / PREDICT / IMAGESCANNY
'''

NOISE_TRAIN={'min' : 40, 'max' : 200}
NOISE_TEST ={'min' : 150,'max' : 200}

GREEN = (0,255,0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)

def makeDir(path):
    # This part is make dir when it doesnt exist
    if not os.path.isdir(path) :
        print('##-PATH CREATE : ' + path)
        os.mkdir(path)
        return True
    return False

def delete_folder(pth) :
    for sub in pth.iterdir() :
        if sub.is_dir() :
            delete_folder(sub)
        else :
            sub.unlink()
    pth.rmdir()

def change_autofocus(self):
    global AUTO_FOCUS
    AUTO_FOCUS = not AUTO_FOCUS
    print("Autofocus is", "on" if AUTO_FOCUS else "off")
