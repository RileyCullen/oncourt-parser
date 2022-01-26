import time, sys

def update_progress(progress: float, barLength = 10):
    """
    This function is responsible for displaying and updating a console progress
    bar. Note that this code was adapted from Brian Khuu's code found here:
    https://stackoverflow.com/questions/3160699/python-progress-bar.

    Typical usage in a for loop is as follows (let N be some integer value):
    for i in range(N):
        update_progress(i/(N-1))

    Preconditions:
    --------------
    This function assumes that progress is a float or int value and no other 
    type.

    Parameters:
    -----------
    progress:  A float representing the progress made towards completing a task.
    barLength: The length of the console progress bar.
    """
    status = ""
    if (isinstance(progress, int)):
        progress = float(progress)
    if (progress < 0):
        progress = 0
        status = "Halt...\r\n"
    if (progress >= 1):
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()