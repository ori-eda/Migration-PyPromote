from TM1py.Services import TM1Service

from PyPromote.Services import CubeService, DimensionService, ProcessService


class PyPromoteService:

    def __init__(self, source: TM1Service, target: TM1Service, server: TM1Service):
        self.source = source
        self.target = target
        self.server = server
        self.cube = CubeService(source=self.source, target=self.target, server=self.server)
        self.dimension = DimensionService(source=self.source, target=self.target, server=self.server)
        self.process = ProcessService(source=self.source, target=self.target, server=self.server)
