"""
Hexastorm Web Model Exporter
- Dynamically discovers and composites ALL PCB materials into Matte Black PBR materials with Gold ENIG pads and white silkscreen
- Fixes laser diode housing material to rich metallic bronze/brass
- Fixes motorhead metal material to dark turned steel (no washed-out white)
- Fixes FFC cable alignment directly into connector 2-84952-0
- Bakes seamless 120-frame periodic 1/4-turn polygon prism & rotor rotation (-90 degrees)
- prismholder002 remains completely stationary (static housing)
- Bakes physically accurate dynamic laser ray tracing (incident, prism refraction, scanning beam, SOS mirror bounce, and spot)
- Exports single-track unified animation with Draco compression (~20.8 MB)
- Synchronizes output across Quarto source, docs, and hardware repos
"""

import bpy
import mathutils
import math
import numpy as np
from PIL import Image
import os
import shutil

print("=== Starting Hexastorm Web Model Exporter (Matte Black PCBs + Bronze Diode + Steel Motor + Static Prismholder) ===")

output_dir_io = "/home/hexastorm/Documents/Python/hstarmans.github.io/models"
output_dir_docs = "/home/hexastorm/Documents/Python/hstarmans.github.io/docs/models"
output_dir_cad = "/home/hexastorm/Documents/hardware/hexastorm_design/models"
cache_dir = "/home/hexastorm/Documents/hardware/hexastorm_design/renders/pbr_cache"

for d in [output_dir_io, output_dir_docs, output_dir_cad, cache_dir]:
    os.makedirs(d, exist_ok=True)

glb_path_io = os.path.join(output_dir_io, "hexastorm.glb")
glb_path_docs = os.path.join(output_dir_docs, "hexastorm.glb")
glb_path_cad = os.path.join(output_dir_cad, "hexastorm.glb")

# -------------------------------------------------------------
# Part 1: Matte Black PCB PBR Material Baking for ALL PCBs
# -------------------------------------------------------------

def get_image_as_numpy(blend_img):
    if not blend_img or blend_img.size[0] == 0:
        return None
    w, h = blend_img.size
    pixels = np.empty(w * h * 4, dtype=np.float32)
    blend_img.pixels.foreach_get(pixels)
    pixels = np.clip(pixels, 0.0, 1.0)
    pixels = pixels.reshape((h, w, 4))
    return np.flipud(pixels)

