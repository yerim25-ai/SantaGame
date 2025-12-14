from email.mime import image
from tkinter import * # tkinter에서 모든 정의를 임포트한다.
import time
import pygame
import random


class Enemy:
	def __init__(self,canvas,images,id):
		self.__frame = 0		
		self.id = 'e'+str(id)
		self.canvas = canvas
		self.images = images
		self.me = self.canvas.create_image(1440,random.randint(10,950), image = self.images[0],tags=self.id)
		self.frame = 0

	def update(self):
		self.canvas.itemconfig(self.me, image = self.images[self.frame%len(self.images)])
		self.canvas.move(self.me,-4,0)		
		self.frame = self.frame + 1

	def getPos(self):
		return self.canvas.coords(self.me)

	def getId(self):
		return self.me


class Gift:
	def __init__(self,canvas,images,id):
		self.__frame = 0		
		self.id = 'e'+str(id)
		self.canvas = canvas
		self.images = images
		self.me = self.canvas.create_image(1440,random.randint(10,950), image = self.images[0],tags=self.id)
		self.frame = 0
		

	def update(self):
		self.canvas.itemconfig(self.me, image = self.images[self.frame%len(self.images)])
		self.canvas.move(self.me,-4,0)		
		self.frame = self.frame + 1

	def getPos(self):
		return self.canvas.coords(self.me)

	def getId(self):
		return self.me

	

