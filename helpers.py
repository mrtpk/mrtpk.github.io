import matplotlib
import matplotlib.pyplot as plt

def plot(imgs, labels=None, cmap='gray', figsize=(20,10), fontsize=30):
    '''
    Displays images and labels in a plot.
    Usage:
    The input imgs should be in the format "[[img]]""
    '''
    nrows, ncols = len(imgs), len(imgs[0])
    if nrows > 100 or ncols > 50:
        print("Uh-oh, cannot plot these many images")
        return None
    f, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    if nrows == 1 or ncols == 1:
        axes = [axes]
    if nrows == 1 and ncols == 1:
        axes = [axes]
    for i in range(0, nrows):
        for j in range(0, ncols):
            try:
                axes[i][j].imshow(imgs[i][j], cmap=cmap)
                if labels is not None:
                    axes[i][j].set_title(labels[i][j], fontsize=fontsize)
            except IndexError as err:
                continue
    return axes