def composite_pcb_pbr(cu_img, mask_img, silks_img, paste_img, is_green=False):
    ref_img = cu_img or mask_img or silks_img
    if not ref_img:
        return None, None
        
    w, h = ref_img.size
    
    cu_arr = get_image_as_numpy(cu_img)
    mask_arr = get_image_as_numpy(mask_img)
    silks_arr = get_image_as_numpy(silks_img)
    paste_arr = get_image_as_numpy(paste_img)
    
    has_cu = (cu_arr[:, :, 0] > 0.3) if cu_arr is not None else np.zeros((h, w), dtype=bool)
    has_mask = (mask_arr[:, :, 0] > 0.3) if mask_arr is not None else np.ones((h, w), dtype=bool)
    has_silks = (silks_arr[:, :, 0] > 0.3) if silks_arr is not None else np.zeros((h, w), dtype=bool)
    has_paste = (paste_arr[:, :, 0] > 0.3) if paste_arr is not None else np.zeros((h, w), dtype=bool)
    
    albedo = np.zeros((h, w, 3), dtype=np.uint8)
    arm = np.zeros((h, w, 3), dtype=np.uint8)
    arm[:, :, 0] = 255 # Occlusion default 1.0
    
    if is_green:
        dielectric_color = np.array([22, 65, 28], dtype=np.uint8)
        trace_color = np.array([38, 115, 45], dtype=np.uint8)
        dielectric_roughness = int(0.45 * 255)
        trace_roughness = int(0.25 * 255)
    else:
        # Matte Black
        dielectric_color = np.array([20, 20, 22], dtype=np.uint8)
        trace_color = np.array([32, 32, 35], dtype=np.uint8)
        dielectric_roughness = int(0.85 * 255)
        trace_roughness = int(0.50 * 255)
        
    bare_fr4 = np.array([130, 120, 80], dtype=np.uint8)
    albedo[:, :] = bare_fr4
    arm[:, :, 1] = int(0.60 * 255)
    arm[:, :, 2] = 0
    
    mask_no_cu = has_mask & (~has_cu)
    albedo[mask_no_cu] = dielectric_color
    arm[mask_no_cu, 1] = dielectric_roughness
    arm[mask_no_cu, 2] = 0
    
    mask_with_cu = has_mask & has_cu
    albedo[mask_with_cu] = trace_color
    arm[mask_with_cu, 1] = trace_roughness
    arm[mask_with_cu, 2] = 0
    
    exposed_cu = (~has_mask) & has_cu
    enig_gold = np.array([230, 195, 110], dtype=np.uint8)
    albedo[exposed_cu] = enig_gold
    arm[exposed_cu, 1] = int(0.28 * 255)
    arm[exposed_cu, 2] = int(0.95 * 255)
    
    albedo[has_paste] = np.array([215, 218, 220], dtype=np.uint8)
    arm[has_paste, 1] = int(0.35 * 255)
    arm[has_paste, 2] = int(0.90 * 255)
    
    silks_visible = has_silks & (~has_paste)
    albedo[silks_visible] = np.array([245, 245, 245], dtype=np.uint8)
    arm[silks_visible, 1] = int(0.70 * 255)
    arm[silks_visible, 2] = 0
    
    albedo_img = Image.fromarray(albedo, mode='RGB')
    arm_img = Image.fromarray(arm, mode='RGB')
    
    # Web & iOS Safari Optimization: Clamp PCB resolution to 1024px to prevent WebKit memory exhaustion
    MAX_PCB_DIM = 1024
    if albedo_img.width > MAX_PCB_DIM or albedo_img.height > MAX_PCB_DIM:
        scale = min(MAX_PCB_DIM / albedo_img.width, MAX_PCB_DIM / albedo_img.height)
        new_w = max(1, int(albedo_img.width * scale))
        new_h = max(1, int(albedo_img.height * scale))
        albedo_img = albedo_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        arm_img = arm_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    return albedo_img, arm_img

# Convert ALL materials in Blender that contain PCB layers to Matte Black PBR Principled BSDF
converted_pcb_count = 0
for mat in bpy.data.materials:
    if not mat.node_tree:
        continue
    cu_node = mat.node_tree.nodes.get('cu')
    if not cu_node or not cu_node.image:
        continue
        
    mask_node = mat.node_tree.nodes.get('mask')
    silks_node = mat.node_tree.nodes.get('silks')
    paste_node = mat.node_tree.nodes.get('paste')
    
    cu_img = cu_node.image
    mask_img = mask_node.image if mask_node else None
    silks_img = silks_node.image if silks_node else None
    paste_img = paste_node.image if paste_node else None
    
    safe_name = mat.name.replace(".", "_")
    albedo_path = os.path.join(cache_dir, f"{safe_name}_albedo.png")
    arm_path = os.path.join(cache_dir, f"{safe_name}_arm.png")
    
    albedo_pil, arm_pil = composite_pcb_pbr(cu_img, mask_img, silks_img, paste_img, is_green=False)
    if not albedo_pil or not arm_pil:
        continue
        
    albedo_pil.save(albedo_path, format="PNG", optimize=True)
    arm_pil.save(arm_path, format="PNG", optimize=True)
    
    bl_albedo = bpy.data.images.load(albedo_path, check_existing=True)
    bl_albedo.colorspace_settings.name = 'sRGB'
    
    bl_arm = bpy.data.images.load(arm_path, check_existing=True)
    bl_arm.colorspace_settings.name = 'Non-Color'
    
    # Rebuild material nodes with clean PBR Principled BSDF
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    out = nodes.new('ShaderNodeOutputMaterial')
    p_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    tex_alb = nodes.new('ShaderNodeTexImage')
    tex_alb.image = bl_albedo
    
    tex_arm = nodes.new('ShaderNodeTexImage')
    tex_arm.image = bl_arm
    sep_arm = nodes.new('ShaderNodeSeparateColor')
    
    mat.node_tree.links.new(tex_alb.outputs['Color'], p_bsdf.inputs['Base Color'])
    mat.node_tree.links.new(tex_arm.outputs['Color'], sep_arm.inputs['Color'])
    mat.node_tree.links.new(sep_arm.outputs['Green'], p_bsdf.inputs['Roughness'])
    mat.node_tree.links.new(sep_arm.outputs['Blue'], p_bsdf.inputs['Metallic'])
    mat.node_tree.links.new(p_bsdf.outputs['BSDF'], out.inputs['Surface'])
    
    converted_pcb_count += 1
    print(f"Converted PCB material '{mat.name}' to Matte Black PBR")

