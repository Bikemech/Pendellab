from tkinter import Tk, Canvas, Scale
from math import cos, sin, pi
from time import sleep
from matplotlib import pyplot as plt
from collections import deque

class pend:
	def __init__(self, t0, dt, canvas):
		self.dt = dt
		self.theta = t0
		self.steplen = 0.001
		self.const = 1
		self.M = 1
		self.F = 0

		self.arm_color = "#999999"
		self.head_color = "#888800"
		self.bkg=False

		self.frame = canvas

		self.canvas_id = []
		self.plen = 200
		self.center_x = 300
		self.center_y = 300

		self.head_x = self.center_x + self.plen * cos(self.theta)
		self.head_y = self.center_y + self.plen * sin(self.theta)

	def upd(self):
		self.dt = -self.const * sin(self.theta) + self.dt + self.F * self.steplen * 10
		self.dt = self.dt/self.M
		self.theta = self.theta + self.dt * self.steplen

		# if self.theta > 2 * pi:
		# 	self.theta -= 2 * pi
		# elif self.theta < 0:
		# 	self.theta += 2 * pi

		self.head_x = self.center_x + self.plen * cos(self.theta)
		self.head_y = self.center_y + self.plen * sin(self.theta)

	def render(self):
		for item in self.canvas_id:
			self.frame.delete(item)
		self.canvas_id.append(
			self.frame.create_line(self.head_y, self.head_x,
				self.head_y + sin(self.theta + pi/2) * self.F,
				self.head_x + cos(self.theta + pi/2) * self.F)
			)
		self.canvas_id.append(
			self.frame.create_line(self.center_y, self.center_x, self.head_y, self.head_x, width=4, fill = self.arm_color)
			)
		self.canvas_id.append(
			self.frame.create_oval(self.head_y-30, self.head_x-30, self.head_y+30, self.head_x+30, fill=self.head_color)
			)


		if self.bkg:
			self.bring_back()

		self.frame.update()

	def bring_back(self):
		for item in reversed(self.canvas_id):
			self.frame.tag_lower(item)

	def nudge(self, f):
		self.dt += f

class plotter(Canvas):
	def __init__(self, root):
		self.root = root
		self.buffsz = 600
		self.pts = deque()
		self.canvas_id = deque()
		self.width = 600
		self.height = 400
		self.span = self.width//self.buffsz


		super().__init__(root, width=self.width, height=self.height, bg="#bbbbbb")
		self.xaxis = self.create_line(0, self.height/2, self.width, self.height/2, fill = "#000000")
		# self.yaxis = self.create_line(self.width/2, 0, self.width/2, self.height)
		self.pack()

	def plot(self, y):
		new_p = sin(y) * 180 + self.height/2
		if self.pts:
			old_p = self.pts[-1]
		else:
			old_p = new_p
		self.pts.append(new_p)
		if self.pts.__len__() > self.buffsz:
			self.pts.popleft()
			for item in self.canvas_id:
				self.delete(item)
			self.canvas_id = deque()

			for i in range(len(self.pts) - 1):
				self.canvas_id.append(
					self.create_line(self.span*i, self.pts[i], self.span*(i + 1), self.pts[i+1], fill = "#ff0000")
					)
		else:
			self.canvas_id.append(
				self.create_line(
					self.span*self.pts.__len__(), new_p,
					self.span*(self.pts.__len__() - 1), old_p,
					fill = "#ff0000", width=2
					)
				)

		self.update()



root = Tk()
frame = Canvas(root, width=600, height=600, bg = "#554433")
frame.pack()
Momentum = Scale(root, from_ = -314, to_ = 314, orient="horizontal", length=400)
Momentum.pack()

Mscalar = Scale(root, from_=0, to_=1000, orient="horizontal", length=400)
Mscalar.pack()


p = pend(1, 0, frame)

ghost_p = pend(0, 0, frame)
ghost_p.arm_color = "#555555"
ghost_p.head_color = "#555522"
ghost_p.bkg = True


curve = plotter(Tk())
p.M = 1.005


text_error = frame.create_text(100, 100, text=0)
text_target = frame.create_text(100, 120, text=0)
text_pend = frame.create_text(100, 140, text=0)


def nudge(event):
	p.nudge((event.x - 300)/10)


def main():
	error = (p.theta - Momentum.get()/100) % (2 * pi)
	if error > pi:
		error -= 2 * pi

	frame.itemconfig(text_error, text="%.3f"%error)
	frame.itemconfig(text_target, text="%.3f"%(Momentum.get()/100))
	frame.itemconfig(text_pend, text="%.3f"%p.theta)

	ghost_p.theta = Momentum.get()/100
	p.F = -error/(2 * pi) * Mscalar.get()
	# print(error)

	ghost_p.dt = 0
	ghost_p.upd()
	ghost_p.render()
	p.upd()
	p.render()

	curve.plot(error)
	root.after(5, main)

root.bind("<Button-3>", nudge)

main()

frame.mainloop()


