from scene import *


class Main (Scene):
	def setup(self):
		self.state = 'Play'
		self.n1 = 'Player 1'  # player names
		self.n2 = 'Player 2'
		self.s1 = 501  # player scores
		self.s2 = 501
		self.before = 501  # the players score at the start of their turn
		self.turnsLeft = 3
		self.cur = self.n1  # the player currently throwing
		self.multiplier = 1
		self.background = (0, 0, 0)
		self.tint = (0.3, 0.3, 1)
		self.normal = (1, 1, 1)
		self.states = []
		self.current = -1
		self.redo = False
		self.save()
		
	def draw(self):
		if self.state == 'Play':
			self.drawPlay()
		else:
			self.drawWin()
			
	def drawPlay(self):
		w = self.size.w
		h = self.size.h
		background(self.background)
		f = 'Futura'
		large = 40
		medium = 32.5
		small = 25
		x = 160
		
		tint(self.tint)
		text(str(self.turnsLeft), f, large * 1.5, 5 if self.cur == self.n1 else w - 5, h * 0.1, 6 if self.cur == self.n1 else 4)
		if self.cur == self.n2:
			tint(self.normal)
		text(self.n1 + ': ' + str(self.s1), f, small, 5, 20, 6)
		if self.cur == self.n2:
			tint(self.tint)
		else:
			tint(self.normal)
		text(self.n2 + ': ' + str(self.s2), f, small, w - 5, 20, 4)
		
		tint(self.normal)
		if self.multiplier == 1:
			tint(self.tint)
		text('x1', f, large, w * 0.12, h * 0.635)
		tint(self.normal)
		if self.multiplier == 2:
			tint(self.tint)
		text('x2', f, large, w * 0.12, h * 0.44)
		tint(self.normal)
		if self.multiplier == 3:
			tint(self.tint)
		text('x3', f, large, w * 0.12, h * 0.245)
		tint(self.normal)
		
		for i in range(5):
			for j in range(1, 5):
				num = (i * 4 + j)
				x = (j * w * 0.2) + w * 0.1
				y = ((5 - i) * h * 0.13) + h * 0.05
				text(str(num), f, large, x, y)
				
		text('Miss', f, large, w * 0.5, h * 0.1)
		text('Inner Ring', f, medium, 5, h * 0.8, 6)
		text('Bull\'s Eye', f, medium, w - 5, h * 0.8, 4)
		
		if self.current > 0:
			text('Undo', f, large, 5, h * 0.95, 6)
		
		if self.redo:
			text('Redo', f, large, w * 0.5, h * 0.95, 6)
			
	def drawWin(self):
		w = self.size.w
		h = self.size.h
		f = 'Futura'
		s = 25
		background(self.background)
		text(self.cur + ' wins!', f, s, w * 0.5, h * 0.5)
		text('Tap to start a new game.', f, s, w * 0.5, h * 0.4)
		
	def touch_began(self, touch):
		l = touch.location
		w = self.size.w
		h = self.size.h
		
		if self.state == 'Play':
			if l in Rect(w * 0.03, h * 0.61, w * 0.14, h * 0.06):
				self.multiplier = 1
			if l in Rect(w * 0.03, h * 0.415, w * 0.14, h * 0.06):
				self.multiplier = 2
			if l in Rect(w * 0.03, h * 0.22, w * 0.14, h * 0.06):
				self.multiplier = 3
				
			if l in Rect(w * 0, h * 0.785, w * 0.4, h * 0.045):
				self.addPoint(25)
			if l in Rect(w * 0.625, h * 0.785, w * 0.375, h * 0.045):
				self.addPoint(50)
			if l in Rect(w * 0.395, h * 0.08, w * 0.235, h * 0.06):
				self.addPoint(0)
			
			for i in range(5):
				for j in range(1, 5):
					num = (i * 4 + j)
					a = (j * w * 0.2) + w * 0.1
					b = ((5 - i) * h * 0.13) + h * 0.05
					if l in Rect(a - 20, b - 20, 40, 40):
						self.addPoint(num * self.multiplier)
						
			if l in Rect(w * 0, h * 0.925, w * 0.31, h * 0.065) and self.current > 0:
				self.current -= 1
				self.load()
				self.redo = True
				
			if l in Rect(w * 0.49, h * 0.925, w * 0.29, h * 0.065) and self.redo:
				self.current += 1
				self.load()
		else:
			self.setup()  # start a new game
						
	def addPoint(self, value):
		self.turnsLeft -= 1
		if self.cur == self.n1:
			self.s1 -= value
			if self.s1 == 0 and self.multiplier == 2:
				self.state = 'Win'
				return
			elif self.s1 <= 1:
				self.s1 = self.before
				self.turnsLeft = 0
		else:
			self.s2 -= value
			if self.s2 == 0 and self.multiplier == 2:
				self.state = 'Win'
				return
			elif self.s2 <= 1:
				self.s2 = self.before
				self.turnsLeft = 0
				
		if self.turnsLeft == 0:
			self.turnsLeft = 3
			if self.cur == self.n1:
				self.cur = self.n2
				self.before = self.s2
			else:
				self.cur = self.n1
				self.before = self.s1
				
		self.save()
		
	# Handling saving and loading states for undo and redo
	def save(self):
		self.current += 1
		if len(self.states) > self.current:
			self.states[self.current] = [self.s1, self.s2, self.before, self.turnsLeft, self.cur]
			self.states[self.current + 1:] = []
		else:
			self.states.append([self.s1, self.s2, self.before, self.turnsLeft, self.cur])
		self.redo = False
		
	def load(self):
		s = self.states[self.current]
		self.s1 = s[0]
		self.s2 = s[1]
		self.before = s[2]
		self.turnsLeft = s[3]
		self.cur = s[4]
		if self.current == len(self.states) - 1:
			self.redo = False
		
run(Main(), PORTRAIT)
