import datetime

from TM1py.Exceptions import TM1pyException
from TM1py.Services import TM1Service


class DimensionService:

    def __init__(self, source: TM1Service, target: TM1Service, server: TM1Service):
        self.source = source
        self.target = target
        self.server = server

    def copy_dimension(self, dimension: str, item: str, deployment: str):
        start_time = datetime.datetime.now()
        try:
            if self.source.dimensions.exists(dimension_name=dimension):
                dim = self.source.dimensions.get(dimension_name=dimension)
                if self.target.dimensions.exists(dimension_name=dimension):
                    self.target.dimensions.update(dimension=dim)
                    message = f"Target dimension: '{dimension}' updated"
                else:
                    self.target.dimensions.create(dimension=dim)
                    message = f"Target dimension: '{dimension}' created"
            else:
                message = "Source dimension does not exist"
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            cellset = dict()
            cellset[(deployment, item, "Deployment Status")] = message
            cellset[(deployment, item, "Deployment Start")] = datetime.datetime.strftime(start_time,
                                                                                         '%Y-%m-%d %H:%M:%S')
            cellset[(deployment, item, "Deployment End")] = datetime.datetime.strftime(end_time,
                                                                                       '%Y-%m-%d %H:%M:%S')
            cellset[(deployment, item, "Deployment Duration")] = str(duration)
            self.server.cubes.cells.write_values('System - Deployments', cellset)
        except TM1pyException as t:
            print(t)

    def copy_subset(self, dimension: str, subset: str, item: str, deployment: str):
        start_time = datetime.datetime.now()
        try:
            if self.source.subsets.exists(dimension_name=dimension,
                                          hierarchy_name=dimension,
                                          subset_name=subset,
                                          private=False):
                source_subset = self.source.subsets.get(dimension_name=dimension,
                                                        hierarchy_name=dimension,
                                                        subset_name=subset,
                                                        private=False)
                if self.target.subsets.exists(dimension_name=dimension,
                                              hierarchy_name=dimension,
                                              subset_name=subset,
                                              private=False):
                    self.target.subsets.update(subset=source_subset, private=False)
                    message = f"Target subset: '{subset}' updated"
                else:
                    self.target.subsets.create(subset=source_subset, private=False)
                    message = f"Target subset: '{subset}' created"
            else:
                message = f"Source subset '{subset}' does not exist"
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            cellset = dict()
            cellset[(deployment, item, "Deployment Status")] = message
            cellset[(deployment, item, "Deployment Start")] = datetime.datetime.strftime(start_time,
                                                                                         '%Y-%m-%d %H:%M:%S')
            cellset[(deployment, item, "Deployment End")] = datetime.datetime.strftime(end_time,
                                                                                       '%Y-%m-%d %H:%M:%S')
            cellset[(deployment, item, "Deployment Duration")] = str(duration)
            self.server.cubes.cells.write_values('System - Deployments', cellset)
        except TM1pyException as t:
            print(t)
