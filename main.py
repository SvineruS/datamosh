import subprocess

END_FRAME_HEX = b'00dc'
I_FRAME_HEX = b'\x00\x01\xb0'


repeat_p_frames = 2
fps = 25


def main(filename, effect_sec_list):
    # need avi
    subprocess.call(f'ffmpeg -loglevel error -y -i {filename} -r {fps} temp1.avi', shell=True)
    magic(effect_sec_list)
    subprocess.call(f'ffmpeg -loglevel error -y -i temp2.avi output.mp4', shell=True)


def magic(effect_sec_list):
    # dont copy I frames and multiply P frames in specified seconds
    with open('temp1.avi', 'rb') as in_file, open('temp2.avi', 'wb') as out_file:
        frames = split_file(in_file, END_FRAME_HEX)

        for index, frame in enumerate(frames):
            if not is_need_effect_here(index / fps, effect_sec_list):
                out_file.write(frame + END_FRAME_HEX)
                continue

            if not is_iframe(frame):
                out_file.write((frame + END_FRAME_HEX) * repeat_p_frames)


def split_file(fp, marker, blocksize=4096):
    buffer = b''
    for block in iter(lambda: fp.read(blocksize), b''):
        buffer += block
        while True:
            markerpos = buffer.find(marker)
            if markerpos == -1:
                break
            yield buffer[:markerpos]
            buffer = buffer[markerpos + len(marker):]
    yield buffer


def is_need_effect_here(curr_sec, effect_sec_list):
    return any(start < curr_sec < end for start, end in effect_sec_list)


def is_iframe(frame):
    return frame[5:8] == I_FRAME_HEX


if __name__ == "__main__":
    # example
    main(
        'input.mp4',   # input file name 
        [
            (1, 2.5),  # make effect on 1-2.5 seconds
            (6, 9)     # and 6-9 seconds of video
        ]
    )
