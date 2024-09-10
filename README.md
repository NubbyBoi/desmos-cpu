# Desmos CPU

Well gosh darn, it's a CPU in the hit graphing calculator [Desmos](https://www.desmos.com/calculator)  
I made this because I got bored, don't expect much  
Use `assembler.py` to assemble programs to run on it  
Here's a [link](https://www.desmos.com/calculator/ilnyyv3m0e) to the actual project  
If it doesn't work, make a formal complaint  

## The Assembly Language

Mainly the `assembler.py` assembles programs written in [this specification](/instruction_set.png) which I took from AQA but there's a couple extra bits too  
1. As well as `ADD` and `SUB`, there's also shiny new `MUL` and `DIV` for multiplication and division, respectively
2. It is recommended to write all instructions in an ASM program indented by 8 spaces (or 1 equivalent tab) to make space for labels
3. Entry point is at the `main` label, as seen in `demo1.asm` and `demo2.asm`
4. Yeah have fun (this will be worse for you than it was for me)
5. I claim to have added support for comments and blank lines. I have not. Deal with it.
