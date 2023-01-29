""" Set up the imports """
import pygame, sys
from pygame.locals import *
from mcpi.minecraft import Minecraft

""" Set up the pygame """
pygame.init()

""" Set up the colors """
BLACK = (0,0,0)
WHITE = (255,255,255)

""" Set up the basic functions """
def drawText(text,font,surface,x,y,COLOR=BLACK):
	pygame.init()
	textobj = font.render(text,1,COLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj, textrect)
def Im(ImageName):
	return pygame.image.load(f'/home/pi/Documents/mc_images/{ImageName}.png')
def RECT(Im_obj):
	return Im_obj.get_rect()
	
""" GUI function """
def PICRAFT():
	try:
		mc = Minecraft.create()
	except:
		print("Please Start Minecraft Pi Edition. Cannot Currently Connect.")
		pygame.quit()
		sys.exit()

	# Set up the window, font, and clock
	WINDOWWIDTH = 235
	WINDOWHEIGHT = 500
	font = pygame.font.SysFont(None, 22)
	windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('PiCraft Companion')
	mainClock = pygame.time.Clock()
	mc_icon = pygame.transform.scale(Im("mc_grass_block"), (28,32))
	pygame.display.set_icon(mc_icon)
	
	# Set up the sprites
	item_column = Im("item_column")
	item_column_rect = Rect(18,25,200,450)
	
	# Set up the sprites for the block icons
	bush = Im("bush")
	grass = Im("grass")
	snow = Im("snow")
	ice = Im("ice")
	water = Im("water")
	lava = Im("lava")
	mushroom_brown = Im("mushroom_brown")
	mushroom_red = Im("mushroom_red")
	tnt = Im("tnt")
	cobweb = Im("cobweb")
	bedrock = Im("bedrock")
	BACKGROUND_BLANK = Im("background_blank")
	none = Im("blank")
	bush_rect = RECT(bush)
	grass_rect = RECT(grass)
	snow_rect = RECT(snow)
	ice_rect = RECT(ice)
	water_rect = RECT(water)
	lava_rect = RECT(lava)
	mushroom_brown_rect = RECT(mushroom_brown)
	mushroom_red_rect = RECT(mushroom_red)
	tnt_rect = RECT(tnt)
	cobweb_rect = RECT(cobweb)
	bedrock_rect = RECT(bedrock)
	BACKGROUND_BLANK_rect = RECT(BACKGROUND_BLANK)
	
	
	# Set up the block variables (as tuples)
	c1 = water, Rect(50.0,50,32,32), "Water", 8, None
	c2 = lava, Rect(50.0,100,32,32), "Lava", 10, None
	c3 = snow, Rect(50.0,150,32,32), "Snow Layer", 78, None
	c4 = ice, Rect(50.0,200,32,32), "Ice Block", 79, None
	c5 = mushroom_brown, Rect(50.0,250,32,32), "Mushroom (brown)", 39, None
	c6 = mushroom_red, Rect(50.0,300,32,32), "Mushroom (red)", 40, None
	c7 = tnt, Rect(150.0,50,32,32), "TNT", 46, 1
	c8 = cobweb, Rect(150.0,100,32,32), "Cobweb", 30, None
	c9 = bedrock, Rect(150.0,150,32,32), "Bedrock Block", 7, None
	c10 = bush, Rect(150.0,200,32,32), "Bush", 31, None
	c11 = grass, Rect(150.0,250,32,32), "Grass", 31, 1 
	c12 = none, Rect(150.0,300,32,32), "None", 0, None 
	choices = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
	faces = {1:"top",0:"bottom",4:"- ",5:"+ ",2:" -",3:" +"}
	
	# Set up the default selected block variable
	selected_image = Im("blank")
	selected_rect = Rect(70,417,32,32)
	selected_text, selected_code, selected_status = "None", 0, None
	
	# Set up the GUI loop
	while True:
		# Input events
		for event in pygame.event.get():
			# EXIT clicked
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# Mouse clicks
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				# Click a block icon
				for choice in choices:
					if choice[1].collidepoint(mouse_pos):
						# Set the selected block variables to the correct values
						selected_image = choice[0]
						selected_text = choice[2]
						selected_code = choice[3]
						selected_status = choice[4]
				
		# Detect if the mouse is hovering over a block icon
		mouse_pos = pygame.mouse.get_pos()
		display_text=""
		for choice in choices:
			# If so, set the display text to the block text
			if choice[1].collidepoint(mouse_pos):
				display_text = choice[2]
				
		# Render the GUI (background and buttons)
		windowSurface.fill(WHITE)
		windowSurface.blit(item_column, item_column_rect)
		windowSurface.blit(selected_image, selected_rect)
		# Render the GUI (block icons and display text)
		for i in range(11):
			windowSurface.blit(BACKGROUND_BLANK,Rect(50+100*((i-(i%6))/6),50*((i%6)+1),32,32))
			windowSurface.blit(choices[i][0],Rect(50+100*((i-(i%6))/6),50*((i%6)+1),32,32))
		windowSurface.blit(none, Rect(150,300,32,32))
		drawText(display_text,font,windowSurface, 50, 350)
		
		# Update the screen
		pygame.display.update()
		
		# If in a Minecraft Pi Edition world, allow the sword's right-click feature to place the selected block
		try:
			# Detect if a sword right-click has occurred
			blockEvent = mc.events.pollBlockHits()
			if blockEvent!=[]:
				# If so, detirmine the face of the hit and the coordinate of the block hit
				side = (faces[blockEvent[-1].face])
				X,Y,Z = blockEvent[-1].pos
				# Find which face the event occurred and place the new block on the correct side
				if side == "top":
					mc.setBlock(X,Y+1,Z,selected_code,selected_status)
				elif side == "bottom":
					mc.setBlock(X,Y-1,Z,selected_code,selected_status)
				elif side == "+ ":
					mc.setBlock(X+1,Y,Z,selected_code,selected_status)
				elif side == "- ":
					mc.setBlock(X-1,Y,Z,selected_code,selected_status)
				elif side == " +":
					mc.setBlock(X,Y,Z+1,selected_code,selected_status)
				elif side == " -":
					mc.setBlock(X,Y,Z-1,selected_code,selected_status)
		except:
			# No block hit event occurred
			pass

		mainClock.tick(200)

if __name__ == "__main__":
	PICRAFT()

