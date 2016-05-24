class PEDACmd_Extend:
    def pdisasret(self, *arg):
        """
        Format output of gdb disassemble command(until "ret") with colors
        """
        (address, ) = normalize_argv(arg, 1)
        for i in range(0x1000):
            code = peda.get_disasm(address, i)
            if code[-3:] == 'ret' or code[-3:] == 'hlt':
                msg(format_disasm_code(code))
                break
        return

class PEDA_Override:
    def read_int(self, address, intsize=None):
        """
        Read an interger value from memory

        Args:
            - address: address to read (Int)
            - intsize: force read size (Int)

        Returns:
            - mem value (Int)
        """
        if not intsize:
            intsize = self.intsize()
        value = self.readmem(address, intsize)
        if value:
            # patch for python 3
            # value = to_int("0x" + codecs.encode(value[::-1], 'hex'))
            value = int.from_bytes(value, "little")
            return value
        else:
            return None

    def write_int(self, address, value, intsize=None):
        """
        Write an interger value to memory

        Args:
            - address: address to read (Int)
            - value: int to write to (Int)
            - intsize: force write size (Int)

        Returns:
            - Bool
        """
        if not intsize:
            intsize = self.intsize()
        # patch for python 3
        # buf = hex2str(value, intsize).ljust(intsize, "\x00")[:intsize]
        buf = value.to_bytes(intsize, "little")
        saved = self.readmem(address, intsize)
        if not saved:
            return False

        ret = self.writemem(address, buf)
        if ret != intsize:
            self.writemem(address, saved)
            return False
        return True

    def getpid(self):
        """
        Get PID of the debugged process
        Returns:
            - pid (Int)
        """

        out = None
        status = self.get_status()
        if not status or status == "STOPPED":
            return None

        if self.is_target_remote(): # remote target
            ctx = config.Option.get("context")
            config.Option.set("context", None)
            try:
                out = self.execute_redirect("call getpid()")
            except:
                pass

            config.Option.set("context", ctx)

            if out is None:
                #return None
                None
            else:
                out = self.execute_redirect("print $")
                if out:
                    return to_int(out.split("=")[1])
                else:
                    return None

        pid = gdb.selected_inferior().pid
        return int(pid) if pid else None

# Add to PEDA
for cmd in [c for c in dir(PEDACmd_Extend) if callable(getattr(PEDACmd_Extend, c)) and not c.startswith("_")]:
    pedacmd.commands.append(cmd)
    setattr(PEDACmd, cmd, getattr(PEDACmd_Extend, cmd))
    func = getattr(pedacmd, cmd)
    func.__func__.__doc__ = func.__doc__.replace("MYNAME", cmd)
    if cmd not in ["help", "show", "set"]:
        Alias(cmd, "peda %s" % cmd, 0)

for cmd in [c for c in dir(PEDA_Override) if callable(getattr(PEDA_Override, c)) and not c.startswith("_")]:
    setattr(PEDA, cmd, getattr(PEDA_Override, cmd))
