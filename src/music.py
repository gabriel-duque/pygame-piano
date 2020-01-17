#!/usr/bin/env python3

import os
import sys

# Hide welcome message from pygame when importing (seriously, who does that?)
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.midi


# This is the key mapping for our 'piano' is you use another keymap than qwerty
# you might want to change some keys.
# I have annotated the changes to make for the azerty keymap
key_to_note = {
        # pygame_key_id: (pitch, black, on)

        # pygame_key_id: pygame's internal constant to represent a key
        # pitch: the pitch of this note (on the octave 0)
        # black: a boolean to know if the key is black or white
        # on: a boolean to keep track of if this note is on

        # 24 is the pitch for the first C on a piano keyboard (C0)
        pygame.K_a: (24, False, False), # C0       (azerty: pygame.K_q)
        pygame.K_w: (25, True,  False), # C#/Db0   (azerty: pygame.K_z)
        pygame.K_s: (26, False, False), # D0
        pygame.K_e: (27, False, False), # D#/Eb0
        pygame.K_d: (28, True,  False), # E0
        pygame.K_f: (29, False, False), # F0
        pygame.K_t: (30, True,  False), # F#/Gb0
        pygame.K_g: (31, False, False), # G0
        pygame.K_y: (32, False, False), # G#/Ab0
        pygame.K_h: (33, True,  False), # A0
        pygame.K_u: (34, False, False), # A#/Bb0
        pygame.K_j: (35, True,  False), # B0
}

# The number of different notes in an octave
note_count = 12

# The octave we're playing in
octave = 4

# The default velocity (volume)
velocity = 124

def midi_device_prompt() -> int:
    '''Dump MIDI devices info and prompt user for a choice'''
    for i in range(0, pygame.midi.get_count()):
        (interf, name, inp, outp, opened) = pygame.midi.get_device_info(i)
        print(f'Device: {i}')
        print(f'\tInterface: {interf.decode("utf-8")}')
        print(f'\tName: {name.decode("utf-8")}')
        print(f'\tInput: {inp == 1}')
        print(f'\tOutput: {outp == 1}')
        print(f'\tOpened: {opened == 1}\n')

    return int(input("Which MIDI device would you like to use ? "))

def main() -> None:
    '''The main entrypoint for our program'''

    # Initialize the pygame MIDI module
    pygame.midi.init()

    # Parse arguments
    if (len(sys.argv) == 2):
        midi_dev = int(sys.argv[1])
    elif (len(sys.argv) == 1):
        midi_dev = midi_device_prompt()
    else:
        print(f'Usage: {os.path.basename(sys.argv[0])} [MIDI_DEVICE]')
        sys.exit(os.EX_USAGE)

    # Initialize the display
    pygame.display.init()
    pygame.display.set_caption('Girls can code (and play music)!')
    # XXX: actually set size of window and display initial keyboard
    pygame.display.set_mode((190, 1))

    # We only want to get events for our keyboard
    # Let's disable the others for performance
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.KEYDOWN)

    # Create our MIDI handle
    print(f'Setting MIDI device to {midi_dev}')
    midi_hndl = pygame.midi.Output(midi_dev)

    # Our main loop which gets pressed keys, plays or stops notes and updates the display
    go_on = True
    while go_on:
        for event in pygame.event.get():

            # Turn note on if known key
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in key_to_note:
                    note, black, on = key_to_note[key]
                    if not on:
                        # XXX: fix 'bug' in midi_to_ansi_note
                        print(f'DOWN: Key: {key} Note: {note + note_count * octave} ', end='')
                        print(f'Name: {pygame.midi.midi_to_ansi_note(note + note_count * octave)}')
                        midi_hndl.note_on(note + note_count * octave, velocity)
                        key_to_note[key] = note, black, True

                # Exit is user pressed <escape>
                elif key == pygame.K_ESCAPE:
                    go_on = False

            # Turn note off if known key
            elif event.type == pygame.KEYUP:
                key = event.key
                if key in key_to_note:
                    note, black, on = key_to_note[key]
                    if on:
                        # XXX: fix 'bug' in midi_to_ansi_note
                        print(f'UP: Key: {key} Note: {note + note_count * octave} ', end='')
                        print(f'Name: {pygame.midi.midi_to_ansi_note(note + note_count * octave)}')
                        midi_hndl.note_off(note + note_count * octave, velocity)
                        key_to_note[key] = note, black, False

        # XXX: Update our screen to show which keys are pressed

if __name__ == '__main__':
    main()
