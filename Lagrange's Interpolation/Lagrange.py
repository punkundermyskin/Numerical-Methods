from PIL import Image, ImageDraw
import sys as sy
import mpmath
sy.modules['sympy.mpmath'] = mpmath
from sympy import *
import matplotlib.pyplot as plt
x, y, z = symbols('x, y, z')
init_printing(use_unicode=False, wrap_line=False)

class Lagrange():
	def __init__(self, input_file_name, scale):
		self.img_object = None
		self.pic_name = input_file_name
		self.pic_scale = scale
		self.pic_coordinates = None
		self.pic_size = None
		self.pic_polynome = None
		self.new_points = None
		self.xi_coordinates = []
		self.yi_coordinates = []
		self.x_coordinates = []
		self.y_coordinates = []
	def read_img(self):
		"""
		file_name is the name of the input file.
		Reads the input file.
		Returns a list of x, y coordinates in the intermediate form.
		For excample: pic 3x3, where the diagonal is painted over
		looks lile [[0, 255, 255], [255, 0, 255], [255, 255, 0]].
		"""
		size = list(self.img_object.size)
		pix_val = list(self.img_object.getdata())
		array = []
		for x in pix_val:
			array.append(x[1])
		coordinates = [[0 for x in range(size[0])] for y in range(size[1])]
		count = 0
		for i in range (0,size[1]):
			for j in range (0, size[0]):
				coordinates[i][j] = array[count]
				count += 1
		coordinates.reverse();
		return(coordinates)
	def form_corrdinates(self, matrix):
		"""
		...
		"""
		coordinates = []
		for y in range(0, self.pic_size[0]):
			for x in range(0, self.pic_size[1]):
			   if matrix[x][y] == 0:
				   coordinates.append([x,y])
		for i in coordinates:
			i.reverse()
		check_buff = []
		unique_coordinates = []
		for i in coordinates:
			if i[0] not in check_buff:
				check_buff.append(i[0])
				unique_coordinates.append(i)
		return(unique_coordinates)
	def coordinate_scaling(self, coordinates, flag, scale, size):
		"""
		coordinates - list of coordinates your function,
		scale - list of your function boundaries,
		size - the size of the picture.
		Converts source coordinates to scaled.
		Return corrected coordinates.
		"""
		delta_x = (scale[1]-scale[0])/float(size[0]-1)
		delta_y = (scale[3]-scale[2])/float(size[1]-1)
		
		for y in coordinates:
			if flag == 0:
				y[0] = (y[0]*delta_x)+scale[0]
				y[1] = (y[1]*delta_y)+scale[2]
			else:
				y[0] = int(round((y[0]-scale[0])/delta_x))
				y[1] = int(round((y[1]-scale[2])/delta_y))
		return(coordinates)
	def find_polynome(self, c):
		"""
		[[10.0, 2.0], [12.0, 4.0]]
		"""
		L=0
		for i in range(0, len(c)):
			l = c[i][1]
			for j in range(0,len(c)):
				if i==j:
					continue
				l = l * (x-c[j][0])/(c[i][0]-c[j][0])
			L += l
		return(L)
	def get_value_x_new_points(self):
		"""
		...
		"""
		check_list = []
		for i in range (0, len(self.pic_coordinates)):
			check_list.append(self.pic_coordinates[i][0])
		new_points = []
		for x in range(0, self.pic_size[0]):
			if x not in check_list:
				new_points.append([x,0])
		return(new_points)
	def get_value_y_new_points(self, coordinates):
		"""
		...
		"""
		for i in coordinates:
			i[1] = self.pic_polynome.subs(x, i[0])
		return(coordinates)
	def output_picture(self, coordinates):
		"""
		...
		"""
		img_draw = ImageDraw.Draw(self.img_object)
		for x in coordinates:
			if x[0]>0 and x[1]>0:
				x[1] = (self.pic_size[1]-1)-x[1]
				img_draw.point(x, fill='red')
		self.img_object.save(self.pic_name)
	def processing_basic_pic(self):
		"""
		...
		"""
		self.img_object = Image.open(self.pic_name, 'r')
		matrix = self.read_img()
		self.pic_size = [len(matrix[0]),len(matrix)]
		if (self.pic_scale == None):
			self.pic_scale = list ([0, self.pic_size[0], 0, self.pic_size[1]])
		self.pic_coordinates = self.form_corrdinates(matrix)
		if (len(self.pic_coordinates) < 2):
			if (len(self.pic_coordinates) == 0):
				return(11)
			return (22)
		self.new_points = self.get_value_x_new_points()
		self.pic_coordinates = self.coordinate_scaling(self.pic_coordinates, 0,
			self.pic_scale, self.pic_size)
		for i in self.pic_coordinates:
			self.x_coordinates.append(i[0])
			self.y_coordinates.append(i[1])
	def next_processing(self):
		"""
		...
		"""
		self.pic_polynome = self.find_polynome(self.pic_coordinates)
		self.new_points = self.coordinate_scaling(self.new_points, 0,
			self.pic_scale, self.pic_size)
		self.new_points = self.get_value_y_new_points(self.new_points)
		for i in self.new_points:
			self.xi_coordinates.append(i[0])
			self.yi_coordinates.append(i[1])
	def output_result(self):
		"""
		...
		"""
		self.pic_coordinates = self.coordinate_scaling(self.pic_coordinates, 1,
			self.pic_scale, self.pic_size)
		self.new_points = self.coordinate_scaling(self.new_points, 1, 
			self.pic_scale, self.pic_size)
		self.output_picture(self.new_points)	
	def __str__(self):
		"""
		...
		"""
		plt.plot(self.x_coordinates, self.y_coordinates,'o', self.xi_coordinates, self.yi_coordinates,'.')
		plt.axis(self.pic_scale)
		plt.show()
		return("")
		
def main():
	"""
	...
	"""
	if (len(sy.argv) < 2):
		return("ERROR. Enter path to picture")
	if	(len(sy.argv) > 3) and (len(sy.argv) < 6):
		input_file_name = sy.argv[1]
		scale = list([int(sy.argv[2]), int(sy.argv[3]), 
			int(sy.argv[2]), int(sy.argv[3])])
	else:
		if (len(sy.argv) > 5):
			input_file_name = sy.argv[1]
			scale = list([int(sy.argv[2]), int(sy.argv[3]), 
				int(sy.argv[4]), int(sy.argv[5])])
		else:
			input_file_name = sy.argv[1]
			scale = None
	work(input_file_name, scale)
	
def work(input_file_name, scale):
	"""
	...
	"""

	picture = Lagrange(input_file_name, scale)
	check = picture.processing_basic_pic()
	if (check == 22):
		print ("ERROR! Need more points!")
		return(0)
	if (check == 11):
		print ("ERROR! No points!")
		return(0)
	modif_picture = picture
	modif_picture.next_processing()

	for i in (0, len(sy.argv) - 1):
		if (sy.argv[i] == "-P"):
			print (modif_picture)
	modif_picture.output_result()
		
if __name__=='__main__':
	main()