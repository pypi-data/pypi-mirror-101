import itertools
from dataclasses import dataclass
from dataclasses import field
from typing import Tuple
from typing import Set
from typing import Dict
from typing import List

import numpy as np

from forsyde.io.python.api import ForSyDeModel
from forsyde.io.python.core import Vertex
from forsyde.io.python.core import Edge
from forsyde.io.python.core import Port
from forsyde.io.python.types import SDFComb
from forsyde.io.python.types import Process
from forsyde.io.python.types import Signal
from forsyde.io.python.types import AbstractOrdering
from forsyde.io.python.types import AbstractMapping
from forsyde.io.python.types import AbstractScheduling
from forsyde.io.python.types import AbstractProcessingComponent
from forsyde.io.python.types import AbstractCommunicationComponent
from idesyde.identification.interfaces import DecisionModel
from idesyde.identification.interfaces import DirectDecisionModel
from idesyde.identification.interfaces import CompositeDecisionModel
from idesyde.identification.interfaces import MinizincableDecisionModel

import idesyde.sdf as sdfapi


@dataclass
class SDFExecution(DecisionModel):
    """
    This decision model captures all SDF actors and channels in
    the design model and can only be identified if the 'Global' SDF
    application (the union of all disjoint SDFs) is consistent, i.e.
    it has a PASS.

    After identification this decision model provides the global
    SDF topology and the PASS with all elements included.
    """

    sdf_actors: List[Vertex] = field(default_factory=list)
    sdf_delays: List[Vertex] = field(default_factory=list)
    sdf_channels: List[Tuple[Vertex, Vertex, List[Vertex]]] = field(default_factory=list)
    sdf_topology: np.ndarray = np.zeros((0, 0))
    sdf_repetition_vector: np.ndarray = np.zeros((0))
    sdf_initial_tokens: np.ndarray = np.zeros((0))
    sdf_pass: List[Vertex] = field(default_factory=list)

    sdf_max_tokens: np.ndarray = np.zeros((0))

    def covered_vertexes(self):
        yield from self.sdf_actors
        for (_, _, p) in self.sdf_channels:
            yield from p

    def compute_deduced_properties(self):
        self.max_tokens = np.zeros((len(self.sdf_channels)), dtype=int)
        for (cidx, c) in enumerate(self.sdf_channels):
            self.max_tokens[cidx] = max(self.sdf_topology[cidx, aidx] * self.sdf_repetition_vector[aidx]
                                        for (aidx, a) in enumerate(self.sdf_actors))


@dataclass
class SDFToOrders(MinizincableDecisionModel):

    # sub identifications
    sdf_exec_sub: SDFExecution = SDFExecution()

    # partial identification
    orderings: List[Vertex] = field(default_factory=list)

    def covered_vertexes(self):
        yield from self.orderings
        yield from self.sdf_exec_sub.covered_vertexes()

    def compute_deduced_properties(self):
        self.orderings_enum = {k: i for (i, k) in enumerate(self.orderings)}

    def get_mzn_data(self):
        data = dict()
        sub = self.sdf_exec_sub
        data['sdf_actors'] = range(1, len(sub.sdf_actors) + 1)
        data['sdf_channels'] = range(1, len(sub.sdf_channels) + 1)
        data['sdf_topology'] = sub.sdf_topology.tolist()
        data['max_steps'] = len(sub.sdf_pass) // len(self.orderings)
        data['max_steps'] += 1 if len(sub.sdf_pass) % len(self.orderings) > 0 else 0
        data['max_tokens'] = sub.max_tokens.tolist()
        data['activations'] = sub.sdf_repetition_vector[:, 0].tolist()
        data['static_orders'] = range(1, len(self.orderings) + 1)
        # TODO: find a awya to compute the initial tokens
        # reliably
        data['initial_tokens'] = [0 for c in sub.sdf_channels]
        return data

    def get_mzn_model_name(self):
        return 'sdf_order_linear_dmodel.mzn'

    def rebuild_forsyde_model(self, results):
        return ForSyDeModel()


