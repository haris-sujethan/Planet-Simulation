import pygame
import math
pygame.init() #initialize the module

WIDTH, HEIGHT =  800, 800 #Pygame window (width and height in pixels) 800x800 would be a square
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Sets up the window
pygame.display.set_caption("Planet Simulation")#title of window


class Planet:
	AU = 149.6e6 * 1000 #Distance from the earth to the sun (astronomical unit) in meters
	G = 6.67428e-11 #Gravitational constant in used to find force of attraction between objects
	SCALE = 250 / AU  #Since real values are used, appropriate scale is required since we are only using a 800x800 window (One AU is 100 pixels in pygame)
	TIMESTEP = 3600*24 #represent how much time we want elapse (3600*24 is one day) 

	def __init__(self, x, y, radius, color, mass): #the x and y are the postion we want the planet to be on the screen
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass #kg

		self.orbit = [] #used to keep track of all the points this planet has travled on, to create a circular representation of the orbit
		self.sun = False #checks if the planet is the sun, beacuse this program draws planets orbiting around the sun. 
		self.distance_to_sun = 0 #updates the value for each planet

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win): #draws planets on window
    #x and y represent how many meters away from the sun (needs to be scaled)
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) > 2:
			updated_points = [] #all the x y coordinates to scale
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2) #takes points, and draws lines between points

		pygame.draw.circle(win, self.color, (x, y), self.radius) 
		 
		if not self.sun:
			distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE) #the distance to the sun in km from each respective planet
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other): #We move the planets from the values of the x_vel and the y_vel and we need to determine those values
		other_x, other_y = other.x, other.y
        #calculate the distance from one object to another 
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance #if the other object is the sun

		force = self.G * self.mass * other.mass / distance**2 #calculating the force of attraction
		theta = math.atan2(distance_y, distance_x) #atan2 python function that takes the y over the x and gives the corresponding angle
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y #with this data we can update the postion of each planet based on the force of attraction between all planets

	def update_position(self, planets): #loops through all the planets and calculate the force of attraction between the current planet and all the other planets. 
                                        #Then calculate what the velocity needs to be for the planets, and move them by that velocity 
		total_fx = total_fy = 0 #total forces exerted on this planet from all other planets 
		for planet in planets:
			if self == planet: #we dont want to calculate the force with ourself (also 0 divsion error)
				continue

			fx, fy = self.attraction(planet)  #for every planet we will calculate the force x and force y it is exerting on this planet
			total_fx += fx
			total_fy += fy # with these forces we can calculate what the velocity of the planet is going to be

		self.x_vel += total_fx / self.mass * self.TIMESTEP #Find the x_vel and y_vel Continuously changing 
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP #updating the x and y postion using the velocity and multipling by the timestep to make sure the planets are moving in the accurate amount of time
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y)) #appending the current x and y postion, enabling the program to draw the orbit of the planet


WHITE = (255, 255, 255) #rgb values
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16) #font color and size, (on the planets, for the distance to the sun)


def main():
	run = True #pygame event loop, infinte loop thats going to run the entire time that the simulation is going. 
	clock = pygame.time.Clock() #frame rate of the game wont go over a certain value

	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) #mass in kg
	sun.sun = True

	earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) #-1 makes the planet drawn to the left (Planet.AU is written with planet because its in class planet)
	earth.y_vel = 29.783 * 1000 

	mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000

	mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000

	venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000

	planets = [sun, earth, mars, mercury, venus]

	while run:
		clock.tick(60) #how many times it updates per second (max)
		WIN.fill((0, 0, 0))
# pygame.display.update()#takes all the drawings after the last update, and draws them
		for event in pygame.event.get():#gets all the events running in pygame
			if event.type == pygame.QUIT: #Only one event is needed, so it will only look for user quit
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()