class ShootingGame:
	def __init__(self):
		self.window = Tk() # 윈도우 생성
		self.window.title("귀여운 산타를 지켜라!") # 제목을 설정
		self.window.geometry("1440x750") # 윈도우 크기 설정
		self.window.resizable(0,0)        
		self.lastTime = time.time()
		self.lightingTimer = time.time()
		self.keys=set()
		self.canvas = Canvas(self.window, bg = "white")
		self.canvas.pack(expand=True,fill=BOTH)
		self.window.bind("<KeyPress>",self.keyPressHandler)
		self.window.bind("<KeyRelease>",self.keyReleaseHandler)
		self.window.protocol("WM_DELETE_WINDOW", self.onClose)


		self.my_images_number=0 #산타 이미지
		self.myimages=[PhotoImage(file='image/santa_fly.png').subsample(11)]

		self.enemy_img1_number=0 #괴물1 이미지
		self.enemyimages1=[PhotoImage(file='image/monster1.png').subsample(6)]

		self.enemy_img2_number=0 #괴물2 이미지
		self.enemyimages2=[PhotoImage(file='image/monster2.png').subsample(6)]

		self.gift_img_number=0 #선물 이미지
		self.giftimages=[PhotoImage(file='image/gift.png').subsample(13)]

		self.background_img = PhotoImage(file='image/background.png') #배경 이미지

		self.bomb=[PhotoImage(file='image/bomb.png').subsample(7)] #폭탄 이미지

		#산타 이미지 설정
		self.santa=self.canvas.create_image(300, 480, image=self.myimages[0], tags='santa')

		#괴물1 리스트와 아이디
		self.enemy1_list=[]
		self.enemy1_id=0

		#괴물 2 리스트와 아이디
		self.enemy2_list=[]
		self.enemy2_id=0

		#선물 리스트와 아이디
		self.gift_list=[]
		self.gift_id=0

		#배경음악 설정
		pygame.init()
		pygame.mixer.music.load("sound/bgm.mp3")
		pygame.mixer.music.play(-1)

		#효과음 설정
		self.sounds=pygame.mixer
		self.sounds.init()
		self.s_effect1=self.sounds.Sound("sound/get_happy.mp3") #상품 얻는 소리
		self.s_effect2=self.sounds.Sound("sound/bomb_sad.mp3") #폭탄으로 괴물 죽이는 소리

		#화면에 설명글
		self.canvas.create_text(150,50,fill="black", font="Times 15 italic bold", text="입력키:↑, ↓, ←, →, space")
		
		#배경 이미지를 두 장로 연결하려고 준비하는
		self.bg_width = self.background_img.width() #배경 사진의 너비를 저장하는
		
		self.bg_x1 = 0 #첫 번째 배경 이미지의 x좌표를 0으로 초기화
		self.bg_x2 = self.bg_width #두 번째 배경 이미지의 x좌표를 이미지 너비로 설정. 이미지가 끝나는 부분에 바로 이미지2가 붙을 수 있도록
		
		         #anchor="nw"는 기준점을 왼쪽 위로 하겠다는 의미
				 #self.cavas는 캔버스 위에서 뭘 한다는 의미
				 #이미지 1,2를 각각 그려서 self.bg1과 self.bg2에 각각의 오브젝트 id를 저장한다는 의미
		self.bg1 = self.canvas.create_image(self.bg_x1, 0, image=self.background_img, anchor="nw")
		self.bg2 = self.canvas.create_image(self.bg_x2, 0, image=self.background_img, anchor="nw")


		#배경 이미지 뒤로 움직이게 하는
	#def move_background(self):
		#self.bg_x1 -= 4 #이 함수가 실행될 때마다 x좌표가 4픽셀만큼 왼쪽으로 이동 
		#self.bg_x2 -= 4 #이 함수가 실행될 때마다 x좌표가 4픽셀만큼 왼쪽으로 이동 
			
		#if self.bg_x1 <= -self.bg_width:
			#첫 번째 배경이 완전히 화면 왼쪽으로 나가서 그 너비만큼 왼쪽으로 이동했는지 확인하는
            #bg_x1이 -bg_width 이하라면 첫 번째 이미지는 화면에서 완전히 보이지 않음
			#self.bg_x1 = self.bg_width
			#bg_x1의 x좌표를 이미지의 너비로 설정한다. 즉 남아있는 이미지 바로 오른쪽에 다시 이미지 생성으로 붙는 것
		#if self.bg_x2 <= -self.bg_width:
			#self.bg_x2 = self.bg_width
			#이 if문도 윗 쪽 if처럼 2번의 좌표가 넘어가서 화면에 안 보일 경우 다시 1번 그림의 오른쪽에 붙는다는 뜻
				
		#self.canvas.coords(self.bg1, self.bg_x1, 0)
		#self.canvas.coords(self.bg2, self.bg_x2, 0)
			#self.bg1과 self.bg2의 x좌표가 각각 갱신된다
			
		#self.window.after(20, self.move_background)
			#20밀리리초..? 후에 함수 실행한다는 의미


		#폭탄이 화면에서 어떻게 나오는지 설정
		while True:

			try:
				self.canvas.itemconfig(self.santa, image = self.myimages[self.my_image_number%len(self.myimages)])    			

				self.my_image_number += 1
				self.enemy_img_number += 1

				bombs = self.canvas.find_withtag("bomb")
				self.display()
			

				for bomb in bombs:
					self.canvas.move(bomb,9,0)
					if self.canvas.coords(bomb)[0] > self.canvas.winfo_width():
						self.canvas.delete(bomb)
			    

				self.manageEnemy()
				self.manageGift()

            #윈도우 강제 종료 에러 방지
			except TclError:
				return

			self.window.after(33)
			self.window.update()


	#괴물들 이미지 이벤트 루프 생성
	def manageEnemy(self):
		if (random.randint(0,110) == 0):		
			self.enemy1_list.append(Enemy(self.canvas,self.enemyimages1,self.enemy1_id))
			self.enemy1_id = self.enemy1_id + 1

		if (random.randint(0,110) == 0):		
			self.enemy2_list.append(Enemy(self.canvas,self.enemyimages2,self.enemy2_id))
			self.enemy2_id = self.enemy2_id + 1

		for e in self.enemy1_list:
			e.update()
			if e.getPos()[0] < 0:
				self.canvas.delete(e.getId())
				self.enemy1_list.pop(self.enemy1_list.index(e))

		for e in self.enemy2_list:
			e.update()
			if e.getPos()[0] < 0:
				self.canvas.delete(e.getId())
				self.enemy2_list.pop(self.enemy2_list.index(e))

		bombs=self.canvas.find_withtag("bomb")
		area=25
		for bomb in bombs:
			f_pos = self.canvas.coords(bomb)
			for e in self.enemy1_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect2.play()
					self.canvas.delete(e.getId())
					self.enemy1_list.pop(self.enemy1_list.index(e))
					self.canvas.delete(bomb)

		bombs=self.canvas.find_withtag("bomb")
		area=25
		for bomb in bombs:
			f_pos = self.canvas.coords(bomb)
			for e in self.enemy2_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect2.play()
					self.canvas.delete(e.getId())
					self.enemy2_list.pop(self.enemy2_list.index(e))
					self.canvas.delete(bomb)


	#선물 이미지 이벤트 루프 생성
	def manageGift(self):
		if (random.randint(0,160) == 0):		
			self.gift_list.append(Gift(self.canvas,self.giftimages,self.gift_id))
			self.gift_id = self.gift_id + 1

		for e in self.gift_list:
			e.update()
			if e.getPos()[0] < 0:
				self.canvas.delete(e.getId())
				self.gift_list.pop(self.gift_list.index(e))

		bombs=self.canvas.find_withtag("bomb")
		area=25
		for bomb in bombs:
			f_pos = self.canvas.coords(bomb)
			for e in self.gift_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect2.play()
					self.canvas.delete(e.getId())
					self.gift_list.pop(self.gift_list.index(e))
					self.canvas.delete(bomb)

	#키보드 누른거 기록 삭제하는 코드
	def keyReleaseHandler(self, event):
		if event.keycode in self.keys:
			self.keys.remove(event.keycode)

	#키보드 설정
	def display(self):
		santa = self.canvas.find_withtag("santa")
		for key in self.keys:
			if key == 39: #오른쪽 키
				self.canvas.move(santa, 5, 0)
			if key == 37: #왼쪽 키
				self.canvas.move(santa, -5, 0)
			if key == 38: #아래쪽 키
				self.canvas.move(santa, 0, -5)
			if key == 40: #위쪽 키
				self.canvas.move(santa, 0, 5)
			if key == 32: #스페이스 바
				now = time.time()#print(now-self.lastTime)
				if (now-self.lastTime) > 0.3:
					self.lastTime = now
					pos = self.canvas.coords(santa)
					self.canvas.create_image(pos[0]+95, pos[1]+12, image = self.bomb,tags="bomb")

	#마무리 설정
	def keyPressHandler(self, event):		
		if event.keycode == 27:#esc key 입력시 종료			
			self.onClose()
			
		else:
			self.keys.add(event.keycode)

	def onClose(self):
		self.running = False
		pygame.mixer.music.stop()
		pygame.quit()
		self.window.destroy()
		
ShootingGame()



		#_init_에 나중에 추가하기 -> 배경 이미지 움직이게 하는
		#self.move_background()