@dataclass
class SDFToMultiCore(MinizincableDecisionModel):

    # sub identifications
    sdf_orders_sub: SDFToOrders = SDFToOrders()

    # partially identified
    cores: List[List[Vertex]] = field(default_factory=list)
    comms: List[List[Vertex]] = field(default_factory=list)
    connections: List[Tuple[Vertex, Vertex, List[Vertex]]] = field(default_factory=list)
    comms_capacity: List[int] = field(default_factory=list)

    # deduced properties
    # vertex_expansions: Dict[Vertex, List[Vertex]] = field(default_factory=dict)
    # edge_expansions: Dict[Edge, List[Edge]] = field(default_factory=dict)
    # cores_enum: Dict[Vertex, int] = field(default_factory=dict)
    # comm_enum: Dict[Vertex, int] = field(default_factory=dict)
    # expanded_cores_enum: Dict[Vertex, int] = field(default_factory=dict)
    # expanded_enum: Dict[Vertex, int] = field(default_factory=dict)
    max_steps: int = 1
    comms_path: List[List[List[int]]] = field(default_factory=list)

    def covered_vertexes(self):
        yield from self.cores
        yield from self.comms
        yield from self.sdf_orders_sub.covered_vertexes()

    def get_mzn_model_name(self):
        return "sdf_mpsoc_linear_dmodel.mzn"

    def compute_deduced_properties(self):
        self.sdf_orders_sub.compute_deduced_properties()
        # vertex_expansions = {p: [p] for p in self.cores}
        # edge_expansions = {e: [] for e in self.connections}
        # expanded_enum = {p: i for (i, p) in enumerate(self.cores)}
        # expand all TDMAs to their slot elements
        # units_enum_index = len(expanded_enum)
        # for (i, bus) in enumerate(self.comms):
        #     vertex_expansions[bus] = []
        #     for s in range(bus.properties['slots']):
        #         bus_slot = Vertex(identifier=f'{bus.identifier}_slot_{s}')
        #         expanded_enum[bus_slot] = units_enum_index
        #         vertex_expansions[bus].append(bus_slot)
        #         units_enum_index += 1
        firings = int(np.sum(self.sdf_orders_sub.sdf_exec_sub.sdf_repetition_vector))
        max_steps = firings // len(self.cores)
        if firings % len(self.cores) > 0:
            max_steps += 1
        # now go through all the connections and
        # create copies of them as necessary to accomodate
        # the newly created processor and comm elements
        # for (v, l) in vertex_expansions.items():
        #     for (o, ol) in vertex_expansions.items():
        #         for e in self.connections:
        #             if e.source_vertex == v and e.target_vertex == o:
        #                 for v_new in l:
        #                     for o_new in ol:
        #                         expanded_e = Edge(source_vertex=v_new, target_vertex=o_new, edge_type=e.edge_type)
        #                         edge_expansions[e].add(expanded_e)
        # self.vertex_expansions = vertex_expansions
        # self.edge_expansions = edge_expansions
        # self.expanded_enum = expanded_enum
        # self.expanded_comm_enum = expanded_comm_enum
        # self.cores_enum = cores_enum
        # self.comm_enum = comm_enum
        self.max_steps = max_steps
        self.comms_path = [[[0 for c in self.comms] for t in self.cores] for s in self.cores]
        for (s, t, p) in self.connections:
            sidx = self.cores.index(s)
            tidx = self.cores.index(t)
            for (i, u) in enumerate(p):
                uidx = self.comms.index(u)
                self.comms_path[sidx][tidx][uidx] = i + 1

    def get_mzn_data(self):
        data = self.sdf_orders_sub.get_mzn_data()
        # expanded_units_enum = {**self.expanded_cores_enum, **self.expanded_comm_enum}
        data['procs'] = set(i + 1 for (i, _) in enumerate(self.cores))
        data['comms'] = set(i + 1 for (i, _) in enumerate(self.comms))
        data['path'] = self.comms_path
        data['comms_capacity'] = self.comms_capacity
        # data['units_neighs'] = [
        #     set(self.expanded_enum[ex.target_vertex] + 1 for (e, el) in self.edge_expansions.items() for ex in el
        #         if ex.source_vertex == u).union(
        #             set(self.expanded_enum[ex.source_vertex] + 1 for (e, el) in self.edge_expansions.items()
        #                 for ex in el if ex.target_vertex == u)) for (u, uidx) in self.expanded_enum.items()
        # ]
        # since the minizinc model requires wcet and wcct,
        # we fake it with almost unitary assumption
        data['wcet'] = (data['max_tokens'] * np.ones((len(data['sdf_actors']), len(self.cores)), dtype=int)).tolist()
        data['token_wcct'] = (np.ones((len(data['sdf_channels']), len(data['procs']) + len(data['comms'])),
                                      dtype=int)).tolist()
        # since the minizinc model requires objective weights,
        # we just disconsder them
        data['objective_weights'] = [0, 0]
        # take away spurius extras
        data.pop('static_orders')
        return data

    def rebuild_forsyde_model(self, results):
        new_model = self.covered_model()
        max_steps = self.max_steps
        sdf_topology = self.sdf_orders_sub.sdf_exec_sub.sdf_topology
        sdf_actors = self.sdf_orders_sub.sdf_exec_sub.sdf_actors
        sdf_channels = self.sdf_orders_sub.sdf_exec_sub.sdf_channels
        orderings = self.sdf_orders_sub.orderings
        for (pidx, core) in enumerate(self.cores):
            ordering = orderings[pidx]
            if not new_model.has_edge(core, ordering, key="object"):
                new_edge = AbstractMapping(source_vertex=core,
                                           target_vertex=ordering,
                                           source_vertex_port=Port(identifier="execution"))
                new_model.add_edge(core, ordering, object=new_edge)
            slot = 0
            for t in range(max_steps):
                sdf_pass = sdfapi.get_PASS(
                    sdf_topology,
                    np.array([[results["mapped_actors"][a][pidx][t] for (a, _) in enumerate(sdf_actors)]]).transpose(),
                    np.array([[results["buffer_start"][c][pidx][t] for (c, _) in enumerate(sdf_channels)]]).transpose())
                for aidx in sdf_pass:
                    actor = sdf_actors[aidx]
                    if not new_model.has_edge(ordering, actor, key="object"):
                        new_edge = AbstractScheduling(source_vertex=ordering,
                                                      target_vertex=actor,
                                                      source_vertex_port=Port(identifier=f"slot[{slot}]"))
                        new_model.add_edge(ordering, actor, object=new_edge)
                        slot += 1
        for (commidx, comm) in enumerate(self.comms):
            ordering = orderings[commidx + len(self.cores)]
            if not new_model.has_edge(comm, ordering, key="object"):
                new_edge = AbstractMapping(source_vertex=comm,
                                           target_vertex=ordering,
                                           source_vertex_port=Port(identifier="timeslots"))
                new_model.add_edge(comm, ordering, object=new_edge)
            slots = [0 for c in sdf_channels]
            for (c, (s, t, path)) in enumerate(sdf_channels):
                clashes = [
                    slots[cc] for (p, _) in enumerate(self.cores) for (pp, _) in enumerate(self.cores)
                    for t in range(max_steps) for tt in range(max_steps) for cc in range(c)
                    if results["send_start"][c][p][pp][t][tt][commidx] +
                    results["send_duration"][c][p][pp][t][tt][commidx] >= results["send_start"][cc][p][pp][t][tt]
                    [commidx] or results["send_start"][cc][p][pp][t][tt][commidx] + results["send_duration"][cc][p][pp]
                    [t][tt][commidx] >= results["send_start"][c][p][pp][t][tt][commidx]
                ]
                slots[c] = min(slot for slot in range(self.comms_capacity[commidx]) if slot not in clashes)
                for e in path:
                    new_edge = AbstractScheduling(source_vertex=ordering,
                                                  target_vertex=e,
                                                  source_vertex_port=Port(identifier=f"slot[{slots[c]}]"))
                    new_model.add_edge(ordering, e, object=new_edge)
        return new_model


