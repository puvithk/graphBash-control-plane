import platform
import time


START_TIME = time.time()


def system_health() -> dict:
    return {
        "status": "healthy",
    }


def system_info() -> dict:
    return {
        "hostname": platform.node(),
        "operating_system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
    }


def system_uptime() -> dict:
    return {
        "process_uptime_seconds": int(
            time.time() - START_TIME
        )
    }