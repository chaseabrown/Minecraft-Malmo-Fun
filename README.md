# Minecraft-Malmo-Fun
The point of this project was to learn. Not specific goal in mind, just reading research papers and playing around with the ideas.

## Data Manipulation / Visualization

**readBlockData.py** was an attempt to visualize the data given from blocks in a radius around the player. At each frame, the agent returns a 1 dimentional array of blocks in a 3D space. In order to put this into a format I could understand, I reshaped the array (in an overly complicated way looking back) and ordered it in a 3 dimentional way. I then plotted each point and scraped a website that had images of all the blocks. When I plotted each block, I used the average RBG value to color the point so I could recognize things better.

![Block Plot](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/blockPlot.png "Block Plot")

After I had this, I was ready to move onto the viewing frustrum issue. After brushing up on the math and finding something that worked with the variables I had, I successfully going the viewing frustrum to match up with the blocks the agent could actually see.

![Viewing Frustrum](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/frustrum.png "Viewing Frustrum")

Also fun to note that the plot was interactive in a web browser. The interactive.mov file demonstrates this a little bit.

## Frame Storage and Processing

**processFrame.py** is the script that I used to breakdown and store the huge amount of data obtained from every frame. This involved dealing with databases, video and image files, depth maps / point clouds, and this is also where I ran tests for edge detection in the next section. Not exciting stuff, but good practice. In order to view the data from each frame, I found an HTML dashboard theme and connected the data streams to that for easy, one stop viewing.

![Dashboard](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/dashboard.png "Dashboard")


## Edge Detection

After I got done with frames, I needed a way to work with image files. When I started this, I was hoping to connect this to the block data from before so I could use an image recognition algorithm to have the actor see blocks, classify them, and store the seen blocks in memory. I stopped playing with this project before it got there, but I still got some fun images from finding edges and surfaces.

![Edge Detection](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/Edge%20detection.png "Edge Detection")

![Edge Detection](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/Edgedetection2.png "Edge Detection")

After getting here, I got excited and started testing out a bunch of different combinations of edge/surface detection algorithms. The agent was given a colormap, RGB image, and depth map for each frame and I used different combinations of those to get these.

![Multiple Views](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/multipleViews1.png "Multiple Views")

![Multiple Views](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/multipleViews2.png "Multiple Views")

![Multiple Views](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/multipleViews3.png "Multiple Views")

This one was my favorite and was even my desktop background for awhile.

![Neat](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/neat.png "Neat")

If you want to see a video of this with movement, the file is edgedetection.mp4 in this repo.

## Extra Tools Made

I got tired of looking at image files and then going to try and find the depth at that point, so I built a quick tool that lets me look at an image, then click a point and see the depths around that point. Short scripts and pretty basic stuff, but handy.

That tool is ./tools/imageViewer.py

