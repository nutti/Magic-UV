.. _bpy.types.Scene.muv:
.. _bpy.ops.uv.muv:

********
Magic UV
********

Activation
==========

- Open Blender and go to Preferences then the Add-ons tab.
- Click UV then Magic UV to enable the script.


Interface
=========

Located in the :menuselection:`3D Viewport --> Sidebar -->  Edit`
and :menuselection:`UV Editor --> Sidebar --> Magic UV`.


Instructions
============

- :ref:`Copy/Paste UV <copypaste-uv>`
- :ref:`Transfer UV <transfer-uv>`
- :ref:`Flip/Rotate UV <fliprotate-uv>`
- :ref:`Mirror UV <mirror-uv>`
- :ref:`Move UV <move-uv>`
- :ref:`World Scale UV <world-scale-uv>`
- :ref:`Preserve UV Aspect <preserve-uv-aspect>`
- :ref:`Texture Lock <texture-lock>`
- :ref:`Texture Wrap <texture-wrap>`
- :ref:`UV Sculpt <uv-sculpt>`
- :ref:`Unwrap Constraint <unwrap-constraint>`
- :ref:`Texture Projection <texture-projection>`
- :ref:`UVW <uvw>`
- :ref:`Align UV <align-uv>`
- :ref:`Smooth UV <smooth-uv>`
- :ref:`Select UV <select-uv>`
- :ref:`Pack UV (Extension) <pack-uv-extension>`
- :ref:`Clip UV <clip-uv>`
- :ref:`Align UV Cursor <align-uv-cursor>`
- :ref:`UV Cursor Location <uv-cursor-location>`
- :ref:`UV Bounding Box <uv-bounding-box>`
- :ref:`UV Inspection <uv-inspection>`


.. _copypaste-uv:

Copy/Paste UV
-------------

3D Viewport (Edit)
^^^^^^^^^^^^^^^^^^

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Copy/Paste UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Copy/Paste UV --> Copy/Paste UV`

Copy and paste UV coordinates among same/different object's faces in 3D View.
Copy/Paste UV sometimes fails to paste UV correctly because of the incorrect UV index.
Instead, you can try Transfer UV which you can copy and paste based on the topology.

Target UV Map
  :Default: Copy/paste UV maps currently displayed.
  :All: Copy/Paste all UV maps.
  :New: Allocate new UV map and paste to it.

Copy/Paste Mode
   :Selection Sequence: provides a way to specify the ordering of copied/pasted faces by face selection.
Seams
   If enabled, you can also copy/paste seams.
Strategy
   Provides a way to decide copy/paste UV repeatedly if a number of copied faces is differs from pasted faces.

.. tip::

   You can flip or rotate UV by changing *Flip Copied UV* property or *Rotate Copied UV* property.

.. rubric:: Usage

#. Click check box *Copy/Paste UV* to show Copy/Paste UV menu.
#. Select faces whose UV you want to copy.
#. Click :menuselection:`Copy --> (Target UV Map)`.
#. Select faces whoe UV you want to paste.
#. Click :menuselection:`Paste --> (Target UV Map)``.


3D Viewport (Object)
^^^^^^^^^^^^^^^^^^^^

.. reference::

   :Editor:    3D Viewport
   :Mode:      Object
   :Menu:      :menuselection:`Object --> Copy/Paste UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Copy/Paste UV`

Copy and paste UV coordinates among same topology objects.

Copy/Target UV Map
  :[Default]: Copy/paste UV maps currently displayed.
  :[All]: Copy/Paste all UV maps.
  :[New]: Allocate new UV map and paste to it.
Seams
   If enabled, you can also copy/paste seams.

.. rubric:: Usage

#. Select object whose UV you want to copy.
#. Click :menuselection:`Copy --> (Target UV Map)`.
#. Select objects whose UV you want to paste.
#. Click :menuselection:`Paste --> (Target UV Map)`.

.. tip::

   You can paste UV to the multiple objects.


UV Editor
^^^^^^^^^

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UV --> Copy/Paste UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Copy/Paste UV`

Copy and paste UV coordinates among same/different object's faces in UV Editor.

.. rubric:: Usage

#. Select UVs you want to copy.
#. Click *Copy*.
#. Select UVs you want to paste.
#. Click *Paste*.

.. note::

   You must select UVs which consist closed loop (i.e. face).


.. _transfer-uv:

Transfer UV
-----------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Transfer UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Copy/Paste UV --> Transfer UV`

