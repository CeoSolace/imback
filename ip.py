import bpy
import os
import math
import sys
import shutil

# ————————————————————————————————————————
# CONFIGURATION
# ————————————————————————————————————————
LOGO_PATH = "CVPRk7F2_400x400.jpg"
OUTPUT_DIR = os.path.expanduser("~/youtube_imback")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "imback.mp4")
RES_X, RES_Y = 1920, 1080
FPS = 30
RENDER_FRAMES = 70  # Only render 70 frames
TOTAL_FRAMES = 150  # 150 frames = 5 seconds

# Resolve logo path
if not os.path.isabs(LOGO_PATH):
    LOGO_PATH = os.path.abspath(LOGO_PATH)
if not os.path.exists(LOGO_PATH):
    print(f"❌ ERROR: Logo not found at {LOGO_PATH}")
    sys.exit(1)

# ————————————————————————————————————————
# RESET SCENE
# ————————————————————————————————————————
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = RENDER_FRAMES
scene.render.image_settings.file_format = 'PNG'

eevee = scene.eevee
eevee.use_bloom = True
eevee.bloom_threshold = 0.8
eevee.bloom_intensity = 0.6
eevee.use_ssr = True
eevee.use_gtao = True
eevee.use_soft_shadows = True
eevee.taa_samples = 16

# ————————————————————————————————————————
# ROAD
# ————————————————————————————————————————
road = bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -0.01))
road_obj = bpy.context.active_object
road_obj.scale = (30, 3, 1)  # narrower road
road_mat = bpy.data.materials.new("RoadMat")
road_mat.use_nodes = True
bsdf = road_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.12, 1)
bsdf.inputs['Roughness'].default_value = 0.9
road_obj.data.materials.append(road_mat)

# ————————————————————————————————————————
# CAMERA
# ————————————————————————————————————————
cam = bpy.ops.object.camera_add(location=(0, -10, 1.5), rotation=(math.radians(90), 0, 0))
camera = bpy.context.active_object
scene.camera = camera

camera.location = (0, -10, 1.5)
camera.rotation_euler = (math.radians(90), 0, 0)
camera.keyframe_insert("location", frame=1)
camera.keyframe_insert("rotation_euler", frame=1)

camera.location = (0, 0, 1.5)
camera.rotation_euler = (math.radians(90), 0, math.radians(-30))
camera.keyframe_insert("location", frame=30)
camera.keyframe_insert("rotation_euler", frame=30)

camera.location = (7, 0, 1.5)
camera.rotation_euler = (math.radians(90), 0, math.radians(-90))
camera.keyframe_insert("location", frame=60)
camera.keyframe_insert("rotation_euler", frame=60)

camera.location = (7, 0, 1.5)
camera.rotation_euler = (math.radians(90), 0, math.radians(-90))
camera.keyframe_insert("location", frame=70)
camera.keyframe_insert("rotation_euler", frame=70)

# ————————————————————————————————————————
# MAIN MONKEY
# ————————————————————————————————————————
monkey = bpy.ops.mesh.primitive_monkey_add(size=0.8, location=(7.5, 0, 0.4))
monkey_obj = bpy.context.active_object
monkey_obj.name = "MainMonkey"

monkey_obj.shape_key_add(name="Basis", from_mix=False)
sk_smirk = monkey_obj.shape_key_add(name="Smirk_Left", from_mix=False)
sk_tilt = monkey_obj.shape_key_add(name="Head_Tilt", from_mix=False)

for i, v in enumerate(monkey_obj.data.vertices):
    if v.co.x > 0.4 and abs(v.co.y) < 0.1 and v.co.z < -0.1:
        sk_smirk.data[i].co.z += 0.02
    if v.co.z > 0:
        sk_tilt.data[i].co.x += v.co.z * 0.03

monkey_mat = bpy.data.materials.new("MonkeyMat")
monkey_mat.use_nodes = True
bsdf = monkey_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1)
monkey_obj.data.materials.append(monkey_mat)

if monkey_obj.data.shape_keys:
    kb = monkey_obj.data.shape_keys.key_blocks
    kb["Smirk_Left"].value = 0
    kb["Head_Tilt"].value = 0
    kb["Smirk_Left"].keyframe_insert("value", frame=60)
    kb["Head_Tilt"].keyframe_insert("value", frame=60)
    kb["Smirk_Left"].value = 1
    kb["Head_Tilt"].value = 1
    kb["Smirk_Left"].keyframe_insert("value", frame=65)
    kb["Head_Tilt"].keyframe_insert("value", frame=65)
    kb["Smirk_Left"].keyframe_insert("value", frame=70)
    kb["Head_Tilt"].keyframe_insert("value", frame=70)

