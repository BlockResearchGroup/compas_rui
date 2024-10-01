********************************************************************************
Tutorial
********************************************************************************

More info coming soon...


.. code-block:: python

    import rhinoscriptsyntax as rs
    from compas.scene import Scene
    from compas.datastructures import Mesh

    mesh = Mesh.from_meshgrid(10, 10)

    scene = Scene()
    meshobj = scene.add(mesh, show_vertices=True)
    scene.draw()

    rs.Redraw()

    vertices = meshobj.select_vertices()
    print(vertices)


.. code-block:: python

    import rhinoscriptsyntax as rs
    from compas.scene import Scene
    from compas.datastructures import Mesh

    mesh = Mesh.from_meshgrid(10, 10)

    scene = Scene()
    meshobj = scene.add(mesh)
    scene.draw()

    rs.Redraw()

    meshobj.show_vertices = True
    meshobj.draw_vertices()

    vertices = meshobj.select_vertices()
    print(vertices)
