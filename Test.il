.assembly extern mscorlib {}

.assembly Test

{
	.ver 1:0:0:0
}
.module Test.exe

.method static void main() cil managed
{
	.maxstack 1
	.entrypoint

	.locals init([0] int32 j)
	ldc.i4 11
	stloc j
	ldloc j
	call void [mscorlib]System.Console::Write(int32)

	ret
}
.method public static int32 Factorial( int32 num ) cil managed
{
	.maxstack 5
	ldarg num
	ldc.i4 0
	ceq
	ldc.i4.0
	cgt
	brtrue.s LABEL3
	br LABEL4
	LABEL3:
	ldc.i4 1
	br LABEL5
	LABEL4:
	ldarg num
	ldc.i4 1
	sub
	call int32 Factorial(int32)
	ldarg num
	mul
	br LABEL5
	LABEL5:

	ret
}