# ————————————————————————————————————————
# TEXT: “Im Back”
# ————————————————————————————————————————
text_obj = bpy.ops.object.text_add(location=(9, 0, 0.5))
text = bpy.context.active_object
text.name = "ImBackText"
text.data.body = "Im Back"
text.data.size = 1.5
text.data.align_x = 'LEFT'
text.data.extrude = 0.05

text_mat = bpy.data.materials.new("TextMat")
text_mat.use_nodes = True
nodes = text_mat.node_tree.nodes
links = text_mat.node_tree.links
nodes.clear()

out = nodes.new('ShaderNodeOutputMaterial')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
emi = nodes.new('ShaderNodeEmission')
mix = nodes.new('ShaderNodeMixShader')

bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
bsdf.inputs['Roughness'].default_value = 0.1
bsdf.inputs['Metallic'].default_value = 0.9

emi.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1)
emi.inputs['Strength'].default_value = 2.0

mix.inputs[0].default_value = 0.3
links.new(bsdf.outputs['BSDF'], mix.inputs[1])
links.new(emi.outputs['Emission'], mix.inputs[2])
links.new(mix.outputs['Shader'], out.inputs['Surface'])

text.data.materials.append(text_mat)

# ————————————————————————————————————————
# HOLOGRAM
# ————————————————————————————————————————
holo = bpy.ops.mesh.primitive_plane_add(size=1, location=(10.5, 0, 0.5))
holo_obj = bpy.context.active_object
holo_obj.name = "CoveX_Hologram"

holo_mat = bpy.data.materials.new("HologramMat")
holo_mat.use_nodes = True
holo_mat.blend_method = 'BLEND'
nodes = holo_mat.node_tree.nodes
links = holo_mat.node_tree.links
nodes.clear()

out = nodes.new('ShaderNodeOutputMaterial')
emi = nodes.new('ShaderNodeEmission')
img = nodes.new('ShaderNodeTexImage')
img.image = bpy.data.images.load(LOGO_PATH)

links.new(img.outputs['Color'], emi.inputs['Color'])
emi.inputs['Strength'].default_value = 5.0
links.new(emi.outputs['Emission'], out.inputs['Surface'])

holo_obj.data.materials.append(holo_mat)

for f in [60, 65, 70]:
    emi.inputs['Strength'].default_value = 5.0 if f == 65 else 3.0
    emi.inputs['Strength'].keyframe_insert("default_value", frame=f)

# ————————————————————————————————————————
# LIGHTS
# ————————————————————————————————————————
sun = bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun_light = bpy.context.active_object
sun_light.data.energy = 1.5

rim = bpy.ops.object.light_add(type='AREA', location=(-5, 0, 2))
rim_light = bpy.context.active_object
rim_light.data.energy = 300
rim_light.rotation_euler = (0, math.radians(90), 0)

fill = bpy.ops.object.light_add(type='AREA', location=(5, 0, 2))
fill_light = bpy.context.active_object
fill_light.data.energy = 200

# ————————————————————————————————————————
# RENDER 70 FRAMES
# ————————————————————————————————————————
print(f"🎬 Rendering {RENDER_FRAMES} frames to {OUTPUT_DIR}...")

for frame in range(1, RENDER_FRAMES + 1):
    scene.frame_set(frame)
    filepath = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"✅ Frame {frame} saved")

# ————————————————————————————————————————
# EXTEND TO 150 FRAMES (5 SECONDS)
# ————————————————————————————————————————
print("⏳ Extending final frame to reach 5 seconds (150 frames)...")
last_frame_path = os.path.join(OUTPUT_DIR, "frame_0070.png")
for i in range(RENDER_FRAMES + 1, TOTAL_FRAMES + 1):
    new_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
    shutil.copy2(last_frame_path, new_path)

# ————————————————————————————————————————
# ENCODE TO MP4
# ————————————————————————————————————————
try:
    import subprocess
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-framerate', str(FPS),
        '-i', os.path.join(OUTPUT_DIR, 'frame_%04d.png'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'fast',
        '-crf', '18',
        OUTPUT_MP4
    ]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ SUCCESS! Video saved to:\n{OUTPUT_MP4}")
except Exception as e:
    print(f"⚠️  FFmpeg encoding failed: {e}")
    print(f"📁 Raw frames saved in: {OUTPUT_DIR}")
