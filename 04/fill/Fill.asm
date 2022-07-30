// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(start)
@24576
D=M
@j
M=0
@setwhite
D;JEQ
@i
M=0
(setblack)
@SCREEN
D=A
@i
D=D+M
@24576
D=A-D
@start
D;JLE
@SCREEN
D=A
@i
A=M+D
M=-1
@i
M=M+1
@setblack
0;JMP
(setwhite)
@SCREEN
D=A
@j
D=D+M
@24576
D=A-D
@start
D;JLE
@SCREEN
D=A
@j
A=M+D
M=0
@j
M=M+1
@setwhite
0;JMP