Copy and paste UV coordinates based on the mesh's topology.
Transfer UV can solve the Copy/Paste UV issue raised when the meshes don't have same UV indices.
However, Transfer UV also can not solve the issue raised when you try the meshes which don't have same topology.

Invert Normals
   If enabled, you can copy/paste to the mirrored mesh.
Seams
   If enabled, you can also copy/paste seams.

.. rubric:: Usage

#. Click check box *Transfer UV* to show Transfer UV menu.
#. Select *2 adjacent faces* of the mesh whose UV you want to copy.
#. Click *Copy*.
#. Select *2 adjacent faces* of the mesh whose UV you want to paste.
#. Click *Paste*.

.. note::

   - Copied/Pasted mesh must have the same number of faces.
   - Transfer UV ignore the hidden faces.
   - You can paste UV to the multiple meshes.


.. _fliprotate-uv:

Flip/Rotate UV
--------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Flip/Rotate UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Flip/Rotate UV`

Flip or rotate UV.

Seams
   If enabled, you can also flip/rotate seams.

.. rubric:: Usage

#. Click check box *Flip/Rotate UV* to show Flip/Rotate UV menu.
#. Select faces whose UV you want to flip or rotate.
#. Click *Flip/Rotate*.
#. Change value *Flip UV* or *Rotate UV*.


.. _mirror-uv:

Mirror UV
---------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Mirror UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Mirror UV`

Make mirrored UV.

Error
   Changes the error threshold for mirror.
Origin
   Specifies the origin of the mirror operation.

.. rubric:: Usage

#. Click check box *Mirror UV* to show Mirror UV menu.
#. Select faces you want to refer.
#. Choose the axis of the mirror direction.
#. Click *Mirror*.


.. _move-uv:

Move UV
-------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Move UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Move UV`

Move UV with a mouse in the 3D Viewport.

.. rubric:: Usage

#. Click check box *Move UV* to show Move UV menu.
#. Select vertices/edges/faces whose UV you want to move.
#. Click *Start*.
#. Press *Mouse Left Button* to start moving UV.
#. You can move UV with mouse.
#. Press *Mouse Left Button* to stop moving UV.

If you want to cancel moving UV, press :kbd:`RMB`.


.. _world-scale-uv:

World Scale UV
--------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> World Scale UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> World Scale UV`

Measure and set texel density.

Texture
   Texture to be used for the size calculation of density.

  :[Average]: Average size of textures assigned to the selected object.
  :[Max]: Max size of textures assigned to the selected object.
  :[Min]: Min size of textures assigned to the selected object.
  :(Texture Name): Size of selected texture.
Origin
   Changes the UV origin after applying texel density.
Area Calculation Method
   Method to calculate mesh area, UV area and density.
Only Selected
   If enabled, measure/apply only to the selected faces.


Mode: Manual
^^^^^^^^^^^^

.. rubric:: Usage

#. Click check box *World Scale UV* to show World Scale UV menu.
#. Select mode *Manual*.
#. Change value *Texture Size* referred as virtual texture size.
#. Change value *Density* referred as target texel density.
#. Select face you want to apply texel density.
#. Click *Apply*.


Mode: Same Density
^^^^^^^^^^^^^^^^^^

.. rubric:: Usage

#. Click check box *World Scale UV* to show World Scale UV menu.
#. Select mode *Same Density*.
#. Select face you want to measure a texel density.
#. Click *Measure*.
#. You can see the target texel density.
#. Select face you want to apply texel density.
#. Click *Apply*.


Mode: Scaling Density
^^^^^^^^^^^^^^^^^^^^^

.. rubric:: Usage

#. Click check box *World Scale UV* to show World Scale UV menu.
#. Select mode *Scaling Density*.
#. Select face you want to measure a texel density.
#. Click *Measure*.
#. You can see the measured texel density.
#. Change value *Scaling Factor* for the scale factor of the texel density.
#. Select face you want to apply texel density.
#. Click *Apply*.


Mode: Proportional to Mesh
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rubric:: Usage

#. Click check box *World Scale UV* to show World Scale UV menu.
#. Select mode *Proportional to Mesh*.
#. Select face you want to measure a texel density.
#. Click *Measure*.
#. You can see the measured mesh area, UV area and density.
#. Select face you want to apply texel density.
#. Click *Apply*.


