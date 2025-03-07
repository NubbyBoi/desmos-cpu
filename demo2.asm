main:	MOV R1 #2
	STR R1 #16
	MOV R2 #2
	MOV R3 #7
' your programs may contain blank lines, such as the one below:

loop:	LDR R1 #16
	MUL R1 R1 R2
	STR R1 #16
	MOV R1 #0
	SUB R3 R3 #1
	CMP R3 #0
	BGT loop
	HLT
