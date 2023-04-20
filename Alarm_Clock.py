# Alarm Clock application

import PySimpleGUI as psg
import time
import winsound


def create_window():
    # Create the main window with two tabs: "Clock" and "Alarm"

    clock_layout = [
        [psg.VPush()],
        [psg.Text("", font=("Digital-7 Mono", 90), text_color="red", key="-TIME-")],
        [psg.VPush()]
    ]

    alarm_layout = [
        [psg.Text("HOUR", size=(9, 1)), psg.Text("MINUTE", size=(10, 1))],
        [psg.Input(key="-HR-", size=(10, 1)), psg.Input(key="-MIN-", size=(10, 1))],
        [psg.Text("", size=(40, 5), key="-ALARMS-LIST-")],
        [psg.Button("Confirm", button_color=("white", "black"), border_width=0),
         psg.Button("Stop", disabled=True, button_color=("white", "black"), border_width=0)]
    ]

    layout = [
        [psg.VPush()],
        [psg.Push(), psg.Image("close.png", pad=0, enable_events=True, key="-CLOSE-")],
        [psg.TabGroup([[
            psg.Tab("Clock", clock_layout, element_justification="center"),
            psg.Tab("Alarm", alarm_layout)
        ]])]
    ]

    return psg.Window(
        "Alarm Clock", layout, size=(500, 225),
        finalize=True,
        no_titlebar=True,
        grab_anywhere=True,
        element_justification='center')


def update_window(window, list_of_alarms):
    # Update the main window with the current time and the list of alarms

    now = time.strftime("%H:%M:%S")
    window["-TIME-"].update(now)

    window["-ALARMS-LIST-"].update("")
    for alarm in list_of_alarms:
        window["-ALARMS-LIST-"].update(window["-ALARMS-LIST-"].get() + alarm + '\t')


def play_alarm():
    # Play the alarm sound

    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)


def confirm_alarm(window, list_of_alarms, values):
    # Add a new alarm to the list

    hour_alarm = values["-HR-"]
    minute_alarm = values["-MIN-"]

    if hour_alarm and minute_alarm:
        list_of_alarms.append(f"{hour_alarm}:{minute_alarm}:00")

    update_window(window, list_of_alarms)


def stop_alarm(window, list_of_alarms):
    # Stop the currently playing alarm

    window["Stop"].update(disabled=True)
    list_of_alarms.pop(0)
    update_window(window, list_of_alarms)


def main():
    # Main function to run the alarm clock application

    psg.theme("black")
    window = create_window()
    list_of_alarms = []

    while True:
        event, values = window.read(timeout=10)
        if event in (psg.WIN_CLOSED, "-CLOSE-"):
            break

        update_window(window, list_of_alarms)

        if list_of_alarms:
            current_time = time.strftime("%H:%M:%S")
            if current_time == list_of_alarms[0]:
                play_alarm()
                window["Stop"].update(disabled=False)

        if event == "Confirm":
            confirm_alarm(window, list_of_alarms, values)

        if event == "Stop":
            stop_alarm(window, list_of_alarms)

    window.close()


if __name__ == "__main__":
    main()
