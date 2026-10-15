import sys
pid = sys.argv[1]
tpl = open("/tmp/gdb_splice.txt").read()
tpl = tpl.replace("PIDHERE", pid).replace("SWITCHAT", "6531")
open("/tmp/gdb_f.txt","w").write(tpl)
print("склейка на 6531 (InstSettings)")
