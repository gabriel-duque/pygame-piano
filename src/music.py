#!/usr/bin/env python3

import os
import sys
import time

import pygame.midi


def midi_device_prompt() -> int:
    '''Dump MIDI devices info and prompt user for a choice'''
    for i in range(0, pygame.midi.get_count()):
        (interf, name, inp, outp, opened) = pygame.midi.get_device_info(i)
        print(f'Device: {i}')
        print(f'\tInterface: {interf.decode("utf-8")}')
        print(f'\tName: {name.decode("utf-8")}')
        print(f'\tInput: {inp == 1}')
        print(f'\tOutput: {outp == 1}')
        print(f'\tOpened: {opened == 1}')
        print()

    return int(input("Which MIDI device would you like to use ? "))

def print_usage() -> None:
    '''Print our usage'''
    print(f'Usage: {os.path.basename(sys.argv[0])} [MIDI_DEVICE]')

def main() -> None:
    '''The main entrypoint for our program'''

    # Initialize the MIDI library
    pygame.midi.init()

    if (len(sys.argv) == 2):
        midi_dev = int(sys.argv[1])
    elif (len(sys.argv) == 1):
        midi_dev = midi_device_prompt()
    else:
        print_usage()
        sys.exit(os.EX_USAGE)

    # Create our MIDI handle
    print(f'Setting MIDI device to {midi_dev}')
    midi_hndl = pygame.midi.Output(midi_dev)

    midi_hndl.note_on(67, 124)
    time.sleep(1)
    midi_hndl.note_off(67, 124)

if __name__ == '__main__':
    main()
