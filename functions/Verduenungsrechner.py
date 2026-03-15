from datetime import datetime
import pytz

def verduennungsrechner(C1, C2, V2):

    V1 = (C2 * V2) / C1

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "C1": C1,
        "C2": C2,
        "V2": V2,
        "V1": round(V1, 2)
    }