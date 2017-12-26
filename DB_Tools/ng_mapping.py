
NG_terminal_map = {
    "BACTON BBL": "Bacton IP",
    "BACTON IC": "Bacton IP",
    "BACTON PERENCO": "Bacton UKCS",
    "BACTON SEAL": "Bacton UKCS",
    "BACTON SHELL": "Bacton UKCS",
    "ST FERGUS MOBIL": "St Fergus",
    "ST FERGUS NSMP": "St Fergus",
    "ST FERGUS SHELL": "St Fergus",
    "TEESSIDE PX": "Teesside",
    "TEESSIDE BP": "Teesside",
    "ALDBROUGH": "Medium Range Storage",
    "HILLTOP": "Medium Range Storage",
    "HOLE HOUSE FARM": "Medium Range Storage",
    "HOLFORD": "Medium Range Storage",
    "HORNSEA": "Medium Range Storage",
    "STUBLACH": "Medium Range Storage",
    "GRAIN NTS 1": "Isle of Grain",
    "GRAIN NTS 2": "Isle of Grain",
    "EASINGTON DIMLINGTON": "Easington",
    "EASINGTON LANGELED": "Easington",
    "AVONMOUTH": "LNG Storage",
    "GLENMAVIS": "LNG Storage",
    "DYNEVOR ARMS": "LNG Storage",
    "PARTINGTON": "LNG Storage",
    "MILFORD HAVEN - SOUTH HOOK": "Milford Haven",
    "MILFORD HAVEN - DRAGON": "Milford Haven",
    "THEDDLETHORPE": "Theddlethorpe",
    "BARROW SOUTH": "Barrow",
    "EASINGTON ROUGH": "Rough Storage"
}

GTS_terminal_map = {
    'BOCHOLTZ TENP (OGE - FLX TENP)' : 'Bocholtz',
    'BOCHOLTZ VETSCHAU (THYSSENGAS)': 'Bocholtz',
    'DINXPERLO (BEW)': 'Other (DE)',
    'EMDEN EPT (GASSCO)': 'Emden',
    'EMDEN NPT (GASSCO)': 'Emden',
    'HAANRADE (THYSSENGAS)': 'Other (DE)',
    'HILVARENBEEK (FLUXYS)': 'Belgium',
    'JULIANADORP (BBL)': 'BBL',
    'OUDE STATENZIJL (GASCADE-H)': 'Oude Statenzijl',
    'OUDE STATENZIJL (GTG NORD-G)': 'Oude Statenzijl',
    'OUDE STATENZIJL (GUD-G)[OBEBG]': 'Oude Statenzijl',
    'OUDE STATENZIJL (GUD-H)[OBEBH]': 'Oude Statenzijl',
    'OUDE STATENZIJL (OGE)': 'Oude Statenzijl',
    'S-GRAVENVOEREN (FLUXYS)': 'Belgium',
    'TEGELEN (OGE)': 'Other (DE)',
    'VLIEGHUIS (RWE)': 'Other (DE)',
    'WINTERSWIJK (OGE)': 'Other (DE)',
    'ZANDVLIET (FLUXYS-H)': 'Belgium',
    'ZELZATE (FLUXYS)': 'Belgium',
    'ZEVENAAR': 'Other (DE)'
}


class Pipeline:

    def __init__(self, name, val, t):
        self.pipelineName = name
        self.flowValue = val
        self.timestamp = t

    def to_json(self):
        return {"pipelineName": self.pipelineName,
                "flowValue": self.flowValue,
                "timestamp": self.timestamp
                }


class Terminal:

    def __init__(self, name):
        self.terminalName = name
        self.terminalFlow = 0.0
        self.pipelines = []

    def add_pipeline(self, p):
        self.pipelines.append(p)

    def to_json(self):
        for p in self.pipelines:
            self.terminalFlow += p.flowValue

        return {"terminalName": self.terminalName,
                "terminalFlow": self.terminalFlow,
                "terminalTimestamp": self.pipelines[0].timestamp,
                "pipelines": [p.to_json() for p in self.pipelines]
                }
