from pynput import keyboard
import PySimpleGUI as simpleGui
import time
import threading


def get_word_count():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    listener.join()


def on_release(key):
    if key == keyboard.Key.esc:
        window.write_event_value('CLOSE', True)
        return False  # stop listener

    letter_times.append(time.time())
    if letter_times.__len__() > 15:
        letter_times.pop(0)
    if letter_times.__len__() > 1:
        wpm = (letter_times.__len__() / (letter_times[letter_times.__len__() - 1] - letter_times[0])) / 5 * 60
        window.write_event_value('WORD', int(wpm + .5))


if __name__ == '__main__':
    start_time = time.time()
    letter_times = []
    threading.Thread(target=get_word_count, daemon=True).start()

    simpleGui.ChangeLookAndFeel('Black')
    simpleGui.SetOptions(element_padding=(0, 0))

    layout = [[simpleGui.Text('')],
              [simpleGui.Text(size=(4, 1), font=('Helvetica', 20), justification='center', key='text')],
              [simpleGui.Text('')]]

    window = simpleGui.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                              grab_anywhere=True)

    while True:
        event, values = window.read()

        if event == simpleGui.WIN_CLOSED:
            break
        elif event == 'WORD':
            count = values[event]
            window['text'].update(str(count))
        elif event == "CLOSE":
            window.close()
    window.close()
