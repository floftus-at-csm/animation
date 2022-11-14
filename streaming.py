import streamlink
import argparse
# from cv2 import VideoCapture
import cv2
import pafy
from pytube import YouTube
import vlc 

def stream_to_url(url, quality='best'):
    streams = streamlink.streams(url)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No steams were available")

def main(url, sub_method, quality='best', fps=30.0):
    stream_url = stream_to_url(url, quality)
    cap = cv2.VideoCapture(stream_url)

    frame_time = int((1.0 / fps) * 1000.0)

    print(cap)
    counter = 0
    while True:
        try:
            ret, frame = cap.read()
            # cv2.imshow("video", frame)
            if(counter == 1):
                backg = frame
            else if counter > 1:
                cv::Mat diffImage;
                cv::absdiff(frame, background, diffImage)
            # fgMask = backSub.apply(frame, 1.0) # this is changing the background every loop
            fgMask = backSub.apply(frame, 0.000005)
            print(backSub.getHistory())
            if counter % 1000 == 0:
                frameval = "content/armchair_test/" + str(int(counter/100)) + ".png"
                bgval = "content/armchair_test/background" + str(int(counter/100)) + ".png"
                cv2.imwrite(frameval, fgMask)
                background = backSub.getBackgroundImage()
                cv2.imwrite(bgval, background)
            # break
            counter = counter + 1

        except:
            print("error")
            break


# if __name__ == "__main__":
#     main("https://www.youtube.com/watch?v=utFHRDryJL0")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by OpenCV. You can process both videos and images.')
    parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
    parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
    args = parser.parse_args()
    if args.algo == 'MOG2':
        backSub = cv2.createBackgroundSubtractorMOG2()
    else:
        backSub = cv2.createBackgroundSubtractorKNN()
    
    # url = "https://www.youtube.com/watch?v=utFHRDryJL0"
    url = args.input
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    print(playurl)
    main(playurl, backSub)

    # Instance = vlc.Instance()
    # player = Instance.media_player_new()
    # Media = Instance.media_new(playurl)
    # Media.get_mrl()
    # player.set_media(Media)
    # player.play()