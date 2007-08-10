
This is the turcanator. It's a little program
for helping people learn to play the piano.
It takes a midi file, shows a piano roll and
gives you visual feedback as to whether or not
you're playing the notes correctly.


The main code is (c) 2006 Michal J Wallace.
License: BSD style.

Requirements:

  python 2.4
  pygame
  python midi module (included)
  pypm module for win32 (included)
  pyrex is needed if you want to recompile CoreMidi

Usage:

  turcanator.py [filename.mid]

  You should probably use really short, one-voice
  midi files. :)

Instructions:
 
   It's a piano roll.

   Dark blue stripes are the notes to play.

   Hook up your midi keyboard and play those
   keys. (Only works on mac so far.)

   Mis-hit keys will show up red. 

   Correctly hit keys turn green.

   The white bar going across is the current
   goal. When all the keys match, you move
   to the next line.

   You can move the white bar up and down
   with the arrow keys and pgup/pgdown.

   The orange bar on the left shows the
   section to practice on. Press [ to set
   the start and ] to set the end.

   When you reach the end of the section,
   you loop back to the start.

   Space moves you back to the start too.

   Press p to play the section.
       It's slow. Tempo is currently hard coded.
       Maybe you'll fix this? :)


Goals / Help Wanted:

   The code is a mess. 100% ad hockery.

   Win32 Midi input? (should be trivial with pypm.)

   I want to ditch pygame for wxpython.
       For scrolling, menus, etc.

       The plan was/is:
           make pygame backend for sping 
               http://sping.sf.net
               I now run the sping project. Help wanted. :)
           port to sping.pygame
           switch to sping.WX backend
   
   Clean up drawing for longer notes.

   In wxpython:

       Add slider for tempo.

       Add scrolling.

       Add load menu.

   Load tempo from the midi file.

   Add another across-bar showing the "player".
   The ideas is it would play and you try to 
   keep up with it.
   
   Add a metronome.

   Pause a few beats before starting the
   playback, so there's time to switch from
   computer to keyboard.

   Allow recording/editing/sequencing midi files. :)
