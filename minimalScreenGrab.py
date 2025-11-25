from psychopy import core, visual, event
import numpy as np
from scipy.io import savemat
import PIL.ImageOps

# Create window
myWin = visual.Window(
    size=[800, 600],
    units='height',
    color=0,
    fullscr=False
)

# Create a square stimulus
square = visual.Rect(
    myWin,
    width=0.2,
    height=0.2,
    fillColor=(1, 1, 1),
    pos=[0, 0]
)

# Animation parameters
nFrames = 30
startPos = -0.4
endPos = 0.4

wSize = np.append(myWin.size, nFrames)
imStack = np.empty(wSize, dtype=np.float32)

# Animate and capture frames
for frame in range(nFrames):
    # Calculate position (move horizontally)
    xPos = startPos + (endPos - startPos) * (frame / nFrames)
    square.pos = [xPos, 0]
    square.fillColor = -1 * square.fillColor
    # Draw stimulus
    myWin.clearBuffer()
    square.draw()

    # Capture frame
    # scale to -1 to 1
    movieFrame = PIL.ImageOps.grayscale(
        myWin.getMovieFrame(buffer='back'))
    movieFrameNumeric = np.sign(np.array(movieFrame) / 128.0 - 1.0)
    imStack[:, :, frame] = np.transpose(movieFrameNumeric)  # y,x

    filename = f"f_{frame:04d}"
    # myWin.saveMovieFrames(filename)
    # print(f"Saved {filename}")
    print(f"Grabbed {filename}")

    # flip after, as this operation clears back buffer
    # claude didn't get that order quite right
    myWin.flip()

    # Check for quit
    keys = event.getKeys()
    if 'escape' in keys or 'q' in keys:
        break

    # Small delay to see animation
    core.wait(0.016)  # ~60fps

savemat('minimalScreenGrab.mat', {'imStack': imStack})
print("save mat file")

# Cleanup
myWin.close()
core.quit()
