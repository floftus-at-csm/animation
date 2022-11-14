import streamlink

from cv2 import VideoCapture

def stream_to_url(url, quality='best'):
    streams = streamlink.streams(url)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No steams were available")

def main(url, quality='best', fps=30.0):
    stream_url = stream_to_url(url, quality)
    cap = VideoCapture(stream_url)

    frame_time = int((1.0 / fps) * 1000.0)

    while True:
        try:
            ret, frame = cap.read()
        except:
            print("error")


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=utFHRDryJL0")