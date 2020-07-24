import subprocess

END_FRAME_HEX = bytes.fromhex('30306463')
I_FRAME_HEX = bytes.fromhex('0001B0')


repeat_p_frames = 2
fps = 25


def main(start_effect_sec, end_effect_sec):
    subprocess.call(f'ffmpeg -loglevel error -y -i input.mp4  -crf 0 -r {fps} -g 2000000 temp1.avi', shell=True)
    magic(start_effect_sec, end_effect_sec)
    subprocess.call(f'ffmpeg -loglevel error -y -i temp2.avi  -crf 18 -vcodec libx264 output.mp4', shell=True)


def magic(start_effect_sec, end_effect_sec):
    # todo stream
    in_file = open('temp1.avi', 'rb')
    out_file = open('temp2.avi', 'wb')

    frames = in_file.read().split(END_FRAME_HEX)

    for index, frame in enumerate(frames):
        out_file.write(frame + END_FRAME_HEX)
        if start_effect_sec < index / fps < end_effect_sec:
            if frame[5:8] != I_FRAME_HEX:
                for i in range(repeat_p_frames):
                    out_file.write(frame + END_FRAME_HEX)

    in_file.close()
    out_file.close()
