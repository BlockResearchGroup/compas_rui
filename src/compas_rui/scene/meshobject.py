from typing import Optional

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.itertools import flatten
from compas_rhino.scene import RhinoMeshObject
from compas_rui.forms import NamedValuesForm


class RUIMeshObject(RhinoMeshObject):
    mesh: Mesh

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Select
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def select_vertices(self, message="Select Vertices") -> list[int]:
        options = ["All", "Boundary", "Degree", "EdgeLoop", "EdgeStrip", "Manual"]
        option = rs.GetString(message=message, strings=options)
        if not option:
            return

        if option == "All":
            vertices = list(self.mesh.vertices())

        elif option == "Boundary":
            vertices = list(set(flatten(self.mesh.vertices_on_boundaries())))

        elif option == "Degree":
            D = rs.GetInteger(message="Vertex Degree", number=2, minimum=1)
            D = D or 0
            vertices = list(self.mesh.vertices_where(vertex_degree=D))

        elif option == "EdgeLoop":
            guids = compas_rhino.objects.select_lines(message="Select Loop Edges")
            edges = [self._guid_edge[guid] for guid in guids if guid in self._guid_edge] if guids else []
            temp = []
            for edge in edges:
                for u, v in self.mesh.edge_loop(edge):
                    temp.append(u)
                    temp.append(v)
            vertices = list(set(temp))

        elif option == "EdgeStrip":
            raise NotImplementedError

        elif option == "Manual":
            guids = compas_rhino.objects.select_points(message="Select Manual Vertices")
            vertices = [self._guid_vertex[guid] for guid in guids if guid in self._guid_vertex] if guids else []

        vertex_guid = {vertex: guid for guid, vertex in self._guid_vertex.items()}
        guids = [vertex_guid[vertex] for vertex in vertices]

        rs.UnselectAllObjects()
        rs.SelectObjects(guids)

        return vertices

    def select_edges(self, message="Select Edges") -> list[tuple[int, int]]:
        options = ["All", "Boundary", "EdgeLoop", "EdgeStrip", "Manual"]
        option = rs.GetString(message=message, strings=options)
        if not option:
            return

        if option == "All":
            edges = list(self.mesh.edges())

        elif option == "Boundary":
            edges = list(set(flatten(self.mesh.edges_on_boundaries())))

        elif option == "EdgeLoop":
            guids = compas_rhino.objects.select_lines(message="Select Loop Edges")
            edges = []
            for guid in guids:
                edge = self._guid_edge[guid]
                for edge in self.mesh.edge_loop(edge):
                    edges.append(edge)

        elif option == "EdgeStrip":
            guids = compas_rhino.objects.select_lines(message="Select Strip Edges")
            edges = []
            for guid in guids:
                edge = self._guid_edge[guid]
                for edge in self.mesh.edge_strip(edge):
                    edges.append(edge)

        elif option == "Manual":
            guids = compas_rhino.objects.select_lines(message="Select Manual Edges")
            edges = [self._guid_edge[guid] for guid in guids if guid in self._guid_edge] if guids else []

        edges = [(u, v) if self.mesh.has_edge((u, v)) else (v, u) for u, v in edges]
        edge_guid = {edge: guid for guid, edge in self._guid_edge.items()}
        guids = [edge_guid[edge] for edge in edges]

        rs.UnselectAllObjects()
        rs.SelectObjects(guids)

        return edges

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Draw
    # =============================================================================
    # =============================================================================
    # =============================================================================

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Modify
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def update_attributes(self) -> bool:
        names = sorted(self.mesh.attributes.keys())
        values = [str(self.mesh.attributes[name]) for name in names]

        form = NamedValuesForm(names=names, values=values)
        if form.show():
            self.mesh.attributes.update(form.attributes)
            return True
        return False

    def update_vertex_attributes(self, vertices: list[int], names: Optional[list[str]] = None) -> bool:
        if not vertices:
            return False

        names = names or sorted(self.mesh.default_vertex_attributes.keys())
        names = sorted([name for name in names if not name.startswith("_")])

        values = self.mesh.vertex_attributes(vertices[0], names)
        if len(vertices) > 1:
            for i, name in enumerate(names):
                for vertex in vertices[1:]:
                    if values[i] != self.mesh.vertex_attribute(vertex, name):
                        values[i] = "-"
                        break
        values = list(map(str, values))

        form = NamedValuesForm(names=names, values=values)
        if form.show():
            for name, value in form.attributes.items():
                if value == "-":
                    continue
                self.mesh.vertices_attribute(name=name, value=value, keys=vertices)
            return True
        return False

    def update_face_attributes(self, faces: list[int], names: Optional[list[str]] = None) -> bool:
        if not faces:
            return False

        names = names or sorted(self.mesh.default_face_attributes.keys())
        names = sorted([name for name in names if not name.startswith("_")])

        values = self.mesh.face_attributes(faces[0], names)
        if len(faces) > 1:
            for i, name in enumerate(names):
                for face in faces[1:]:
                    if values[i] != self.mesh.face_attribute(face, name):
                        values[i] = "-"
                        break
        values = list(map(str, values))

        form = NamedValuesForm(names=names, values=values)
        if form.show():
            for name, value in form.attributes.items():
                if value == "-":
                    continue
                self.mesh.faces_attribute(name=name, value=value, keys=faces)
            return True
        return False

    def update_edge_attributes(self, edges: list[tuple[int, int]], names: Optional[list[str]] = None) -> bool:
        if not edges:
            return False

        names = names or sorted(self.mesh.default_edge_attributes.keys())
        names = sorted([name for name in names if not name.startswith("_")])

        values = self.mesh.edge_attributes(edges[0], names)
        if len(edges) > 1:
            for i, name in enumerate(names):
                for edge in edges[1:]:
                    if values[i] != self.mesh.edge_attribute(edge, name):
                        values[i] = "-"
                        break
        values = list(map(str, values))

        form = NamedValuesForm(names=names, values=values)
        if form.show():
            for name, value in form.attributes.items():
                if value == "-":
                    continue
                self.mesh.edges_attribute(name=name, value=value, keys=edges)
            return True
        return False

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Move
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def move(self) -> bool:
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

        vertex_p0 = {v: Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices()}
        vertex_p1 = {v: Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices()}

        edges = list(self.mesh.edges())

        def OnDynamicDraw(sender, e):
            current = e.CurrentPoint
            vector = current - start
            for vertex in vertex_p1:
                vertex_p1[vertex] = vertex_p0[vertex] + vector
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for _, attr in self.mesh.vertices(True):
            attr["x"] += vector[0]
            attr["y"] += vector[1]
            attr["z"] += vector[2]

        return True

    def move_vertex(
        self,
        vertex: int,
        constraint: Rhino.Geometry.GeometryBase = None,
        allow_off: bool = True,
    ) -> bool:
        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.mesh.vertex_coordinates(nbr) for nbr in self.mesh.vertex_neighbors(vertex)]
        nbrs = [Rhino.Geometry.Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        self.mesh.vertex_attributes(vertex, "xyz", list(gp.Point()))
        return True

    def move_vertices(self, vertices: list[int]) -> bool:
        def OnDynamicDraw(sender, e):
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                e.Display.DrawDottedLine(a, b, color)
            for a, b in connectors:
                a = a + vector
                e.Display.DrawDottedLine(a, b, color)

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = self.mesh.vertex_coordinates(vertex)
            nbrs = self.mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = self.mesh.vertex_coordinates(nbr)
                line = [Rhino.Geometry.Point3d(*a), Rhino.Geometry.Point3d(*b)]
                if nbr in vertices:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for vertex in vertices:
            point = Point(*self.mesh.vertex_attributes(vertex, "xyz"))
            self.mesh.vertex_attributes(vertex, "xyz", point + vector)
        return True

    def move_vertices_direction(self, vertices: list[int], direction: str) -> bool:
        def OnDynamicDraw(sender, e):
            draw = e.Display.DrawDottedLine
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                draw(a, b, color)
            for a, b in connectors:
                a = a + vector
                draw(a, b, color)

        direction = direction.lower()
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(vertex))
            nbrs = self.mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = Rhino.Geometry.Point3d(*self.mesh.vertex_coordinates(nbr))
                if nbr in vertices:
                    lines.append((a, b))
                else:
                    connectors.append((a, b))

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        if direction == "x":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "y":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 1, 0))
        elif direction == "z":
            geometry = Rhino.Geometry.Line(start, start + Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "xy":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 0, 1))
        elif direction == "yz":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(1, 0, 0))
        elif direction == "zx":
            geometry = Rhino.Geometry.Plane(start, Rhino.Geometry.Vector3d(0, 1, 0))

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw

        if direction in ("x", "y", "z"):
            gp.Constrain(geometry)
        else:
            gp.Constrain(geometry, False)

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = compas_rhino.conversions.vector_to_compas(end - start)

        for vertex in vertices:
            point = self.mesh.vertex_point(vertex)
            self.mesh.vertex_attributes(vertex, "xyz", point + vector)

        return True

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Conduits
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # =============================================================================

    def clear_conduits(self):
        pass

    def clear(self):
        super().clear()
        self.clear_conduits()