# Tutorials

## Features

* [Copy/Pate UV](#copypaste-uv)
* [Transfer UV](#transfer-uv)
* [Flip/Rotate UV](#fliprotate-uv)
* [Mirror UV](#mirror-uv)
* [Move UV](#move-uv)
* [World Scale UV](#world-scale-uv)
* [Preserve UV Aspect](#preserve-uv-aspect)
* [Texture Lock](#texture-lock)
* [Texture Wrap](#texture-wrap)
* [UV Sculpt](#uv-sculpt)
* [Unwrap Constraint](#unwrap-constraint)
* [Texture Projection](#texture-lock)
* [UVW](#uvw)
* [Align UV](#align-uv)
* [Smooth UV](#smooth-uv)
* [Select UV](#select-uv)
* [Pack UV (Extension)](#pack-uv-extension)
* [Align UV Cursor](#align-uv-cursor)
* [UV Cursor Location](#uv-cursor-location)
* [UV Bounding Box](#uv-bounding-box)
* [UV Inspection](#uv-inspection)

## Tutorial (Video)

[![](https://img.youtube.com/vi/0Gj0xvt7Jdc/0.jpg)](https://www.youtube.com/watch?v=0Gj0xvt7Jdc)

## Tutorial (Text)

### Copy/Paste UV

#### Among faces (in 3D View)

Copy and paste UV coordinates among same/different object's faces in 3D View.  
Copy/Paste UV sometimes fails to paste UV correctly because of the incorrect UV index. Instead, you can try Transfer UV which you can copy and paste based on the topology.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **Copy/Paste UV**|
|Location (Built-in Menu)|**3D View** > **U** > **Copy/Paste UV**|
|Mode|**Edit**|

[Usage]
1. Click check box **Copy/Paste UV** to show Copy/Paste UV menu
2. Select faces whose UV you want to copy
3. Click **Copy** > **(Target UV Map)**
4. Select faces whose UV you want to paste
5. Click **Paste** > **(Target UV Map)**

* There are special Target UV Map
  * **[Default]** : Copy/paste UV maps currently displayed
  * **[All]** : Copy/Paste all UV maps
  * **[New]** : Allocate new UV map and paste to it
* **Selection Sequence** option provides a way to specify the ordering of copied/pasted faces by face selection
* If **Seams** option is enabled, you can also copy/paste seams
* **Strategy** option provides a way to decide copy/paste UV repeatedly if a number of copied faces is differs from pasted faces
* You can flip or rotate UV by changing **Flip Copied UV** option or **Rotate Copied UV** option in Tool shelf option

#### Among faces (in UV/Image Editor)

Copy and paste UV coordinates among same/different object's faces in UV/Image Editor. This feature is derived from below add-on.  
[[AddOn] UV_Tool](https://blenderartists.org/forum/showthread.php?294904-AddOn-UV_Tool)

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **Copy/Paste UV**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **Copy/Paste UV**|
|Mode|**Edit**|

[Usage]
1. Select UVs you want to copy
2. Click **Copy**
3. Select UVs you want to paste
4. Click **Paste**

*NOTICE: You must select UVs which consist closed loop (i.e. face)*

#### Among objects

Copy and paste UV coordinates among same topology objects.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **Copy/Paste UV**|
|Location (Built-in Menu)|**3D View** > **Object** > **Copy/Paste UV**|
|Mode|**Object**|

[Usage]
1. Select object whose UV you want to copy
2. Click **Copy** > **(Target UV Map)**
3. Select objects whose UV you want to paste
4. Click **Paste** > **(Target UV Map)**

* There are special Target UV Map
  * **[Default]** : Copy/paste UV maps currently displayed
  * **[All]** : Copy/Paste all UV maps
  * **[New]** : Allocate new UV map and paste to it
* If **Seams** option is enabled, you can also copy/paste seams
* You can paste UV to the multiple objects


### Transfer UV

Copy and paste UV coordinates based on the mesh's topology.  
Transfer UV can solve the Copy/Paste UV issue raised when the meshes don't have same UV indices. However, Transfer UV also can not solve the issue raised when you try the meshes which don't have same topology.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **Copy/Paste UV**|
|Location (Built-in Menu)|**3D View** > **U** > **Copy/Paste UV**|
|Mode|**Edit**|

[Usage]
1. Click check box **Transfer UV** to show Transfer UV menu
2. Select **2 adjacent faces** of the mesh whose UV you want to copy
3. Click **Copy**
4. Select **2 adjacent faces** of the mesh whose UV you want to paste
5. Click **Paste**

*NOTICE: Copied/Pasted mesh must have the same number of faces*

* Transfer UV ignore the hidden faces.
* You can paste UV to the multiple meshes
* If **Seams** option is enabled, you can also copy/paste seams
* If **Invert Normals** option is enabled, you can copy/paste to the mirrored mesh


### Flip/Rotate UV

Flip or rotate UV.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Flip/Rotate UV** to show Flip/Rotate UV menu
2. Select faces whose UV you want to flip or rotate.
3. Click **Flip/Rotate**
4. Change value **Flip UV** or **Rotate UV** in Tool shelf option

* If **Seams** option is enabled, you can also flip/rotate seams


### Mirror UV

Make mirrored UV. This feature is derived from below add-on.  
[Addon: Copy UVs from Mirror](http://blenderaddonlist.blogspot.jp/2015/05/addon-copy-uvs-from-mirror.html)

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Mirror UV** to show Mirror UV menu
2. Select faces you want to refer
3. Choose the axis of the mirror direction
4. Click **Mirror**

* **Error** option in Tool shelf option can change the error threshold for mirror

### Move UV

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

Move UV with a mouse in 3D View. This feature is derived from below add-on.  
[ADDON: Move the UV from the 3D view](https://blenderartists.org/forum/showthread.php?256424-ADDON-Move-the-UV-from-the-3D-view)

[Usage]
1. Click check box **Move UV** to show Move UV menu
2. Select vertices/edges/faces whose UV you want to move
3. Click **Start**
4. Press **Mouse Left Button** to start moving UV
5. You can move UV with mouse
6. Press **Mouse Left Button** to stop moving UV

* If you want to cancel moving UV, press **Mouse Right Button**


### World Scale UV

Measure and set texel density. This feature is derived from below add-on.  
[[Addon] World Scale UV](https://blenderartists.org/forum/showthread.php?275652-Addon-World-Scale-UV)

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|


#### Mode: Manual

[Usage]
1. Click check box **World Scale UV** to show World Scale UV menu
2. Select mode **Manual**
3. Change value **Texture Size** referred as virtual texture size
4. Change value **Density** referred as target texel density
5. Select face you want to apply texel density
6. Click **Apply**

* **Origin** option changes the UV origin after applying texel density

#### Mode: Same Density

[Usage]
1. Click check box **World Scale UV** to show World Scale UV menu
2. Select mode **Same Density**
3. Select face you want to measure a texel density
4. Click **Measure**
5. You can see the target texel density
6. Select face you want to apply texel density
7. Click **Apply**

* **Origin** option changes the UV origin after applying texel density

#### Mode: Scaling Density

[Usage]
1. Click check box **World Scale UV** to show World Scale UV menu
2. Select mode **Scaling Density**
3. Select face you want to measure a texel density
4. Click **Measure**
5. You can see the measured texel density
6. Change value **Scaling Factor** for the scale factor of the texel density
7. Select face you want to apply texel density
8. Click **Apply**

* **Origin** option changes the UV origin after applying texel density

#### Mode: Proportional to Mesh

[Usage]
1. Click check box **World Scale UV** to show World Scale UV menu
2. Select mode **Proportional to Mesh**
3. Select face you want to measure a texel density
4. Click **Measure**
5. You can see the measured mesh area, UV area and density
6. Select face you want to apply texel density
7. Click **Apply**

* **Origin** option changes the UV origin after applying texel density


### Preserve UV Aspect

Change assigned texture with preserving UV aspect.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Preserve UV Aspect** to show Preserve UV Aspect menu
2. Select face you want to change texture
3. Select texture you want to assign
4. Click **Change Image**

* **Origin** option changes the UV origin after changing texture


### Texture Lock

Preserve UV while you edit the mesh.
This feature is same as "Preserve UVs" feature on 3dsmax.  

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

#### Normal Mode

[Usage]
1. Click check box **Texture Lock** to show Texture Lock menu
2. Select vertices/edges/faces which you want to preserve UV
3. Click **Lock**
4. Transform vertices/edges/faces as you like
5. Click **Unlock**, you can return to the UV before locking

* If **connect** option is enabled, you can keep UV connection by changing other face's UV.

#### Interactive mode

[Usage]
1. Click check box **Texture Lock** to show Texture Lock menu
2. Select vertices/edges/faces which you want to preserve UV
3. Click **Lock**
4. Transform vertices/edges/faces while preserving UV
5. Click **Unlock**


### Texture Wrap

Set texture coordinate along to the mesh structure.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Texture Wrap** to show Texture Wrap menu
2. Select a face whose UV you want to refer as initial position
3. Click **Refer**
4. Select an adjacent face whose UV you want to set
5. Click **Set**

* If **Set and Refer** option is enabled, you don't need to click **Refer** after **Set** as long as you refer same face
* If **Selection Sequence** option is enabled, you can select multiple faces and apply **Set** at once. The application order follows the selection sequence


### UV Sculpt

UV Sculpt in 3D View. Same features are supported as the UV sculpt in UV/Image Editor.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **UV Sculpt** to show UV Sculpt menu
2. Select faces whose UV you want to sculpt
3. Click **Enable**
4. Sculpt UV as you like (See detail each tool's usage)
5. Click **Disable**

| | |
|---|---|
|Grab|Move UV along to the mouse movement while you press **Mouse Left Button**|
|Relax|Relax UV while you press **Mouse Left Button**|
|Pinch|Pinch UV while you press **Mouse Left Button**|

* If **Show Brush** option is enabled, display the brush's effective range while sculpting
* **Radius** option provides a way to change the brush radius
* **Strength** option provides a way to change the effectiveness
* You can change tool from **Tools** option
* **Method** option (only available on Relax tool) provides a way to change the relax method
* If **Invert** option (only available on Pinch tool) is enabled, the direction of pinch will be inverted


### Unwrap Constraint

Unwrap UV with an axis fixed. This feature is same as "Unfold Constraints" feature on Maya.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Mapping**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Mapping**|
|Mode|**Edit**|

[Usage]
1. Click check box **Unwrap Constraint** to show Unwrap Constraint menu
2. Select faces whose UV you want to unwrap
3. Enable or disable **U-Constraint** option and **V-constraint** option to fix axis while unwrapping
4. Click **Unwrap**

* Default Unwrap option is available from Tool shelf option


### Texture Projection

Project the texture to the mesh while displaying texture image in 3D View.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Mapping**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Mapping**|
|Mode|**Edit**|

[Usage]
1. Click check box **Texture Projection** to show Texture Projection menu
2. Select faces whose UV you want to apply Texture Projection
3. Select a texture to be projected
4. Click **Enable** to display the texture
5. Adjust texture size and the mesh location to decide the location of projection
6. Click **Project** to project texture to UV
7. Click **Disable**

* **Transparency** option provides a way to change transparency of the displayed texture
* If **Adjust Window** option is enabled, size of the displayed texture is adjusted to the window
* **Magnitude** option (only available if Adjust Window is disabled) provides a way to change size of displayed texture
* If **Texture Aspect Ratio** option is enabled, keep the original aspect of the displayed texture
* If **Assign UV Map** option is enabled, assign new UV map when no UV is assigned to the mesh


### UVW

UVW mapping.

| | |
|---|---|
|Location|**3D View** > **Tool shelf** > **UV Mapping**|
|Location (Built-in Menu)|**3D View** > **U** > **UV Mapping**|
|Mode|**Edit**|

[Usage]
1. Click check box **UVW** to show UVW menu
2. Select faces you want to apply UVW mapping
3. Click **Box** if you apply Box mapping, or click **Best Planner** if you apply Best Planner mapping

* If **Assign UV Map** option is enabled, assign new UV map when no UV is assigned to the mesh
* From Tool shelf option, you can tweak mapping configuration


### Align UV

Align UV. This feature is derived from below add-on.  
[[AddOn] UV_Tool](https://blenderartists.org/forum/showthread.php?294904-AddOn-UV_Tool)

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Align UV** to show Align UV menu
2. Select UVs you want to align (see details below)
3. Click **Circle** or **Straighten** or **XY-axis** depending on your purpose

|Align method|Select|Align to|
|---|---|---|
|Circle|All the outermost UVs|Round shape|
|Straighten|The endmost UVs|Straight line between begin UV and end UV|
|XY-axis|The endmost UVs|Straight line along to X or Y axis|

* If **Transmission** option is enabled, align UVs with vertical direction
* If **Select** option is enabled, the aligned UVs will be selected after operation
* If **Vertical** option is enabled, align UVs to vertical direction with using the influence of mesh vertex location
* If **Horizontal** option is enabled, align UVs to horizontal direction with using influence of mesh vertex location
* **Mesh Influence** option provides a way to change the influence of mesh structure
* In case of XY-axis alignment, you can change the location (Middle, Right/Bottom, Left/Top) after UV alignment


### Smooth UV

Smooth UV. This feature is derived from below add-on.  
[[AddOn] UV_Tool](https://blenderartists.org/forum/showthread.php?294904-AddOn-UV_Tool)

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Smooth UV** to show Smooth UV menu
2. Select UVs you want to smooth (The endmost UVs must be selected)
3. Click **Smooth**

* If **Transmission** option is enabled, smooth UVs which are located on vertical direction of selected UV
* If **Select** option is enabled, the smoothed UVs are selected
* **Mesh Influence** option provides a way to change the influence of mesh structure


### Select UV

Select UV under the specific condition.

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Select UV** to show Select UV menu
2. Click **Overlapped** or **Flipped** depending on your purpose (see details below)

|Feature|Select target|
|---|---|
|Overlapped|Select all overlapped UVs|
|Flipped|Select all flipped UVs|


### Pack UV (Extension)

Apply island packing and integrate islands which have same shape.

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **UV Manipulation**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **UV Manipulation**|
|Mode|**Edit**|

[Usage]
1. Click check box **Pack UV (Extension)** to show Pack UV (Extension) menu
2. Select faces whose UV you want to pack
3. Click **Pack UV**

* **Allowable Center Deviation** provides a way to specify the center deviation that regards as the same island
* **Allowable Size Deviation** provides a way to specify the size deviation that regards as the same island
* Default Pack Islands option is available from Tool shelf option in 3D View


### Align UV Cursor

Align UV cursor (2D Cursor in UV/Image Editor).

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **Editor Enhancement**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **Editor Enhancement**|
|Mode|**Edit**|

[Usage]
1. Click check box **Align UV Cursor** to show Align UV Cursor menu
2. Select **Texture** or **UV** or **UV (Selected)** depending on your purpose (See details below)
3. Click the position button (You can choose the position from 9 buttons)

|Mode|Align to|
|---|---|
|Texture|Selected texture|
|UV|Displayed UV (includes non-selected UV)|
|UV (Selected)|Displayed UV (only selected UV)|


### UV Cursor Location

Set and display UV Cursor (2D Cursor in UV/Image Editor) location.

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **Editor Enhancement**|
|Mode|**Edit**|

[Usage]
1. Click check box **UV Cursor Location** to show UV Cursor Location menu
2. UV cursor location is displayed, and you can set the new location as you like


### UV Bounding Box

Transform UV with Bounding Box like a Photoshop/GIMP's Bounding Box.

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **Editor Enhancement**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **Editor Enhancement**|
|Mode|**Edit**|

[Usage]
1. Click check box **UV Bounding Box** to show UV Bounding Box menu
2. Click **Show** to show the bounding box
3. Transform UV with the bounding box as you like (You can transform UV same as Photoshop/Gimp)
4. Click **Hide**

* If **Uniform Scaling** option is enabled, you can transform uniformly
* **Boundary** option specify the boundary of the bounding box


### UV Inspection

Inspect UV and help you to find which UV is on the abnormal condition.

| | |
|---|---|
|Location|**UV/Image Editor** > **Tool shelf** > **Editor Enhancement**|
|Location (Built-in Menu)|**UV/Image Editor** > **UVs** > **Editor Enhancement**|
|Mode|**Edit**|

[Usage]
1. Click check box **UV Inspection** to show UV Inspection menu
2. Click **Show** to enhance the part on which is under specific condition
3. Click **Update** if you want to update to the latest status
4. Click **Hide**

* If **Overlapped** option is enabled, the overlapped part is enhanced
* If **Flipped** option is enabled, the flipped part is enhanced
* If you specify **Part** in **Mode** option, enhance only to the overlapped/flipped part. If you specify **Face**, enhance the overlapped/flipped face
