import os
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
		self.me = self.canvas.create_image(1440,random.randint(100,700), image = self.images[0],tags=self.id) #괴물들 나오는 세로 범위 설정함
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
		self.me = self.canvas.create_image(1440,random.randint(100,700), image = self.images[0],tags=self.id) #선물 나오는 세로 범위 설정함
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
		self.window.title("우리의 산타를 지켜라!") # 제목을 설정
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
		
		 
		self.running = True #gameloop

		#이미지 정의 부분

		self.my_images_number=0 #산타 이미지
		self.myimages=[PhotoImage(file='image/santa_fly.png').subsample(11)]

		self.enemy_img1_number=0 #괴물1 이미지
		self.enemyimages1=[PhotoImage(file='image/monster1.png').subsample(6)]

		self.enemy_img2_number=0 #괴물2 이미지
		self.enemyimages2=[PhotoImage(file='image/monster2.png').subsample(6)]

		self.gift_img_number=0 #선물 이미지
		self.giftimages=[PhotoImage(file='image/gift.png').subsample(17)]

		self.santa_intro = [PhotoImage(file='image/santa_intro.png').subsample(6)] #시작 화면(1번)에서의 산타 이미지

		self.rudolph = [PhotoImage(file='image/rudolph.png').subsample(5)] #시작 화면(1번)에서의 루돌프 이미지

		self.startBackground_img = PhotoImage(file='image/start_background.png') #시작 배경 이미지 (1번)

		self.background_img = PhotoImage(file='image/background_winter.png').subsample(4) #게임 배경 이미지 (2번)

		self.endBackground_img = PhotoImage(file='image/end_background2.png').zoom(1) #종료 배경 이미지 (3번)

		self.bomb=[PhotoImage(file='image/bomb.png').subsample(7)] #폭탄 이미지

		self.boom=[PhotoImage(file='image/bomm.png').subsample(7)] #폭탄 터질 때 이미지

		self.star=[PhotoImage(file='image/one_star_GIF.gif', format = 'gif -index %i' %(i)).subsample(3) for i in range(4)]  #선물 얻을 때 이미지

		self.stick=[PhotoImage(file='image/stick.png').subsample(4)] #윗 안내판(막대기) 이미지

		#안내판에서의 점수 숫자 정의
		self.score=0
		#self.score_text = self.canvas.create_text(820, 30, fill="white", font="Times 15 italic bold", text=str(self.score))


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
		self.s_effect1=self.sounds.Sound("sound/get_happy.mp3") #선물 얻는 소리
		self.s_effect2=self.sounds.Sound("sound/bomb_sad.mp3") #폭탄으로 괴물 죽이는 소리
		self.s_effect3=self.sounds.Sound("sound/end.mp3") #게임 끝나는 소리

		
		#배경 이미지를 두 장으로 연결하려고 준비하는
		self.bg_width = self.background_img.width() #배경 사진의 너비를 저장하는


		#true면 시작 안내 배경, false면 게임 배경으로 전환된다. 현재는 true이므로 시작 안내 배경이 나온다.
		self.waiting_start = True

		#시작 안내 배경 먼저 호출
		self.start_screen()


	#시작 안내 배경(1번) 관련 코드
	def start_screen(self):
		# 시작 배경 설정
		self.canvas.create_image(0, 0, image=self.startBackground_img, anchor="nw")

		self.canvas.create_image(1100,200, image=self.santa_intro, anchor="nw")

		self.canvas.create_image(60,210, image=self.rudolph, anchor="nw")


		# 안내 문구
		self.canvas.create_text(
			720, 50,
			text="우리의         를 지켜라!",
			font=("Times 40 bold"),
			fill="black")

		self.canvas.create_text(
			688, 50,
			text="산타",
			font=("Times 40 bold"),
			fill="red")

		self.canvas.create_text(
			720, 110,
			text="★산타가 아이들에게 줄 선물을 모으는 것을 도와주세요★",
			font=("Times 19 bold"),
			fill="black")

		self.canvas.create_text(
			720, 320,
			text="1. 괴물을 물리치면 선물 1개를 획득합니다.\n\n2. 선물상자를 먹으면 선물 3개를 획득합니다.\n\n3. 괴물은 폭탄을 이용해 물리칠 수 있습니다.\n\n4. 산타가 괴물과 충돌하면 선물 모으는 것을 중단합니다.\n\n5. 화면 소리를 높이면 더욱 높은 몰입도를 느낄 수 있습니다.",
			font=("Times 19"),
			fill="black",
			justify="center")

		self.canvas.create_text(
			720, 720,
			text="화면을 클릭하면 산타가 있는 장소로 이동합니다!",
			font=("Times 17 italic bold"),
			fill="black")

		#캔버스 위에서 마우스 왼쪽 버튼을 누르면 start_game으로 넘어간다는 의미
		self.canvas.bind("<Button-1>", self.start_game)


	#안내 화면(1번)에서 게임 화면(2번)으로 넘어갈 때 실행되는 함수
	def start_game(self, event=None):
	# 이미 시작했으면 무시한다는 의미
		if not self.waiting_start:
			return

		#음악 재생
		pygame.mixer.music.play(-1)

		#waiting_start가 false경우 게임 화면(2번)으로 넘어감
		self.waiting_start = False

		# 시작 화면 클릭 이벤트 제거한다
		self.canvas.unbind("<Button-1>")

		# 시작 화면 지우기
		self.canvas.delete("all")

		# 게임 화면 세팅 (함수 호출)
		self.setup_game_screen()

		# 게임 루프 시작
		self.running = True
		self.game_loop()


	#게임 화면(2번)이 나올때 관련된 코드
	def setup_game_screen(self):
	# 게임을 다시 시작할 경우 점수 초기화
		self.score = 0

	# 안내판 굴 관련 코드
		self.stick1 = self.canvas.create_image(0, 0, image=self.stick, anchor="nw")
		self.guide = self.canvas.create_text(
			125, 30, fill="white",
			font="Times 15 italic bold",
			text="입력키 : ↑, ↓, ←, →, space"
	)
		self.score_pan = self.canvas.create_text(
			688, 30, fill="white",
			font="Times 15 italic bold",
			text="산타가 획득한 선물 개수 :"
	)
		self.score_text = self.canvas.create_text(
			820, 30, fill="white",
			font="Times 15 italic bold",
			text=str(self.score)
	)
		self.text = self.canvas.create_text(
			1350, 30, fill="yellow",
			font="Times 15 italic bold",
			text="Merry Christmas!"
	)

	# 산타 이미지 설정
		self.santa = self.canvas.create_image(
			300, 480, image=self.myimages[0], tags='santa'
	)

	# 배경 이미지 설정
		self.bg_x1 = 0
		self.bg_x2 = self.bg_width
		self.bg1 = self.canvas.create_image(self.bg_x1, 0, image=self.background_img, anchor="nw")
		self.bg2 = self.canvas.create_image(self.bg_x2, 0, image=self.background_img, anchor="nw")
		self.canvas.tag_lower(self.bg1)
		self.canvas.tag_lower(self.bg2)

	# 적/선물 리스트 초기화 (게임을 다시 시작할 경우 초기화해야하므로)
		self.enemy1_list.clear()
		self.enemy2_list.clear()
		self.gift_list.clear()


	# 배경 이미지 뒤로 움직이게 하는 함수
	def move_background(self):
		self.bg_x1 -=  2.3 #이 함수가 실행될 때마다 x좌표가 2.3픽셀만큼 왼쪽으로 이동 
		self.bg_x2 -= 2.3 #이 함수가 실행될 때마다 x좌표가 2.3픽셀만큼 왼쪽으로 이동 
			
		if self.bg_x1 <= -self.bg_width:
			# 첫 번째 배경이 완전히 화면 왼쪽으로 나가서 그 너비만큼 왼쪽으로 이동했는지 확인하는
			# bg_x1이 -bg_width 이하라면 첫 번째 이미지는 화면에서 완전히 보이지 않음
			self.bg_x1 = self.bg_width
			# bg_x1의 x좌표를 이미지의 너비로 설정한다. 즉 남아있는 이미지 바로 오른쪽에 다시 이미지 생성으로 붙는 것
		if self.bg_x2 <= -self.bg_width:
			self.bg_x2 = self.bg_width
			# 이 if문도 윗 쪽 if처럼 2번의 좌표가 넘어가서 화면에 안 보일 경우 다시 1번 그림의 오른쪽에 붙는다는 뜻
				
		self.canvas.coords(self.bg1, self.bg_x1, 0)
		self.canvas.coords(self.bg2, self.bg_x2, 0)
			# self.bg1과 self.bg2의 x좌표가 각각 갱신된다

	
	#게임의 메인 루프, while true를 수정한 부분임
	def game_loop(self):
		if not self.running:
			return # 게임 종료 상태면 루프 중단

		try:
			# 배경 움직임 처리
			self.move_background()
			
			# 산타 애니메이션 업데이트
			self.canvas.itemconfig(self.santa, image = self.myimages[self.my_images_number%len(self.myimages)])
			self.my_images_number += 1
			self.enemy_img1_number += 1
			self.enemy_img2_number += 1

			# 폭탄 움직임 및 화면 밖 삭제
			bombs = self.canvas.find_withtag("bomb")
			self.display()
		
			for bomb in bombs:
				self.canvas.move(bomb,9,0)
				if self.canvas.coords(bomb)[0] > self.canvas.winfo_width():
					self.canvas.delete(bomb)


			# 적과 선물 관리 및 충돌 처리
			self.manageEnemy()
			self.manageGift()

		# 윈도우 강제 종료 에러 방지
		except TclError:
			self.running = False
			return

		# 33ms 후에 game_loop 함수를 다시 실행하도록 예약
		self.window.after(33, self.game_loop)

		#안내판 이미지가 맨 위로 올라오게 하는 코드 (game_loop에 넣어야 위로 올라간다)
		self.canvas.tag_raise(self.stick1)

		#안내글을 더 위로 올라오게 함
		self.canvas.tag_raise(self.guide)
		self.canvas.tag_raise(self.score_pan)
		self.canvas.tag_raise(self.text)
		self.canvas.tag_raise(self.score_text)
		self.canvas.tag_raise(self.star)


	#괴물들 이미지 이벤트 루프 생성
	def manageEnemy(self):
		if (random.randint(0,100) == 0):		
			self.enemy1_list.append(Enemy(self.canvas,self.enemyimages1,self.enemy1_id))
			self.enemy1_id = self.enemy1_id + 1

		if (random.randint(0,100) == 0):		
			self.enemy2_list.append(Enemy(self.canvas,self.enemyimages2,self.enemy2_id))
			self.enemy2_id = self.enemy2_id + 1


		#괴물 이미지1의 움직임을 설정
		for e in self.enemy1_list[:]:
			e_pos=e.getPos()
			if not e_pos:
				self.enemy1_list.remove(e)
				continue

			e.update()
			if e_pos[0] < 0:
				self.canvas.delete(e.getId())
				self.enemy1_list.remove(e)

		#괴물 이미지2의 움직임을 설정
		for e in self.enemy2_list[:]:
			e_pos=e.getPos()
			if not e_pos:
				self.enemy2_list.remove(e)
				continue

			e.update()
			if e_pos[0] < 0:
				self.canvas.delete(e.getId())
				self.enemy2_list.remove(e)

		#폭탄과 괴물1이 충돌했을 경우
		bombs=self.canvas.find_withtag("bomb")
		area=31
		for bomb in bombs:
			f_pos = self.canvas.coords(bomb)
			for e in self.enemy1_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect2.play()
					self.canvas.delete(e.getId())
					self.enemy1_list.pop(self.enemy1_list.index(e))
					self.canvas.delete(bomb)

					#폭탄과 괴물1이 충돌하여 boom(bomm) 이미지 나타나는 것
					self.boom_img = self.canvas.create_image(f_pos[0], f_pos[1], image=self.boom, anchor="nw")
					#0.6초 후에 boom(bomm) 이미지가 사라지는 것
					self.window.after(600, lambda b=self.boom_img: self.canvas.delete(b))

					#괴물1을 처리했을 때 점수(score)가 1씩 증가한다는 의미
					self.score += 1
					self.canvas.itemconfig(self.score_text, text=str(self.score))

					break # 폭탄이 이미 터졌으므로 다음 폭탄으로 넘어감
				
		#산타 이미지와 괴물1 이미지가 충돌했을 때
		area=63
		santa_pos = self.canvas.coords(self.santa) #산타 이미지의 현재 위치 찾는 코드
		for e in self.enemy1_list[:]: #괴물 1 이미지를 삭제하면서 오류 발생을 예방해주는 코드
			e_pos = e.getPos() #괴물1 이미지의 위치를 정의
			if e_pos and len(e_pos) >= 2: 
				if abs(e_pos[0] - santa_pos[0]) < area and abs(e_pos[1] - santa_pos[1]) < area: #충돌 했는지 안했는지 여부 체크하는 부분					
					self.canvas.delete(e.getId()) #산타 이미지와 충돌한 괴물1 삭제
					self.enemy1_list.pop(self.enemy1_list.index(e)) #리스트에서도 삭제
					self.gameOver() #게임 종료 시 실행되는 함수 호출

		#폭탄과 괴물2가 충돌했을 경우
		bombs=self.canvas.find_withtag("bomb")
		area=31
		for bomb in bombs:
			f_pos = self.canvas.coords(bomb)
			for e in self.enemy2_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect2.play()
					self.canvas.delete(e.getId())
					self.enemy2_list.pop(self.enemy2_list.index(e))
					self.canvas.delete(bomb)

					#폭탄과 괴물1이 충돌하여 boom(bomm) 이미지 나타나는 것
					self.boom_img = self.canvas.create_image(f_pos[0], f_pos[1], image=self.boom, anchor="nw")
					#0.6초 후에 boom(bomm) 이미지가 사라지는 것
					self.window.after(600, lambda b=self.boom_img: self.canvas.delete(b))

					#괴물2를 처리했을 때 점수(score)가 1씩 증가한다는 의미
					self.score += 1
					self.canvas.itemconfig(self.score_text, text=str(self.score))

					break # 폭탄이 이미 터졌으므로 다음 폭탄으로 넘어감

		#산타 이미지와 괴물2 이미지가 충돌했을 때
		area=63
		santa_pos = self.canvas.coords(self.santa) #산타 이미지의 현재 위치 찾는 코드
		for e in self.enemy2_list[:]: #괴물 2 이미지를 삭제하면서 오류 발생을 예방해주는 코드
			e_pos = e.getPos() #괴물2 이미지의 위치를 정의
			if e_pos and len(e_pos) >= 2: 
				if abs(e_pos[0] - santa_pos[0]) < area and abs(e_pos[1] - santa_pos[1]) < area: #충돌 했는지 안했는지 여부 체크하는 부분
					self.canvas.delete(e.getId()) #산타 이미지와 충돌한 괴물2 삭제
					self.enemy2_list.pop(self.enemy2_list.index(e)) #리스트에서도 삭제
					self.gameOver() #게임 종료 시 실행되는 함수 호출


	#선물 이미지 이벤트 루프 생성
	def manageGift(self):
		if (random.randint(0,160) == 0):		
			self.gift_list.append(Gift(self.canvas,self.giftimages,self.gift_id))
			self.gift_id = self.gift_id + 1

		for e in self.gift_list[:]:
			e_pos = e.getPos()
			if not e_pos:
				self.gift_list.remove(e)
				continue

			e.update()
			if e_pos[0] < 0:
				self.canvas.delete(e.getId())
				self.gift_list.remove(e)

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
					break # 폭탄이 이미 터졌으므로 다음 폭탄으로 넘어감

		#산타 이미지와 선물 이미지가 충돌하였을 때
		area=50
		santa_pos = self.canvas.coords(self.santa) #산타 이미지의 현재 위치 찾는 코드
		for e in self.gift_list[:]: #선물 이미지를 삭제하면서 오류 발생을 예방해주는 코드
			e_pos = e.getPos() #선물 이미지의 위치를 정의
			if abs(e_pos[0] - santa_pos[0]) < area and abs(e_pos[1] - santa_pos[1]) < area: #충돌 했는지 안했는지 여부 체크하는 부분
				self.s_effect1.play()
				self.canvas.delete(e.getId()) #산타 이미지와 충돌한 선물 삭제
				self.gift_list.pop(self.gift_list.index(e)) #리스트에서도 삭제
				
				#별 이미지 설정
				self.oneStar = self.canvas.create_image(e_pos[0], e_pos[1], image=self.star[0], anchor="nw")

				#gif는 여러개의 장으로 이루어져있으므로 인덱스 정의해줌
				frame_index = 0

				#한 장씩 꺼내서 이어붙이는 코드
				def gif_star():
					nonlocal frame_index
					frame_index = (frame_index + 1) % len(self.star)
					self.canvas.itemconfig(self.oneStar, image=self.star[frame_index])
					self.canvas.after(100, gif_star)  # 0.1초마다 다음 프레임

				gif_star()

				# 0.6초 후 삭제
				self.canvas.after(600, lambda: self.canvas.delete(self.oneStar))

				#산타가 선물을 먹으면 3씩 점수가 증가한다는 의미 
				self.score += 3
				self.canvas.itemconfig(self.score_text, text=str(self.score)) 

	#키보드 누른거 기록 삭제하는 코드
	def keyReleaseHandler(self, event):
		if event.keycode in self.keys:
			self.keys.remove(event.keycode)

	#키보드 설정
	def display(self):
		santa = self.canvas.find_withtag("santa")
		#산타 위치 가져오는 코드
		x, y = self.canvas.coords(santa)
		for key in self.keys:
			if key == 39: #오른쪽 키
				if x < 1440 - 30: #이 범위를 넘어서지 않는 경우에만 이동 가능
					self.canvas.move(santa, 5, 0)
			if key == 37: #왼쪽 키
				if x > 30: #이 범위를 넘어서지 않는 경우에만 이동 가능
					self.canvas.move(santa, -5, 0)
			if key == 38: #아래쪽 키 (tkinter의 y좌표는 위로 갈수록 작아짐)
				self.canvas.move(santa, 0, -5)
			if key == 40: #위쪽 키 (tkinter의 y좌표는 아래로 갈수록 커짐)
				self.canvas.move(santa, 0, 5)
			if key == 32: #스페이스 바
				now = time.time()#print(now-self.lastTime)
				if (now-self.lastTime) > 0.3:
					self.lastTime = now
					pos = self.canvas.coords(santa)
					self.canvas.create_image(pos[0]+95, pos[1]+12, image = self.bomb[0],tags="bomb") # 폭탄 이미지를 리스트가 아닌 PhotoImage 객체로 참조


	#산타 이미지와 괴물 이미지들이 충돌하여 게임이 끝났을 때 실행되는 함수
	def gameOver(self, *args):
		pygame.mixer.music.stop() #배경음악 멈추기

		# 게임이 끝났다는 소리
		self.s_effect3.play()

		# 게임 루프 종료
		self.running = False  

		#다시 시작하기 클릭 이벤트 제거
		self.canvas.unbind("<Button-1>")

		# 화면 지우기
		self.canvas.delete("all")  

		# 게임 종료시 종료 이미지가 나타나는 코드
		self.canvas.create_image(0, 0, image=self.endBackground_img, anchor="nw")

		# 종료 화면에 나오는 설명글
		  #점수가 0점보다 높을 경우
		if self.score > 0:
			self.canvas.create_text(
				735, 500,
				text=f"{self.score}개밖에 선물을 모으지 못했다네..\n \n조금만 더 나를 도와주게!",
				font=("Times 30 bold"),
				fill="black",
				justify="center" #텍스트를 가운데 정렬
		)
			  #점수가 0점일 경우
		else:
			self.canvas.create_text(
				735, 500,
				text="이런이런..\n 선물을 하나도 얻지 못했어..😭",
				font=("Times 30 bold"),
				fill="black",
				justify="center" #텍스트를 가운데 정렬
				)

		#게임 다시 시작 문구
		self.canvas.create_text(
			735, 720,
			text="화면을 클릭해서 다시 산타를 지키러 가보자!",
			font=("Times 23 bold"),
			fill="red"
			)

		#마우스로 캔버스를 클릭하면 다시 게임이 시작하도록 하는 코드
		self.waiting_start = True
		self.canvas.bind("<Button-1>", self.start_game)


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

#클래스 외부에서 실행하는 것으로 게임을 시작하겠다는 의미
if __name__ == "__main__":
    game = ShootingGame()
    # 이 코드가 없으면 윈도우가 화면에 나타나지 않음
    game.window.mainloop()