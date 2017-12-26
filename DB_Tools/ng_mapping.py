
terminal_map = {
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