.. _preserve-uv-aspect:

Preserve UV Aspect
------------------

.. reference::

   :Editor:    3D Viewport
   :Menu:      :menuselection:`UVs --> Preserve UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Preserve UV Aspect`

Change assigned texture with preserving UV aspect.

Origin
  Changes the UV origin after changing texture.

.. rubric:: Usage

#. Click check box *Preserve UV Aspect* to show Preserve UV Aspect menu.
#. Select face you want to change texture.
#. Select texture you want to assign.
#. Click *Change Image*.


.. _texture-lock:

Texture Lock
------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Texture Lock`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Manipulation --> Texture Lock`

Preserve UV while you edit the mesh.


Normal Mode
^^^^^^^^^^^

Connect
   If enabled, you can keep UV connection by changing other face's UV.

.. rubric:: Usage

#. Click check box *Texture Lock* to show Texture Lock menu.
#. Select vertices/edges/faces which you want to preserve UV.
#. Click *Lock*.
#. Transform vertices/edges/faces as you like.
#. Click *Unlock*, you can return to the UV before locking.


Interactive Mode
^^^^^^^^^^^^^^^^

.. rubric:: Usage

#. Click check box *Texture Lock* to show Texture Lock menu.
#. Select vertices/edges/faces which you want to preserve UV.
#. Click *Lock*.
#. Transform vertices/edges/faces while preserving UV.
#. Click *Unlock*.


.. _texture-wrap:

Texture Wrap
------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Texture Wrap`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Manipulation --> Texture Wrap`

Set texture coordinate along to the mesh structure.

Set and Refer
   If enabled, you don't need to click *Refer* after *Set* as long as you refer same face.
Selection Sequence
   If enabled, you can select multiple faces and apply *Set* at once.
   The application order follows the selection sequence.

.. rubric:: Usage

#. Click check box *Texture Wrap* to show Texture Wrap menu.
#. Select a face whose UV you want to refer as initial position.
#. Click *Refer*.
#. Select an adjacent face whose UV you want to set.
#. Click *Set*.


.. _uv-sculpt:

UV Sculpt
---------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> UV Sculpt`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Manipulation --> UV Sculpt`

UV Sculpt in the 3D Viewport.
Same features are supported as the UV sculpt in UV Editor.

Radius
   Provides a way to change the brush radius.
Strength
   Provides a way to change the effectiveness.
Tools
   :Grab: Move UV along to the mouse movement while you press *Mouse Left Button*.
   :Relax: Relax UV while you press *Mouse Left Button*.

      Method
          Provides a way to change the relax method.
   :Pinch: Pinch UV while you press *Mouse Left Button*.

      Invert
         If enabled, the direction of pinch will be inverted.
Show Brush
   If enabled, display the brush's effective range while sculpting.

.. rubric:: Usage

#. Click check box *UV Sculpt* to show UV Sculpt menu.
#. Select faces whose UV you want to sculpt.
#. Click *Enable*.
#. Sculpt UV as you like (See detail each tool's usage).
#. Click *Disable*.


.. _unwrap-constraint:

Unwrap Constraint
-----------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Unwrap Constraint`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Mapping --> Unwrap Constraint`

Unwrap UV with an axis fixed.

.. rubric:: Usage

#. Click check box *Unwrap Constraint* to show Unwrap Constraint menu.
#. Select faces whose UV you want to unwrap.
#. Enable or disable *U-Constraint* property and *V-constraint* property to fix axis while unwrapping.
#. Click *Unwrap*.


.. _texture-projection:

Texture Projection
------------------

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> Texture Projection`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Mapping --> Texture Projection`

Project the texture to the mesh while displaying texture image in 3D View.

Transparency
   Provides a way to change transparency of the displayed texture.
Adjust Window
   If enabled, size of the displayed texture is adjusted to the window.
Scaling, Rotation, Translation
   Provide a way to apply the affine transformation to the displayed texture.
   Available when *Adjust Window* is disabled.
Texture Aspect Ratio
   If enabled, keep the original aspect of the displayed texture.
Assign UV Map
   If enabled, assign new UV map when no UV is assigned to the mesh.

.. rubric:: Usage

#. Click check box *Texture Projection* to show Texture Projection menu.
#. Select faces whose UV you want to apply Texture Projection.
#. Select a texture to be projected.
#. Click *Enable* to display the texture.
#. Adjust texture size and the mesh location to decide the location of projection.
#. Click *Project* to project texture to UV.
#. Click *Disable*.


