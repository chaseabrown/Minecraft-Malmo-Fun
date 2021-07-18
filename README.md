# Minecraft-Malmo-Fun
The point of this project was to learn. Not specific goal in mind, just reading research papers and playing around with the ideas.

## Data Manipulation / Visualization

**readBlockData.py** was an attempt to visualize the data given from blocks in a radius around the player. At each frame, the agent returns a 1 dimentional array of blocks in a 3D space. In order to put this into a format I could understand, I reshaped the array (in an overly complicated way looking back) and ordered it in a 3 dimentional way. I then plotted each point and scraped a website that had images of all the blocks. When I plotted each block, I used the average RBG value to color the point so I could recognize things better.

![Block Plot](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/blockPlot.png "Block Plot")

After I had this, I was ready to move onto the viewing frustrum issue. After brushing up on the math and finding something that worked with the variables I had, I successfully going the viewing frustrum to match up with the blocks the agent could actually see.

![Viewing Frustrum](https://github.com/chaseabrown/Minecraft-Malmo-Fun/blob/main/frustrum.png "Viewing Frustrum")

Also fun to note that the plot was interactive in a web browser.


