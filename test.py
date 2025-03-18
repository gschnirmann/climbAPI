GRADE_CONVERSION = {
    "FR": {
        "5": {"BR": "IV", "US": "5.7"},
        "5+": {"BR": "V", "US": "5.8"},
        "6a": {"BR": "Vsup", "US": "5.9"},
        "6a+": {"BR": "VI", "US": "5.10a"},
        "6b": {"BR": "VI+", "US": "5.10b"},
        "6b+": {"BR": "VI+", "US": "5.10c/d"},
        "6c": {"BR": "VIIa", "US": "5.11a"},
        "6c+": {"BR": "VIIb", "US": "5.11b"},
        "7a": {"BR": "VIIc", "US": "5.11c/d"},
        "7a+": {"BR": "VIIIa", "US": "5.12a"},
        "7b": {"BR": "VIIIb", "US": "5.12b"},
        "7b+": {"BR": "VIIIc", "US": "5.12c/d"},
        "7c": {"BR": "IXa", "US": "5.13a"},
        "7c+": {"BR": "IXb", "US": "5.13b"},
        "8a": {"BR": "IXc", "US": "5.13c"},
        # Adicione mais graus conforme necessário
    }
}

for v in GRADE_CONVERSION["FR"].values():
    print(v["BR"])