import sys


def get_processes() -> set:
    if sys.platform == "win32":
        import wmi

        return {p.Name for p in wmi.WMI().Win32_Process()}

    raise NotImplementedError(
        f'Fetching processes is not implemented for platform "{sys.platform}"'
    )
