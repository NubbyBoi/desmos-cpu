# Desmos CPU

Well gosh darn, it's a CPU in the hit graphing calculator [Desmos](https://www.desmos.com/calculator)  
I made this because I got bored, don't expect much  
Use `assembler.py` to assemble programs to run on it  
Here's a [link](https://www.desmos.com/calculator/jbaqljhrrt) to the actual project  
If it doesn't work, make a formal complaint  

## The Assembly Language

Mainly the `assembler.py` assembles programs written in [this specification](/instruction_set.png) which I took from [AQA](https://www.aqa.org.uk)'s A-level computer science course but there's a couple extra bits too  
1. As well as `ADD` and `SUB`, there's also shiny new `MUL` and `DIV` for multiplication and division, respectively
2. It is recommended to write all instructions in an ASM program indented by 8 spaces (or 1 equivalent tab) to make space for labels
3. Entry point is at the `main` label, as seen in `demo1.asm` and `demo2.asm`
4. I think comments and blank lines actually work, as seen in `demo1.asm` and `demo2.asm`

## I/O Convention

- Programs should expect inputs to be at the start of RAM
- Programs should output to the start of RAM
- By "the start of RAM", I mean the lowest addresses in ascending order
- For example, a program with 3 inputs should expect them at addresses 1, 2 and 3 of RAM
- Outputs may overwrite inputs in order to properly be at the start of RAM
- Alternatively, outputs may begin immediately after inputs
