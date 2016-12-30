#Python game for Space Shooter

"""
Requires Pygame Module, Sqlite3, eztext , random Modules
License GNU V3 Public
Created By Surender Harsha and Piyush Kumar
Drawings and Locations made By Piyush
Collisions Made by Surender
Documentation by Surender Harsha
"""

#Import Statements
import pygame as p
import random
import sqlite3
import sys
import eztext

#GAME VARIABLES
black=(0,0,0)
white=(255,255,255)
fps=35  #The Initial fps of the game
dx=0
dy=0
sx=640
psx=sx
mx=24
nb=0
score=0 	#The Initial score
inc=15      #The Score incrementor
ships=0		#The ships destroyed
maxp=3000   #Maximum random number
lowp=1500   #If the number generated is greater than this, create enemy
upp=1560	#If Number generated is lesser than this , create enemy

#The Class which handles the windows and all the drawing events
class window():
	
	#Co-ordinates of Bullets and Enemies
	bullet_list=[]
	att_list=[]
	
	#Erasing the bullet after collision given a tuple of its co-ordinates
	def make_black(self,l):
		p.draw.rect(self.Bg,black,[l[0]-8,l[1]-32,16,32])
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#Erase the enemy after collision give a tuple
	def black_attk(self,l):
		p.draw.rect(self.Bg,black,[l[0],l[1],48,32])
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#Renders Text given co-ordinates and text, default font=32
	def make_text(self,x,y,text):
		myfont = p.font.SysFont("None", 32)
		mytext = myfont.render(text, True, (255,255,255))
		mytext = mytext.convert_alpha()
		self.screen.blit(mytext,(x,y))
		p.display.flip()
		
	#The Window constructor and initialisation of class Variables	
	def __init__(self):
		
		#Matrix to store pixel values
		self.matrix=[]
		for i in range(20):
			self.matrix.append([])
			for j in range(40):
				self.matrix[i].append((i*32,j*32))


		#Screen Window Initialisation
		p.init()
		self.screen=p.display.set_mode((1280,640))
		p.display.set_caption("SpaceShooter")
		
		#Music Initialisation and play
		p.mixer.music.load('pmd.mp3')
		p.mixer.music.play(-1)
		
		#Creating text box for input of Name
		clock = p.time.Clock()
		txtbx = eztext.Input(maxlength=45, color=white, prompt='Type Your Name: ')
		txtbx.set_pos(800//2,550//2)
		#Wait For Entering of Name
		mainloop=True
		while mainloop:
			clock.tick(30)
			e=p.event.get()
			for events in e:
				if events.type==p.QUIT:
					sys.exit()
				if events.type==p.KEYDOWN and events.key==p.K_RETURN:
					mainloop=False
					break

			self.screen.fill(black)
		# update txtbx
			txtbx.update(e)
		# blit txtbx on the sceen
			txtbx.draw(self.screen)
			p.display.flip()
		# Get Name into variable
		self.name=txtbx.getVal()
		if self.name==None:
			self.name="JACKIE"
		
		#Initialise surface
		self.Bg=p.Surface((1280,640))
		self.Bg.fill(black)
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#Draw the basic spaceship, in triangle , give x value	
	def drawTri(self,x1):
		p.draw.polygon(self.Bg, black, [[psx, 576], [psx-32, 608],[psx+32, 608]])
		p.draw.polygon(self.Bg, white, [[x1, 576], [x1-32, 608],[x1+32, 608]])
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#Draw the attackers and move them towards the player, animation included
	def Attackers(self,x1,y1):
		p.draw.rect(self.Bg,black,[x1,y1,48,32])
		p.draw.rect(self.Bg,white,[x1,y1+3,48,32])
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#Draw the bullets move towards attackers, animation included	
	def Bullets(self,x,y):
		p.draw.rect(self.Bg,black,[x-8,y-32,16,32])
		p.draw.rect(self.Bg,white,[x-8,y-37,16,32])
		self.Bg=self.Bg.convert()
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		
	#When game over, the method runs
	def Game_over(self):
		global score
		global ships
		self.Bg.fill(black)
		self.screen.blit(self.Bg,(0,0))
		p.display.flip()
		self.make_text(800//2,32,"GameOver! Score:"+str(score)+" Ships Destroyed:"+str(ships))
		self.make_text(800//2,64,"HIGH SCORES: Name,Score,Ships")
		#retrieve High scores from database
		global cur
		rs=cur.execute('select * from space order by score desc')
		c=3
		for i in rs:
			self.make_text(400,32*c,str(i[0]))
			self.make_text(600,32*c,str(i[1]))
			self.make_text(800,32*c,str(i[2]))
			c+=1
		
		#wait for Exit game
		while True:
			for e in p.event.get():
				if e.type==p.QUIT:
					sys.exit()
                    #return

					

#Initialise and create window
mainloop=True
clock = p.time.Clock()
a=window()

#Connect to database and be ready with cursor
db=sqlite3.connect('space.db')
cur=db.cursor()
cur.execute('create table if not exists space(name varchar(30),score number,ships number)')

#create sound for explosion
exp=p.mixer.Sound('boom.wav')

#The main game loop initially clocked at 35 fps
while(mainloop):
	clock.tick(fps)
	#Check for keyboard events
	for e in p.event.get():
				if e.type==p.QUIT:
					sys.exit()
				if e.type==p.KEYDOWN:
					if e.key==p.K_LEFT:
						dx=-mx

					if e.key==p.K_RIGHT:
						dx=mx
					if e.key==p.K_SPACE:
						if len(a.bullet_list)<4:
							a.bullet_list.append((sx,576))
				else:
					dx=0
	i=0
	
	#Probability that a ship will appear, Default maxp,lowp,upp
	r=random.randint(0,maxp)
	if r>lowp and r<upp:
		while 1:
			
			#x position at which the enemy appears
			xr=random.randint(32,1280-32)
			if len(a.att_list)>0:
				tup=a.att_list[-1]
			else:
				tup=(1290,-58)
			if xr>tup[0]-10 and xr<tup[0]+58:
				continue
			else:
				a.Attackers(xr,32)
				a.att_list.append((xr,32+3))
				break
		
	#Check if any enemy has crossed the bottom border, if yes, then go to Game_Over method, update DB
	while i<len(a.att_list):
		j=a.att_list[i]
		if j[1]>=604:
			a.black_attk(a.att_list.pop(i))
			cur.execute('insert into space values(?,?,?)',(a.name,score,ships))
			db.commit()
			a.Game_over()
			continue
		a.Attackers(j[0],j[1])
		a.att_list[i]=(j[0],j[1]+3)
		i=i+1
	
	i=0
	
	#update bullet animation, if bullet has reached upper border, erase it.
	while i<len(a.bullet_list):
		j=a.bullet_list[i]
		if j[1]<=10:
			a.make_black(a.bullet_list.pop(i))
			continue
		a.Bullets(j[0],j[1])
		a.bullet_list[i]=(j[0],j[1]-5)
		i=i+1
		
	i=0
	j=0
	flag=0
	
	#Check for collision between bullet and enemies, increase score, fps and ships. Erase both bullet and enemy
	while i<len(a.bullet_list):
		k=a.bullet_list[i]
		j=0
		while j<len(a.att_list):
			q=a.att_list[j]
			if ((k[0]>q[0] and k[0]<q[0]+48) or ((k[0]+16)>q[0] and (k[0]+16)<q[0]+48)) and (k[1]<=q[1]+32):
				exp.play()
				score+=inc
				ships+=1
				inc+=1
				fps+=1
				a.make_black(a.bullet_list.pop(i))
				a.black_attk(a.att_list.pop(j))
				flag=1
				break
			j+=1
		if flag==1:
			flag=0
			continue
		i+=1
		
		
	#Apply Limits for the player
	if sx<=32 and dx==mx:
		sx=sx+dx
	elif sx>=1248 and dx==-mx:
		sx=sx+dx
	elif sx<=32 and dx==-mx:
		sx=sx
	elif sx>=1248 and dx==mx:
		sx=sx
	else:
		sx+=dx
	#Redraw player at new position
	a.drawTri(sx)
	psx=sx
	nb=nb+5
	
#Code End