.. _uvw:

UVW
---

.. reference::

   :Editor:    3D Viewport
   :Mode:      Edit
   :Menu:      :menuselection:`UV --> UVW`
   :Panel:     :menuselection:`Sidebar --> Edit --> UV Mapping --> UVW`

UVW mapping.

Assign UV Map
   If enabled, assign new UV map when no UV is assigned to the mesh.
Force Axis
   Specifies the axis to apply force mapping.

.. rubric:: Usage

#. Click check box *UVW* to show UVW menu.
#. Select faces you want to apply UVW mapping.
#. Click *Box* if you apply Box mapping, or click *Best Planner* if you apply Best Planner mapping.


.. _align-uv:

Align UV
--------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Align UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Align UV`


Align
^^^^^

Align UV.

Circle
   Selects all the outermost UVs and aligns them to a round shape.
Straighten
   Selects the endmost UVs and aligns them to a straight line between begin UV and end UV.
XY-axis
   Selects the endmost UVs and aligns them to a straight line along to X or Y axis.
Align Location
   In case of XY-axis alignment, you can change the location (Middle, Right/Bottom, Left/Top) after UV alignment.

Transmission
   Align UVs with vertical direction.
Select
   The aligned UVs will be selected after operation.
Vertical
   Align UVs to vertical direction with using the influence of mesh vertex location.
Horizontal
   Align UVs to horizontal direction with using influence of mesh vertex location.
Mesh Influence
   Provides a way to change the influence of mesh structure.

.. rubric:: Usage

#. Click check box *Align UV* to show Align UV menu.
#. Select UVs you want to align (see details below).
#. Click *Circle* or *Straighten* or *XY-axis* depending on your purpose.


Snap
^^^^

Snap UV coordinates to the specified location.

Snap Method
   :Point: Snap UV coordinates to the location specified by *Target Point*.
   :Edge: Snap UV coordinates to the location specified by *Target Edge*.


Snap: Point
"""""""""""

Group
   :Vertex: All selected vertices will snap to *Target Point*.
   :Face: Center of all selected faces will snap to *Target Point*.
   :UV Island: Center of all selected islands will snap to *Target Point*.

.. rubric:: Usage

#. Click check box *Align UV* to show Align UV menu.
#. Select snap method *Point*.
#. Set *Target Point* where UV coordinate will snap to.
#. Set snap *Group* (See below for details).
#. Select vertices or faces or UV islands which you want to snap.


Snap: Edge
""""""""""

Group
   :Edge: Selected edge will snap to the center of *Target Edge*.
   :Face:
      All edges belonging to faces which are included in selected
      edge will snap to the center of *Target Edge*.
   :UV Island:
      All edges belonging to UV islands which are included in
      selected edge will snap to the center of *Target Edge*.

.. rubric:: Usage

#. Click check box *Align UV* to show Align UV menu
#. Select snap method *Edge*.
#. Set *Target Edge* where UV edge will snap to.
#. Set snap *Group* (See below for details).
#. Select edges which you want to snap.


.. _smooth-uv:

Smooth UV
---------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Smooth UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Smooth UV`

Smooth UV.

Transmission
   If enabled, smooth UVs which are located on vertical direction of selected UV.
Select
   If enabled, the smoothed UVs are selected.
Mesh Influence
   Provides a way to change the influence of mesh structure.

.. rubric:: Usage

#. Click check box *Smooth UV* to show Smooth UV menu.
#. Select UVs you want to smooth (The endmost UVs must be selected).
#. Click *Smooth*.


.. _select-uv:

Select UV
---------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Select UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Select UV`

Select UV under the specific condition.

Overlapped
   Selects all overlapped UVs.
Flipped
   Selects all flipped UVs.

Same Polygon Threshold
   Provides a way to set a threshold for judging the same polygons.
Selection Method
   Specifies how to select the faces.
Sync Mesh Selection
   Select the mesh's faces as well as UV's faces.

Zoom Selected UV
   Zoom to the selected UV in 3D Viewport.

.. rubric:: Usage

#. Click check box *Select UV* to show Select UV menu.
#. Click *Overlapped* or *Flipped* depending on your purpose (see details below).


.. _pack-uv-extension:

Pack UV (Extension)
-------------------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Pack UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Pack UV (Extension)`