@dataclass
class SDFToMultiCoreCharacterized(MinizincableDecisionModel):

    # covered partial identifications
    sdf_mpsoc_sub: SDFToMultiCore = SDFToMultiCore()

    # elements that are partially identified
    wcet_vertexes: List[Vertex] = field(default_factory=list)
    token_wcct_vertexes: List[Vertex] = field(default_factory=list)
    goals_vertexes: List[Vertex] = field(default_factory=list)
    wcet: np.ndarray = np.zeros((0, 0), dtype=int)
    token_wcct: np.ndarray = np.zeros((0, 0), dtype=int)
    throughput_importance: int = 0
    latency_importance: int = 0
    send_overhead: np.ndarray = np.zeros((0, 0), dtype=int)
    read_overhead: np.ndarray = np.zeros((0, 0), dtype=int)

    # deduced properties
    # expanded_wcet: np.ndarray = np.array((0, 0), dtype=int)
    # expanded_token_wcct: np.ndarray = np.zeros((0, 0), dtype=int)

    def covered_vertexes(self):
        yield from self.wcet_vertexes
        yield from self.token_wcct_vertexes
        yield from self.goals_vertexes
        yield from self.sdf_mpsoc_sub.covered_vertexes()

    def compute_deduced_properties(self):
        pass

    def get_mzn_model_name(self):
        return "sdf_mpsoc_linear_dmodel.mzn"

    def get_mzn_data(self):
        data = self.sdf_mpsoc_sub.get_mzn_data()
        # remake the wcet and wcct with proper data
        data['max_steps'] = self.sdf_mpsoc_sub.max_steps
        data['wcet'] = self.wcet.tolist()
        data['token_wcct'] = self.token_wcct.tolist()
        data['objective_weights'] = [self.throughput_importance, self.latency_importance]
        return data

    def rebuild_forsyde_model(self, results):
        return self.sdf_mpsoc_sub.rebuild_forsyde_model(results)


