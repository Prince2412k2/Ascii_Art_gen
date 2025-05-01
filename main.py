import shutil
import curses
import cv2

import logging

logging.basicConfig(filename="debug.log", level=logging.INFO)
logger = logging.getLogger()

string = " .,-:;i|=+%O#@B8&$@#^*"


def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines


def ascii(stdscr, img):
    height, width = stdscr.getmaxyx()
    y_sample, x_sample = img.shape[0] // height, img.shape[1] // width
    max_brightness = x_sample * y_sample * 255  # Max possible brightness value
    for y in range(height):
        for x in range(width):
            ys = y * y_sample
            ye = ys + y_sample
            xs = x * x_sample
            xe = xs + x_sample
            patch = img[ys:ye, xs:xe]
            patch_sum = patch.sum()
            fout = int(
                patch_sum / max_brightness * len(string)
            )  # Normalize and map to string index
            if fout > len(string) - 1 // 2:
                fout += 1
            else:
                fout -= 1
            fout = min(fout, len(string) - 1)  # Ensure we don't go out of bounds
            char = string[fout]  # Get the ASCII character
            try:
                stdscr.addstr(y, x, char)  # Print character at the correct position
            except Exception as e:
                logger.warning(
                    f"Failed at ({x},{y}) with fout={fout}, char={repr(char)}: {e}"
                )


def main(stdscr) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stdscr.erase()
        ascii(stdscr, gray)
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    curses.wrapper(main)
    # test()