Apply island packing and integrate islands which have same shape.

Allowable Center Deviation
   Provides a way to specify the center deviation that regards as the same island.
Allowable Size Deviation
   Provides a way to specify the size deviation that regards as the same island.

.. rubric:: Usage

#. Click check box *Pack UV (Extension)* to show Pack UV (Extension) menu.
#. Select faces whose UV you want to pack.
#. Click *Pack UV*.


.. _clip-uv:

Clip UV
-------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Clip UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> UV Manipulation --> Clip UV`

Clip UV coordinate to the specified range.

Range
   Specifies the clipping range.

.. rubric:: Usage

#. Click check box *Clip UV* to show Clip UV menu.
#. Select faces you want to clip UV coordinates.
#. Click *Clip UV*.


.. _align-uv-cursor:

Align UV Cursor
---------------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Align UV Cursor`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Editor Enhancement --> Align UV Cursor`

Align UV cursor (2D Cursor in UV Editor).

Align Method
   :Texture: The UV cursor aligns to the selected texture.
   :UV: The UV cursor aligns to the d UV (includes non-selected UV).
   :UV (Selected): The UV cursor aligns to the displayed UV (only selected UV).

.. rubric:: Usage

#. Click check box *Align UV Cursor* to show Align UV Cursor menu.
#. Select *Texture* or *UV* or *UV (Selected)* depending on your purpose (See details below).
#. Click the position button (You can choose the position from 9 buttons).


.. _uv-cursor-location:

UV Cursor Location
------------------

.. reference::

   :Editor:    UV Editor
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Editor Enhancement --> UV Cursor Location`

Set and display UV Cursor (2D Cursor in UV Editor) location.

.. rubric:: Usage

#. Click check box *UV Cursor Location* to show UV Cursor Location menu.
#. UV cursor location is displayed, and you can set the new location as you like.


.. _uv-bounding-box:

UV Bounding Box
---------------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> UV Bounding Box`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Editor Enhancement --> UV Bounding Box`

Transform UV with Bounding Box like a Photoshop/GIMP's Bounding Box.

Uniform Scaling
   If enabled, you can transform uniformly.
Boundary
   Specifies the boundary of the bounding box.

.. rubric:: Usage

#. Click check box *UV Bounding Box* to show UV Bounding Box menu.
#. Click *Show* to show the bounding box.
#. Transform UV with the bounding box as you like (You can transform UV same as Photoshop/Gimp).
#. Click *Hide*.


.. _uv-inspection:

UV Inspection
-------------

.. reference::

   :Editor:    UV Editor
   :Menu:      :menuselection:`UVs --> Inspect UV`
   :Panel:     :menuselection:`Sidebar --> Magic UV --> Editor Enhancement --> UV Inspection`


Inspect UV
^^^^^^^^^^

Inspect UV and help you to find which UV is on the abnormal condition.

Overlapped
   The overlapped part/face is enhanced.
Flipped
   The flipped part/face is enhanced.
Mode
   :Part: Enhance only to the overlapped/flipped part.
   :Face: Enhance the overlapped/flipped face.
Same Polygon Threshold
   Provides a way to set a threshold for judging the same polygons.
Display View3D
   Display overlapped/flipped faces on View3D as well as UV Editor.

.. rubric:: Usage

#. Click check box *UV Inspection* to show UV Inspection menu.
#. Click *Show* to enhance the part on which is under specific condition.
#. Click *Update* if you want to update to the latest status.
#. Click *Hide*.


Paint UV island
^^^^^^^^^^^^^^^

Paint UV island with random color.

.. rubric:: Usage

#. Click check box *UV Inspection* to show UV Inspection menu.
#. Click *Paint UV island*.


Other Resources
===============

The supplemental documentation (e.g. FAQ) and early release can be found in Magic UV's
`Github repository <https://github.com/nutti/Magic-UV>`__.

.. reference::

   :Category:  UV
   :Description: UV tool set. See add-ons preferences for details.
   :Location: :menuselection:`3D Viewport --> Sidebar -->  Edit` and `UV Editor --> Sidebar ---> Magic UV`
   :File: magic_uv folder
   :Author: Nutti, Mifth, Jace Priester, kgeogeo, mem, imdjs, Keith (Wahooney) Boshoff, McBuff,
            MaxRobinot, Alexander Milovsky
   :License: GPL 3+
   :Note: This add-on is bundled with Blender.
