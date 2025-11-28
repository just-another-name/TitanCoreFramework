#!/usr/bin/env python3
import sys
from app.Console.Kernel import Kernel

def main():
    args = sys.argv[1:]  # Получаем все аргументы командной строки
    if not args:
        print("Available commands:")
        kernel = Kernel()
        for signature, cmd in kernel.commands.items():
            print(f"  {signature.ljust(20)}")
        return
    
    command = args[0]
    kernel = Kernel()
    # Передаем все оставшиеся аргументы
    sys.exit(kernel.run(command, args[1:]))

if __name__ == "__main__":
    main()