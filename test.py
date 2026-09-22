import psutil

def get_ram_usage(pid):
    try:
        process = psutil.Process(pid)

        # RSS = physical RAM currently being used
        ram_bytes = process.memory_info().rss

        return {
            "bytes": ram_bytes,
            "mb": ram_bytes / (1024 ** 2),
            "gb": ram_bytes / (1024 ** 3),
            "percent": process.memory_percent()
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None