@dataclass
class SDFToMPSoCClusteringDirect(DirectDecisionModel):
    """SDF 2 MPSoC clustering approach greedy decision model"""

    # covered partial identifications
    sdf_mpsoc_char_sub: SDFToMultiCoreCharacterized = SDFToMultiCoreCharacterized()

    # elements that are partially identified

    def execute(self):
        return None


@dataclass
class SDFToMPSoCClusteringMzn(MinizincableDecisionModel):
    """SDF 2 MPSoC clustering approach decision model

    This decision model executes a polynomial time algorithm
    whenever called by an explorer to obtain the minimum number
    of clusters that the SDF actors are mapped onto. These clusters
    are then mapped onto the platform.
    """

    # covered partial identifications
    sdf_mpsoc_char_sub: SDFToMultiCoreCharacterized = SDFToMultiCoreCharacterized()

    # elements that are partially identified

    # deduced properties
    num_clusters: int = 1

    # expanded_wcet: np.ndarray = np.array((0, 0), dtype=int)
    # expanded_token_wcct: np.ndarray = np.zeros((0, 0), dtype=int)

    def covered_vertexes(self):
        yield from self.sdf_mpsoc_char_sub.covered_vertexes()

    def compute_deduced_properties(self):
        # conservative estimation of the number of clusters
        self.num_clusters = int(
            self.sdf_mpsoc_char_sub.sdf_mpsoc_sub.sdf_orders_sub.sdf_exec_sub.sdf_repetition_vector.sum())

    def get_mzn_model_name(self):
        return "sdf_mpsoc_linear_cluster.mzn"

    def get_mzn_data(self):
        data = self.sdf_mpsoc_char_sub.get_mzn_data()
        # remake the wcet and wcct with proper data
        return data

    def rebuild_forsyde_model(self, results):
        return self.sdf_mpsoc_char_sub.rebuild_forsyde_model(results)


