import matplotlib
import matplotlib.pyplot as plt
# %matplotlib qt # for process_stream

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

def process_stream(path, process_frame, interval=1):
    '''
    Process and display a video stream at @param path using @param process_frame function.
    The @param interval specifies the interval at which the frame to be processed.

    Usage:
    count = 0
    def save_frame(img):
        global count
        count += 1
        cv2.imwrite('data/eq/#.jpg'.replace('#', str(count)), img)
        return img
    process_stream(path='sample.mp4', process_frame=save_frame, interval=10)
    '''
    cap = cv2.VideoCapture(path)
    counter = 1
    while(True):
        ret,frame = cap.read()
        if ret is True and counter % interval == 0:
            frame = process_frame(frame)
            cv2.imshow('frame',frame)
        counter += 1
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()