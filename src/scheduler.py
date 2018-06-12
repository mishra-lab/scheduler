from netflow import FlowVertex, FlowArc

NUM_WEEKS = 10


class Clinician:
    def __init__(self, weeks_off=[], min_weeks=0, max_weeks=NUM_WEEKS):
        self.weeks_off = weeks_off
        self.min_weeks = min_weeks
        self.max_weeks = max_weeks


class Parser:
    """
    Converts an input file into arcs and vertices
    """

    def __init__(self, filename):
        self.vertices = {
            'source': FlowVertex('source', NUM_WEEKS),
            'sink': FlowVertex('sink', -NUM_WEEKS)
        }

        self.arcs = [
            # circulation edge
            FlowArc(
                self.vertices['sink'], 
                self.vertices['source'], 
                min_cap=0, 
                max_cap=self.vertices['source'].supply - self.vertices['sink'].supply, 
                cost=0, 
                fixed_cost=True)
        ]

        self.clinicians = {}
        content = ''
        with open(filename) as f:
            content = f.read()

        [bounds, weeks_off] = content.split('---\n')
        # parse bounds
        for line in bounds.rstrip().split('\n'):
            parts = line.split(':')
            key = parts[0]
            [min, max] = parts[1].split(',')
            self.clinicians[key] = Clinician([], int(min), int(max))
        # parse weeks off
        for line in weeks_off.split('\n'):
            parts = line.split(':')
            key = parts[0]
            weeks_off = parts[1].split(',')
            self.clinicians[key].weeks_off = weeks_off

        self.create_arcs()

    def create_arcs(self):
        # add vertices for each week up to NUM_WEEKS and an arc from
        # each week to the sink
        for i in range(0, NUM_WEEKS):
            self.vertices[str(i+1)] = FlowVertex(str(i+1), 0)
            self.arcs.append(
                FlowArc(
                    self.vertices[str(i+1)],
                    self.vertices['sink'],
                    min_cap=1,
                    max_cap=1,
                    cost=0,
                    fixed_cost=True)
            )

        # add vertices for each clinican, an arc from source to clinician
        # and an arc from clinician to each week
        sum_max = 0
        for key in self.clinicians:
            self.vertices[key] = FlowVertex(key, 0)
            clinician = self.clinicians[key]
            sum_max += clinician.max_weeks
            self.arcs.append(
                FlowArc(
                    self.vertices['source'],
                    self.vertices[key],
                    min_cap=clinician.min_weeks,
                    max_cap=clinician.max_weeks,
                    cost=0,
                    fixed_cost=True)
            )
            for i in range(0, NUM_WEEKS):
                self.arcs.append(
                    FlowArc(
                        self.vertices[key],
                        self.vertices[str(i+1)],
                        min_cap=0,
                        max_cap=1,
                        cost=1000 if str(i+1) in clinician.weeks_off else 1,
                        fixed_cost=True if str(i+1) in clinician.weeks_off else False)
                )

    def get_arcs(self):
        return self.arcs

    def get_vertices(self):
        return self.vertices