print(f"Total PCB materials converted to Matte Black: {converted_pcb_count}")

# -------------------------------------------------------------
# Part 2: Metal Shaders (Bronze Diode Housing & Dark Turned Steel Motorhead)
# -------------------------------------------------------------

# 1. Laser Diode Housing -> Bronze / Brass
def setup_bronze_material(mat_name):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    # Rich warm bronze/brass: RGB (0.86, 0.58, 0.24)
    bsdf.inputs['Base Color'].default_value = (0.86, 0.58, 0.24, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.24
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print(f"Configured material '{mat_name}' as metallic bronze")

setup_bronze_material('copper.001')
setup_bronze_material('metallaserdiode')

# Assign bronze material to laserdiodebasesolid and lenstubebody (laser_ring002 is chrome!)
bronze_mat = bpy.data.materials.get('metallaserdiode')
for obj_name in ['laserdiodebasesolid', 'lenstubebody']:
    obj = bpy.data.objects.get(obj_name)
    if obj and obj.data and hasattr(obj.data, 'materials'):
        obj.data.materials.clear()
        obj.data.materials.append(bronze_mat)
        print(f"Assigned bronze material to '{obj_name}'")

# 1b. Laser Diode Front Retention Ring -> Polished Chrome
def setup_chrome_material(mat_name='chrome_metal'):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    # High-polish bright chrome/chromium
    bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.98, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.05
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print(f"Configured material '{mat_name}' as polished chrome")

setup_chrome_material('chrome_metal')
chrome_mat = bpy.data.materials.get('chrome_metal')

ring_obj = bpy.data.objects.get('laser_ring002')
if ring_obj and ring_obj.data and hasattr(ring_obj.data, 'materials'):
    ring_obj.data.materials.clear()
    ring_obj.data.materials.append(chrome_mat)
    print("Assigned polished chrome material to 'laser_ring002'")

# 1c. Optical Turning Mirror -> High-Reflectivity Specular Mirror Surface
def setup_mirror_material(mat_name='mirror'):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    # Optically flat first-surface mirror: pure metal, near-zero roughness for sharp reflections
    bsdf.inputs['Base Color'].default_value = (0.98, 0.98, 0.98, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.005
    bsdf.inputs['IOR'].default_value = 1.52
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print(f"Configured material '{mat_name}' as high-reflectivity optical mirror")

setup_mirror_material('mirror')
mirror_mat = bpy.data.materials.get('mirror')
mirror_obj = bpy.data.objects.get('mirror')
if mirror_obj and mirror_obj.data and hasattr(mirror_obj.data, 'materials'):
    mirror_obj.data.materials.clear()
    mirror_obj.data.materials.append(mirror_mat)
    print("Assigned polished mirror material to 'mirror' object")

# 1d. Cylindrical Lenses Glass Material
def setup_glass_material(mat_name='Material_Optical_Glass'):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.95, 0.98, 1.0, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.01
    bsdf.inputs['IOR'].default_value = 1.52
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 1.0
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print(f"Configured material '{mat_name}' as optical glass with transmission")

setup_glass_material('Material_Optical_Glass')

# 1e. Laserhead Screws (M2x12 1 to 4) -> Fix from legacy Glossy BSDF (which rendered chalk white) to Hardware Steel
bolt_mat = bpy.data.materials.get('CNC_Bolt_Hardware_Steel')
if not bolt_mat:
    bolt_mat = bpy.data.materials.new(name='CNC_Bolt_Hardware_Steel')
    nodes = bolt_mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.72, 0.73, 0.75, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.95
    bsdf.inputs['Roughness'].default_value = 0.20
    bolt_mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

metal_screw_mat = bpy.data.materials.get('metal_screw')
if metal_screw_mat:
    nodes = metal_screw_mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.72, 0.73, 0.75, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.95
    bsdf.inputs['Roughness'].default_value = 0.20
    metal_screw_mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print("Updated 'metal_screw' material to Principled BSDF steel")

for obj_name in ['M2x12_Screw_01', 'M2x12_Screw_02', 'M2x12_Screw_03', 'M2x12_Screw_04']:
    s_obj = bpy.data.objects.get(obj_name)
    if s_obj and s_obj.data and hasattr(s_obj.data, 'materials'):
        s_obj.data.materials.clear()
        s_obj.data.materials.append(bolt_mat)
        print(f"Assigned CNC_Bolt_Hardware_Steel to '{obj_name}'")

# 2. Motorhead Metal & Metal Ring -> Turned Dark Steel / Titanium Bell
def setup_steel_material(mat_name):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    # Dark turned steel: RGB (0.28, 0.29, 0.31)
    bsdf.inputs['Base Color'].default_value = (0.28, 0.29, 0.31, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.28
    mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    print(f"Configured material '{mat_name}' as turned dark steel")

setup_steel_material('motor_bell_steel')
setup_steel_material('metalring')

# -------------------------------------------------------------
# Part 3: Rigging FFC Cable to Connector 2-84952-0
# -------------------------------------------------------------

ffc = bpy.data.objects.get("FFC_Cable")
if ffc and ffc.type == 'CURVE' and ffc.data.splines:
    s = ffc.data.splines[0]
    ref_ffc = [
        (0.030400, -0.479100, 0.158400, 0.030400, -0.479100, 0.148400, 0.030400, -0.479100, 0.168400),
        (0.030400, -0.465000, 0.250000, 0.030400, -0.475000, 0.200000, 0.015000, -0.450000, 0.285000),
        (-0.015000, -0.435000, 0.300000, 0.010000, -0.450000, 0.295000, -0.040000, -0.415000, 0.295000),
        (-0.065000, -0.365000, 0.245000, -0.050000, -0.385000, 0.275000, -0.080000, -0.345000, 0.210000),
        (-0.080000, -0.358000, 0.130000, -0.078000, -0.358000, 0.170000, -0.085000, -0.358000, 0.080000),
        (-0.108630, -0.358000, 0.045000, -0.108630, -0.358000, 0.070884, -0.108630, -0.358000, 0.025000),
        (-0.108630, -0.367401, 0.029189, -0.111341, -0.357593, 0.030562, -0.105880, -0.377348, 0.027797),
        (-0.108630, -0.380310, 0.046500, -0.108630, -0.380310, 0.038000, -0.108630, -0.380310, 0.048500),
    ]
    for idx, bp_data in enumerate(ref_ffc):
        if idx < len(s.bezier_points):
            bp = s.bezier_points[idx]
            bp.co = (bp_data[0], bp_data[1], bp_data[2])
            bp.handle_left = (bp_data[3], bp_data[4], bp_data[5])
            bp.handle_right = (bp_data[6], bp_data[7], bp_data[8])
    print("Locked FFC_Cable point 0 directly into connector 2-84952-0 socket!")

# -------------------------------------------------------------
# Part 4: Sample 120-Frame Periodic Laser Ray Tracing
# -------------------------------------------------------------

TOTAL_FRAMES = 120
START_BLEND_FRAME = 833

# Explicitly load and register hexastorm_laser_tracer.py so physics handler is active
tracer_text = bpy.data.texts.get('hexastorm_laser_tracer.py')
if tracer_text:
    exec(tracer_text.as_string(), globals())
    if 'register' in globals():
        globals()['register']()
    print("Explicitly loaded and registered hexastorm_laser_tracer.py handler!")

frames_data = []
for i in range(TOTAL_FRAMES + 1):
    f_src = START_BLEND_FRAME + i
    bpy.context.scene.frame_set(f_src)
    if 'update_laser_physics' in globals():
        globals()['update_laser_physics'](bpy.context.scene)
    
    beam_air = bpy.data.objects.get("Laser_Beam_Air")
    s0 = beam_air.data.splines[0]
    p_diode = mathutils.Vector(s0.points[0].co[:3])
    p_prism_in = mathutils.Vector(s0.points[1].co[:3])
    
    s1 = beam_air.data.splines[1]
    p_prism_out = mathutils.Vector(s1.points[0].co[:3])
    p_target = mathutils.Vector(s1.points[1].co[:3])
    
    hit_mirror = False
    p_mirror_refl = None
    if len(s1.points) == 3 and s1.points[1].co[1] != s1.points[2].co[1]:
        hit_mirror = True
        p_mirror_refl = mathutils.Vector(s1.points[2].co[:3])
        
    frames_data.append({
        'frame_idx': i + 1,
        'p_diode': p_diode,
        'p_prism_in': p_prism_in,
        'p_prism_out': p_prism_out,
        'p_target': p_target,
        'hit_mirror': hit_mirror,
        'p_mirror_refl': p_mirror_refl,
    })

p_start = frames_data[0]['p_target']
p_half = frames_data[60]['p_target']
scan_span_mm = (p_half - p_start).length * 1000.0
print(f"Sampled {len(frames_data)} frames of ray-traced laser beam physics.")
print(f"  Frame 1  Target: {p_start}")
print(f"  Frame 61 Target: {p_half}")
print(f"  Laser Scan Sweep Distance: {scan_span_mm:.2f} mm across substrate plane!")
if scan_span_mm < 1.0:
    raise RuntimeError(f"ERROR: Laser beam is not moving! Sweep distance is only {scan_span_mm:.3f} mm!")

# -------------------------------------------------------------
# Part 5: Dynamic Laser Beams Setup
# -------------------------------------------------------------

laser_mat = bpy.data.materials.get("Web_Laser_Glow")
if not laser_mat:
    laser_mat = bpy.data.materials.new(name="Web_Laser_Glow")
    laser_mat.use_nodes = True
    lnodes = laser_mat.node_tree.nodes
    lnodes.clear()
    out = lnodes.new('ShaderNodeOutputMaterial')
    emit = lnodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = (0.05, 0.85, 1.0, 1.0) # High-tech UV Cyan Glow
    emit.inputs['Strength'].default_value = 10.0
    laser_mat.node_tree.links.new(emit.outputs['Emission'], out.inputs['Surface'])

def create_beam_cylinder(name, radius=0.00035):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=1.0, vertices=8, location=(0,0,0))
    cyl = bpy.context.active_object
    cyl.name = name
    cyl.data.materials.clear()
    cyl.data.materials.append(laser_mat)
    cyl.rotation_mode = 'QUATERNION'
    return cyl

beam_incident = create_beam_cylinder("Web_Laser_Incident", radius=0.00035)
beam_glass = create_beam_cylinder("Web_Laser_Glass", radius=0.00030)
beam_scan = create_beam_cylinder("Web_Laser_Scan", radius=0.00035)
beam_sos = create_beam_cylinder("Web_Laser_SOS", radius=0.00030)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = TOTAL_FRAMES

def set_beam_endpoints(obj, p_a, p_b, visible=True):
    if not visible or (p_b - p_a).length < 1e-6:
        obj.scale = (0.0, 0.0, 0.0)
        return
    v = p_b - p_a
    dist = v.length
    obj.location = (p_a + p_b) * 0.5
    obj.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(v.normalized())
    obj.scale = (1.0, 1.0, dist)

spot_bed = bpy.data.objects.get("Laser_Spot_Bed")
if spot_bed:
    spot_bed.animation_data_clear()

for fd in frames_data:
    f = fd['frame_idx']
    if f > TOTAL_FRAMES:
        continue
        
    set_beam_endpoints(beam_incident, fd['p_diode'], fd['p_prism_in'], visible=True)
    beam_incident.keyframe_insert(data_path="location", frame=f)
    beam_incident.keyframe_insert(data_path="rotation_quaternion", frame=f)
    beam_incident.keyframe_insert(data_path="scale", frame=f)
    
    set_beam_endpoints(beam_glass, fd['p_prism_in'], fd['p_prism_out'], visible=True)
    beam_glass.keyframe_insert(data_path="location", frame=f)
    beam_glass.keyframe_insert(data_path="rotation_quaternion", frame=f)
    beam_glass.keyframe_insert(data_path="scale", frame=f)
    
    set_beam_endpoints(beam_scan, fd['p_prism_out'], fd['p_target'], visible=True)
    beam_scan.keyframe_insert(data_path="location", frame=f)
    beam_scan.keyframe_insert(data_path="rotation_quaternion", frame=f)
    beam_scan.keyframe_insert(data_path="scale", frame=f)
    
    if fd['hit_mirror'] and fd['p_mirror_refl']:
        set_beam_endpoints(beam_sos, fd['p_target'], fd['p_mirror_refl'], visible=True)
    else:
        beam_sos.scale = (0.0, 0.0, 0.0)
    beam_sos.keyframe_insert(data_path="location", frame=f)
    beam_sos.keyframe_insert(data_path="rotation_quaternion", frame=f)
    beam_sos.keyframe_insert(data_path="scale", frame=f)
    
    if spot_bed:
        if fd['hit_mirror']:
            spot_bed.scale = (0.0, 0.0, 0.0)
        else:
            spot_bed.scale = (1.0, 1.0, 1.0)
            if spot_bed.parent:
                spot_bed.location = spot_bed.parent.matrix_world.inverted() @ fd['p_target']
            else:
                spot_bed.location = fd['p_target']
        spot_bed.keyframe_insert(data_path="location", frame=f)
        spot_bed.keyframe_insert(data_path="scale", frame=f)

# Loop frame (TOTAL_FRAMES + 1 equals frame 1)
fd0 = frames_data[0]
for obj, p_a, p_b, vis in [
    (beam_incident, fd0['p_diode'], fd0['p_prism_in'], True),
    (beam_glass, fd0['p_prism_in'], fd0['p_prism_out'], True),
    (beam_scan, fd0['p_prism_out'], fd0['p_target'], True),
    (beam_sos, fd0['p_target'], fd0['p_mirror_refl'], fd0['hit_mirror']),
]:
    set_beam_endpoints(obj, p_a, p_b, visible=vis)
    obj.keyframe_insert(data_path="location", frame=TOTAL_FRAMES + 1)
    obj.keyframe_insert(data_path="rotation_quaternion", frame=TOTAL_FRAMES + 1)
    obj.keyframe_insert(data_path="scale", frame=TOTAL_FRAMES + 1)

# -------------------------------------------------------------
# Part 6: Rotor 1/4-Turn (-90 deg) Rotation Setup
# Notice: prismholder002 is explicitly EXCLUDED and remains STATIC!
# -------------------------------------------------------------

# Clear any animation on static prism holder
ph = bpy.data.objects.get("prismholder002")
if ph:
    ph.animation_data_clear()
    ph.rotation_euler = (0.0, 0.0, 0.0)
    print("Explicitly ensured prismholder002 is static (no animation)!")

rotor_names = [
    "pcbmotor_polygon_prism",
    "motorhead001",
    "motor_ring002",
    "polygonsupport003",
    "pcbmotor_rotor_magnetholder",
    "pcbmotor_rotor_magnets"
]

angle_start = -math.radians(44.4)
angle_end = angle_start - math.pi / 2.0

for name in rotor_names:
    obj = bpy.data.objects.get(name)
    if not obj:
        continue
    obj.animation_data_clear()
    obj.rotation_mode = 'XYZ'
    
    obj.rotation_euler.z = angle_start
    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    
    obj.rotation_euler.z = angle_end
    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=TOTAL_FRAMES + 1)
    
    try:
        if obj.animation_data and obj.animation_data.action:
            for fc in getattr(obj.animation_data.action, 'fcurves', []):
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
    except Exception:
        pass

print("Successfully baked 120-frame animation for rotor and laser beams (prismholder002 static)!")

# -------------------------------------------------------------
# Part 7: Cleanup & Filtering for Clean WebGL Export
# -------------------------------------------------------------

for h_name in ["Laser_Beam_Air", "Laser_Beam_Glass", "Laser_Scan_Sheet", "Web_Laser_Beam_Fan"]:
    h_obj = bpy.data.objects.get(h_name)
    if h_obj:
        h_obj.hide_render = True
        h_obj.hide_set(True)

EXCLUDE_COLLECTIONS = [
    "Cameras",
    "Lighting",
    "Studio_Setup",
    "Option_PCB_Motor",
    "SMD_Components_PCB_Motor",
]
objects_to_export = []

for obj in bpy.data.objects:
    in_excluded = any(
        col.name in EXCLUDE_COLLECTIONS or col.hide_render
        for col in obj.users_collection
    )
    if in_excluded or obj.hide_render or obj.name == "motorpcb002":
        obj.hide_set(True)
        continue
        
    if obj.type in ['MESH', 'CURVE']:
        objects_to_export.append(obj)

print(f"Total objects selected for export: {len(objects_to_export)}")

# -------------------------------------------------------------
# Part 7b: Geometry Decimation for Mobile / iOS WebKit Stability
# Reduces scene from 4.8M vertices down to ~700k without affecting optical fidelity
# -------------------------------------------------------------
img_artwork = bpy.data.images.get('PCB_Gerber_Artwork')
if img_artwork and (img_artwork.size[0] > 1024 or img_artwork.size[1] > 1024):
    scale = min(1024 / img_artwork.size[0], 1024 / img_artwork.size[1])
    img_artwork.scale(max(1, int(img_artwork.size[0] * scale)), max(1, int(img_artwork.size[1] * scale)))
    print(f"Rescaled PCB_Gerber_Artwork to {img_artwork.size[:]} for mobile performance")

HIGH_POLY_DECIMATE = {
    'bldcstator_coils': 0.08,
    'stepper_motor_nema17': 0.12,
    'leadscrew_T8': 0.15,
    'motorhead001': 0.30,
    'stepper_motor_Z_axis': 0.20,
    'ESP32-S3': 0.30,
    'leadscrew_end_bearing_mount': 0.05,
    'GUNCAIZHU_Ventilator': 0.15,
    'hardware_10x10mm': 0.30,
}

for obj in objects_to_export:
    if obj.type == 'MESH' and obj.data:
        v_count = len(obj.data.vertices)
        if any(k in obj.name.lower() for k in ['prism', 'mirror', 'lens', 'beam', 'ring', 'diode', 'laser', 'ffc']):
            continue  # NEVER decimate optical precision parts or delicate connectors
        
        matched_ratio = None
        for key, r in HIGH_POLY_DECIMATE.items():
            if obj.name.startswith(key):
                matched_ratio = r
                break
        
        if matched_ratio is not None:
            ratio = matched_ratio
        elif v_count > 25000:
            ratio = max(0.10, 5000.0 / v_count)
        elif v_count > 6000:
            ratio = max(0.25, 3000.0 / v_count)
        else:
            ratio = None
            
        if ratio is not None:
            mod = obj.modifiers.new(name="WebDecimate", type='DECIMATE')
            mod.decimate_type = 'COLLAPSE'
            mod.ratio = ratio
            print(f"Decimating '{obj.name}' ({v_count} verts) with ratio {ratio:.2f}")

bpy.ops.object.select_all(action='DESELECT')
for obj in objects_to_export:
    obj.select_set(True)

# -------------------------------------------------------------
# Part 8: glTF Export with Draco & Unified Scene Animation
# -------------------------------------------------------------

print("Exporting GLTF with Draco compression and unified periodic animation...")
bpy.ops.export_scene.gltf(
    filepath=glb_path_io,
    export_format='GLB',
    use_selection=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=7,
    export_apply=True,
    export_animations=True,
    export_animation_mode='SCENE',
    export_anim_scene_split_object=False,
    export_materials='EXPORT',
    export_image_format='AUTO'
)

print(f"SUCCESS: Exported {glb_path_io}")
file_size_mb = os.path.getsize(glb_path_io) / (1024 * 1024)
print(f"GLB File Size: {file_size_mb:.2f} MB")

shutil.copyfile(glb_path_io, glb_path_docs)
shutil.copyfile(glb_path_io, glb_path_cad)
print("Synchronized GLB to all target locations:")
print(f"  -> {glb_path_io}")
print(f"  -> {glb_path_docs}")
print(f"  -> {glb_path_cad}")

print("=== Finished Hexastorm Web Model Exporter ===")
