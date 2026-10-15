import sys, os
pid = sys.argv[1]
rem = os.path.getsize("/tmp/inject.bin")
tpl = open("/tmp/gdb_inject2.txt").read()
tpl = tpl.replace("PIDHERE", pid).replace("REMHERE", str(rem))
open("/tmp/gdb_f.txt","w").write(tpl)
print("сгенерирован, rem =", rem)
