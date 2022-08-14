.assembly extern mscorlib {}

.assembly Game

{
	.ver 1:0:0:0
}
.module Game.exe

.method static void main() cil managed
{
	.maxstack 9
	.entrypoint

	.locals init([0] int32 p2,[1] int32 player2Wins,[2] int32 move,[3] int32 idx,[4] int32 numMoves,[5] int32[] playerOneMoves,[6] int32 gameFinished,[7] int32 player,[8] int32 p1,[9] string command,[10] int32[] playerTwoMoves,[11] int32 numDraws,[12] int32 player1Wins,[13] string xo)
	ldstr "Welcome to the Noughts and Crosses game!\n"
	call void [mscorlib]System.Console::Write(string)
	ldc.i4 0
	stloc player1Wins
	ldc.i4 0
	stloc player2Wins
	ldc.i4 0
	stloc numDraws
	ldstr "P"
	stloc command
	LABEL1:
	ldloc command
	ldstr "Q"
	call bool [mscorlib]System.String::op_Inequality(string,string)
	ldc.i4.0
	beq LABEL2
	ldstr "\nPress P-Play or Q-Quit\n"
	call void [mscorlib]System.Console::Write(string)
	call string [mscorlib]System.Console::ReadLine()
	stloc command
	ldloc command
	ldstr "P"
	call bool [mscorlib]System.String::op_Equality(string,string)
	brtrue.s LABEL7
	br LABEL8
	LABEL7:
	call void DisplayInitialBoard()
	ldc.i4 9
	newarr int32
	stloc playerOneMoves
	ldc.i4 9
	newarr int32
	stloc playerTwoMoves
	ldc.i4 0
	stloc gameFinished
	ldc.i4 1
	stloc player
	ldc.i4 0
	stloc numMoves
	LABEL10:
	ldloc gameFinished
	ldc.i4 0
	ceq
	ldc.i4.0
	beq LABEL11
	ldloc player
	call int32 AskForMove(int32)
	stloc move
	ldloc move
	call int32 MoveValid(int32)
	ldc.i4 0
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL16
	br LABEL17
	LABEL16:
	ldstr "\nMove "
	call void [mscorlib]System.Console::Write(string)
	ldloc move
	call void [mscorlib]System.Console::Write(int32)
	ldstr " not valid!\n"
	call void [mscorlib]System.Console::Write(string)
	br LABEL18
	LABEL17:
	ldloc playerTwoMoves
	ldloc move
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldloc move
	ldelem.i4
	ldc.i4 1
	ceq
	or
	ldc.i4.0
	cgt
	brtrue.s LABEL25
	br LABEL26
	LABEL25:
	ldstr "\nMove "
	call void [mscorlib]System.Console::Write(string)
	ldloc move
	call void [mscorlib]System.Console::Write(int32)
	ldstr " already taken!\n"
	call void [mscorlib]System.Console::Write(string)
	br LABEL27
	LABEL26:
	ldloc player
	ldc.i4 2
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL30
	br LABEL31
	LABEL30:
	ldloc playerTwoMoves
	ldloc move
	ldc.i4 1
	stelem.i4
	br LABEL32
	LABEL31:
	ldloc playerOneMoves
	ldloc move
	ldc.i4 1
	stelem.i4
	br LABEL32
	LABEL32:
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "0 |"
	call void [mscorlib]System.Console::Write(string)
	ldc.i4 0
	stloc idx
	LABEL33:
	ldloc idx
	ldc.i4 9
	clt
	ldc.i4.0
	beq LABEL34
	ldstr " "
	stloc xo
	ldloc playerOneMoves
	ldloc idx
	ldelem.i4
	stloc p1
	ldloc p1
	ldc.i4 1
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL39
	br LABEL40
	LABEL39:
	ldstr "X"
	stloc xo
	br LABEL41
	LABEL40:
	br LABEL41
	LABEL41:
	ldloc playerTwoMoves
	ldloc idx
	ldelem.i4
	stloc p2
	ldloc p2
	ldc.i4 1
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL44
	br LABEL45
	LABEL44:
	ldstr "0"
	stloc xo
	br LABEL46
	LABEL45:
	br LABEL46
	LABEL46:
	ldloc xo
	call void [mscorlib]System.Console::Write(string)
	ldstr " |"
	call void [mscorlib]System.Console::Write(string)
	ldloc idx
	ldc.i4 1
	add
	stloc idx
	ldloc idx
	ldc.i4 3
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL49
	br LABEL50
	LABEL49:
	ldstr " 2\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n3 |"
	call void [mscorlib]System.Console::Write(string)
	br LABEL51
	LABEL50:
	br LABEL51
	LABEL51:
	ldloc idx
	ldc.i4 6
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL54
	br LABEL55
	LABEL54:
	ldstr " 5\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n6 |"
	call void [mscorlib]System.Console::Write(string)
	br LABEL56
	LABEL55:
	br LABEL56
	LABEL56:
	br LABEL33
	LABEL34:
	ldstr " 8\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)
	ldloc playerOneMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 1
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 3
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 5
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 7
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 3
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 1
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 7
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 5
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerOneMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerOneMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerOneMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldc.i4.0
	cgt
	brtrue.s LABEL151
	br LABEL152
	LABEL151:
	ldc.i4 1
	stloc gameFinished
	ldloc player1Wins
	ldc.i4 1
	add
	stloc player1Wins
	ldstr "\nPlayer 1 WINS!"
	call void [mscorlib]System.Console::Write(string)
	br LABEL153
	LABEL152:
	br LABEL153
	LABEL153:
	ldloc playerTwoMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 1
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 3
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 5
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 7
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 3
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 1
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 7
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 5
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 0
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 8
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldloc playerTwoMoves
	ldc.i4 2
	ldelem.i4
	ldc.i4 1
	ceq
	ldloc playerTwoMoves
	ldc.i4 4
	ldelem.i4
	ldc.i4 1
	ceq
	and
	ldloc playerTwoMoves
	ldc.i4 6
	ldelem.i4
	ldc.i4 1
	ceq
	and
	or
	ldc.i4.0
	cgt
	brtrue.s LABEL248
	br LABEL249
	LABEL248:
	ldc.i4 1
	stloc gameFinished
	ldloc player2Wins
	ldc.i4 1
	add
	stloc player2Wins
	ldstr "\nPlayer 2 WINS!"
	call void [mscorlib]System.Console::Write(string)
	br LABEL250
	LABEL249:
	br LABEL250
	LABEL250:
	ldloc numMoves
	ldc.i4 8
	ceq
	ldloc gameFinished
	ldc.i4 0
	ceq
	and
	ldc.i4.0
	cgt
	brtrue.s LABEL257
	br LABEL258
	LABEL257:
	ldc.i4 1
	stloc gameFinished
	ldstr "\nThe game has ended in a DRAW!\n"
	call void [mscorlib]System.Console::Write(string)
	ldloc numDraws
	ldc.i4 1
	add
	stloc numDraws
	br LABEL259
	LABEL258:
	br LABEL259
	LABEL259:
	ldloc numMoves
	ldc.i4 1
	add
	stloc numMoves
	ldloc player
	ldc.i4 2
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL262
	br LABEL263
	LABEL262:
	ldc.i4 1
	stloc player
	br LABEL264
	LABEL263:
	ldc.i4 2
	stloc player
	br LABEL264
	LABEL264:
	br LABEL27
	LABEL27:
	br LABEL18
	LABEL18:
	br LABEL10
	LABEL11:
	ldstr "\n\nSTANDINGS\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "------------\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "DRAWS : "
	call void [mscorlib]System.Console::Write(string)
	ldloc numDraws
	call void [mscorlib]System.Console::Write(int32)
	ldstr "\nPLAYER 1 WINS : "
	call void [mscorlib]System.Console::Write(string)
	ldloc player1Wins
	call void [mscorlib]System.Console::Write(int32)
	ldstr "\nPLAYER 2 WINS : "
	call void [mscorlib]System.Console::Write(string)
	ldloc player2Wins
	call void [mscorlib]System.Console::Write(int32)
	ldstr "\n"
	call void [mscorlib]System.Console::Write(string)
	br LABEL9
	LABEL8:
	br LABEL9
	LABEL9:
	ldloc command
	ldstr "P"
	call bool [mscorlib]System.String::op_Inequality(string,string)
	ldloc command
	ldstr "Q"
	call bool [mscorlib]System.String::op_Inequality(string,string)
	and
	brtrue.s LABEL271
	br LABEL272
	LABEL271:
	ldstr "\nCommand not valid.\n"
	call void [mscorlib]System.Console::Write(string)
	br LABEL273
	LABEL272:
	br LABEL273
	LABEL273:
	br LABEL1
	LABEL2:
	ldstr "\nThank you for playing, see you again!"
	call void [mscorlib]System.Console::Write(string)

	ret
}
.method public static void DisplayInitialBoard(  ) cil managed
{
	.maxstack 1
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "  |0 |1 |2 |\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "  |3 |4 |5 |\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "  |6 |7 |8 |\n"
	call void [mscorlib]System.Console::Write(string)
	ldstr "   __ __ __\n"
	call void [mscorlib]System.Console::Write(string)

	ret
}
.method public static int32 AskForMove( int32 player ) cil managed
{
	.maxstack 1
	.locals init([0] int32 move)
	ldstr "\nPlayer "
	call void [mscorlib]System.Console::Write(string)
	ldarg player
	call void [mscorlib]System.Console::Write(int32)
	ldstr " please enter your move: eg. 5\n"
	call void [mscorlib]System.Console::Write(string)
	call string [mscorlib]System.Console::ReadLine()
	call int32 [mscorlib]System.Int32::Parse(string)
	stloc move
	ldloc move

	ret
}
.method public static int32 MoveValid( int32 move ) cil managed
{
	.maxstack 9
	ldarg move
	ldc.i4 0
	clt
	ldarg move
	ldc.i4 8
	cgt
	or
	ldc.i4.0
	cgt
	brtrue.s LABEL280
	br LABEL281
	LABEL280:
	ldc.i4 0
	br LABEL282
	LABEL281:
	ldc.i4 1
	br LABEL282
	LABEL282:

	ret
}