@dataclass
class CharacterizedJobShop(MinizincableDecisionModel):

    # models that were abstracted in jobs
    originals: List[DecisionModel] = field(default_factory=list)

    # properties
    jobs: List[Vertex] = field(default_factory=list)
    comm_jobs: List[Tuple[Vertex, Vertex, List[Vertex]]] = field(default_factory=list)
    # the virtual processors and communicators should go from
    # most physical -> cyber
    procs: List[List[Vertex]] = field(default_factory=list)
    comms: List[List[Vertex]] = field(default_factory=list)
    comm_capacity: List[int] = field(default_factory=list)
    weak_next: List[Tuple[int, int]] = field(default_factory=list)
    strong_next: List[Tuple[int, int]] = field(default_factory=list)
    wcet: np.ndarray = np.zeros((0, 0), dtype=int)
    wcct: np.ndarray = np.zeros((0, 0, 0), dtype=int)
    paths: List[Tuple[Vertex, Vertex, List[Vertex]]] = field(default_factory=list)
    objective_weights: List[int] = field(default_factory=list)

    def covered_vertexes(self):
        yield from self.jobs
        for p in self.procs:
            yield from p
        for p in self.comms:
            yield from p
        for m in self.originals:
            yield from m.covered_vertexes()

    def get_mzn_model_name(self):
        return "dependent_job_scheduling.mzn"

    def get_mzn_data(self):
        data = dict()
        data['jobs'] = set(i + 1 for (i, _) in enumerate(self.jobs))
        data['procs'] = set(i + 1 for (i, _) in enumerate(self.procs))
        data['comms'] = set(i + 1 for (i, _) in enumerate(self.comms))
        data['comm_capacity'] = self.comm_capacity
        # data['activations'] = self['self.sdf_mpsoc_sub.sdf_mpsoc_sub.sdf_orders_sub.sdf_exec_sub.sdf_repetition_vector
        # delete spurious elements
        data['weak_next'] = [[(sidx, tidx) in self.weak_next for (tidx, _) in enumerate(self.jobs)]
                             for (sidx, _) in enumerate(self.jobs)]
        data['strong_next'] = [[(sidx, tidx) in self.strong_next for (tidx, _) in enumerate(self.jobs)]
                               for (sidx, _) in enumerate(self.jobs)]
        data['path'] = [[[0 for c in self.comms] for t in self.procs] for s in self.procs]
        for (s, t, path) in self.paths:
            for (e, u) in enumerate(path):
                for (pidx, p) in enumerate(self.procs):
                    for (ppidx, pp) in enumerate(self.procs):
                        for (cidx, c) in enumerate(self.comms):
                            if s in p and t in pp and u in c:
                                data['path'][pidx][ppidx][cidx] = e + 1
        data['wcet'] = self.wcet.tolist()
        data['wcct'] = self.wcct.tolist()
        data['release'] = [0 for j in self.jobs]
        data['deadline'] = [0 for j in self.jobs]
        data['objective_weights'] = self.objective_weights
        return data

    def rebuild_forsyde_model(self, results):
        new_model = self.covered_model()
        # TODO: Must find a better and more general way to rebuild the
        # job shop abstraction
        for (jidx, plist) in enumerate(results["start"]):
            j = self.jobs[jidx]
            for (pidx, t) in enumerate(plist):
                if t is not None:
                    # create the mapping between elements of the abstract
                    # processing machine
                    for (p, pp) in zip(self.procs[pidx][:-1], self.procs[pidx][1:]):
                        if not new_model.has_edge(p, pp, key="object"):
                            new_edge = AbstractMapping(source_vertex=p, target_vertex=pp)
                            new_model.add_edge(p, pp, object=new_edge)
                    # add the job to this one machine, assuming the
                    # last element is the one represeting the machine's
                    # interface
                    p = self.procs[pidx][-1]
                    if not new_model.has_edge(p, j, key="object"):
                        new_edge = AbstractScheduling(source_vertex=p, target_vertex=j)
                        new_model.add_edge(p, j, object=new_edge)
                        if 'trigger-time' not in p.properties:
                            p.properties['trigger-time'] = {}
                        p.properties['trigger-time'][t] = j.identifier
        for (s, t, path) in self.comm_jobs:
            s_idxs = (i for (i, j) in enumerate(self.jobs) if j == s)
            t_idxs = (i for (i, j) in enumerate(self.jobs) if j == t)
            for (s_idx, t_idx, (u_idx, u)) in itertools.product(s_idxs, t_idxs, enumerate(self.comms)):
                t = results["comm_start"][s_idx][t_idx][u_idx]
                if t is not None:
                    # create the mapping between elements of the abstract
                    # processing communicator
                    for (p, pp) in zip(u[:-1], u[1:]):
                        if not new_model.has_edge(p, pp, key="object"):
                            new_edge = AbstractMapping(source_vertex=p, target_vertex=pp)
                            new_model.add_edge(p, pp, object=new_edge)
                    # add the comm job to this one communicator, assuming the
                    # last element is the one represeting the machine's
                    # interface
                    p = u[-1]
                    for c in path:
                        if not new_model.has_edge(p, c, key="object"):
                            new_edge = AbstractScheduling(source_vertex=p, target_vertex=c)
                            new_model.add_edge(p, c, object=new_edge)
                            if 'trigger-time' not in p.properties:
                                p.properties['trigger-time'] = {}
                            p.properties['trigger-time'][c.identifier] = t
        return new_model
