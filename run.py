#! /usr/bin/env python3
import os, sys
from subprocess import call
DEVNULL = open(os.devnull, "w")
commands = {"install": 0, "uninstall": 0, "compile": 0, "dump": 2}

if os.getuid() != 0:
    print("Can not run without root privileges!")
    sys.exit(1)
elif len(sys.argv) < 2:
    print("Usage:   run.py <command> [arguments]\nExample: run.py dump ./encrypted.sh.x ./decrypted.sh")
    sys.exit(1)

def cmd_install():
    if os.access("/bin/bash-shxdumper1", 0):
        if os.access("/bin/bash.bak", 0):
            print("Will not overwrite bash binary backup")
            sys.exit(1)
        os.rename("/bin/bash", "/bin/bash.bak")
        os.rename("/bin/bash-shxdumper1", "/bin/bash")
        return True
    else:
        result = cmd_compile()
        if result:
            return cmd_install()
        else:
            return result

def cmd_uninstall():
    os.rename("/bin/bash", "/bin/bash-shxdumper1")
    os.rename("/bin/bash.bak", "/bin/bash")
    return True

def cmd_compile():
    pullsource = not os.access("./thisisshxdumper", 0)
    if pullsource:
        oldcwd = os.getcwd()
        os.chdir("/tmp")
        print("\nPulling source code...")
        call(["rm", "-rf", "shxdumper"])
        r = call(["git", "clone", "https://github.com/niansa/bash-shxdumper", "shxdumper"])
        if r != 0: return False
        os.chdir("shxdumper")
    print("\nGenerating makefile...")
    r = call(["./configure"])
    if r != 0: return False
    print("\nCompiling source code...")
    call(["make", "-j", str(os.cpu_count())])
    print("\nAdding compiled binary to system...")
    os.rename("./bash", "/bin/bash-shxdumper1")
    if pullsource:
        print("\nCleaning up environment...")
        os.chdir("..")
        call(["rm", "-rf", "shxdumper"])
        os.chdir(oldcwd)
    return True

def cmd_dump(secondtry=False):
    finput = sys.argv[2]
    foutput = sys.argv[3]
    if os.access(foutput, 0):
        print(foutput+": Already exists")
        sys.exit(1)
    extraargs = sys.argv[3:]
    extraargs.pop()
    os.environ["OUTFILE"] = foutput
    r = call(["timeout", "1s", finput] + extraargs, stdout=DEVNULL)
    if not os.access(foutput, 0):
        if secondtry:
            return False
        else:
            if cmd_install():
                r1 = cmd_dump(secondtry=True)
                r2 = cmd_uninstall()
                return r1 and r2
            else:
                return False
    else:
        if r == 0 or r == 124:
            print("\nDecryption very likely succeded!")
        else:
            print("\nDecryption likely succeded!")
        return True



if sys.argv[1] in commands.keys():
    if len(sys.argv) < 2 + commands[sys.argv[1]]:
        print(f"{sys.argv[1]} requires at least {commands[sys.argv[1]]} argument(s)")
        sys.exit(1)
    r = eval(f"cmd_{sys.argv[1]}()")
    if not r:
        print("An error has occured. See above messages for more informations.")
        sys.exit(1)
    else:
        sys.exit(0)
