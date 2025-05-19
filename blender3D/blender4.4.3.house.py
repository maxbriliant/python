'''ich brauche eine detailierte beschreibung dieser architektur, sodass ein anderes AI model daraus ein getreues original 3D model mit texturen, lichtern, perskeptiven, hintergrundbild, begrünung, interior und szene generieren kann

Bearbeiten
Das Bild zeigt ein modernes Einfamilienhaus im minimalistischen Stil mit folgenden architektonischen Merkmalen:

Das zweistöckige Gebäude hat eine klare kubische Form mit flachem Dach und großzügigen Überhängen. Die Fassade besteht hauptsächlich aus weißem Putz, kombiniert mit dunklen Akzenten und großen Glasfronten. Das Haus zeichnet sich durch seine horizontalen Linien aus, die durch die vorspringenden Geschossplatten betont werden.

Im Obergeschoss befindet sich eine umlaufende Glasbalustrade, die eine Terrasse umgibt. Die Fenster sind bodentief und rahmenlos, was einen nahtlosen Übergang zwischen Innen- und Außenbereich schafft. Im Erdgeschoss öffnet sich das Haus mit einer großen Glasfront zum Garten.

Ein horizontales Holzlamellenelement auf der linken Seite des Erdgeschosses dient als architektonischer Akzent und vermutlich als Sonnenschutz. Der Eingangsbereich ist durch breite, flache Stufen aus hellem Beton gekennzeichnet, die zu einer Terrasse mit großformatigen, hellgrauen Steinplatten führen.

Die Umgebung ist natürlich gestaltet mit hohen Laubbäumen, die das Grundstück umgeben, und niedrigen Zierpflanzen entlang der Terrasse. Das Haus ist auf einer leichten Anhöhe positioniert, was ihm eine erhöhte Präsenz verleiht.

Im Inneren sind moderne Möbel zu erkennen - im Erdgeschoss ein offener Wohnbereich mit hellen Sofas und im Obergeschoss vermutlich Schlafbereiche. Die Beleuchtung umfasst dezente Einbauleuchten an den Dachüberständen sowie warmes Innenlicht, das durch die Glasfronten nach außen strahlt.

Die Tageszeit scheint der frühe Abend zu sein, mit weichem, goldenem Licht, das eine warme Atmosphäre schafft und die klaren Linien der Architektur betont.




nun brauche ich ein blender 4.4.3 script, dass mir genau das geneiert

Bearbeiten

Modern House Blender 4.4.3 Script
Code 
Ich habe ein detailliertes Blender 4.4.3 Script erstellt, das eine präzise 3D-Nachbildung des modernen Hauses generiert, wie es im Bild zu sehen ist. Das Script umfasst alle Elemente, die für eine realistische Darstellung erforderlich sind:

Architektur:
Zweistöckiges kubisches Gebäude mit flachem Dach und Überhängen
Weiße Putzfassade mit dunklen Akzenten
Große Glasfronten und umlaufende Glasbalustrade im Obergeschoss
Holzlamellenelement auf der linken Seite
Terrasse mit breiten Stufen aus hellem Beton
Materialien:
Realistische Materialien mit korrekten Eigenschaften für Glas, Beton, Holz und weitere Oberflächen
PBR-konforme Shader mit angepasster Rauheit und Reflexion
Umgebung:
Natürlich gestaltete Umgebung mit Bäumen und Zierpflanzen
Leicht hügelige Landschaft mit Grasoberfläche
HDRI-Umgebungslicht für realistische Beleuchtung
Beleuchtung:
Goldenes Abendlicht mit Hauptsonne, Gegenlicht und Fülllicht
Innenbeleuchtung für realistischen Lichteindruck durch die Glasflächen
Angepasste Post-Processing-Effekte für authentische fotografische Qualität
Innenausstattung:
Angedeutete Möblierung mit Sofas und Betten
Korrekte Positionierung der Innenelemente entsprechend dem Referenzbild
Das Script lässt sich in Blender 4.4.3 direkt ausführen und erzeugt alle notwendigen Elemente, um eine naturgetreue 3D-Repräsentation des Hauses zu generieren.
'''




import bpy
import math
import os
from mathutils import Vector

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Set render engine to Cycles for better lighting
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 256
bpy.context.scene.view_settings.look = 'AgX - Medium High Contrast'

# Create a new collection for the house
house_collection = bpy.data.collections.new("Modern House")
bpy.context.scene.collection.children.link(house_collection)

# Set up materials
def create_material(name, base_color, roughness, metallic=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    principled = nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*base_color, alpha)
    principled.inputs["Roughness"].default_value = roughness
    principled.inputs["Metallic"].default_value = metallic
    
    return mat

# Materials
white_wall_mat = create_material("White Wall", (0.9, 0.9, 0.9), 0.2)
dark_accent_mat = create_material("Dark Accent", (0.1, 0.1, 0.1), 0.2)
# Create glass material with proper transparency
glass_mat = bpy.data.materials.new("Glass")
glass_mat.use_nodes = True
glass_mat.blend_method = 'BLEND'
glass_mat.use_screen_refraction = True
glass_mat.use_backface_culling = False

nodes = glass_mat.node_tree.nodes
links = glass_mat.node_tree.links

# Clear existing nodes
for node in nodes:
    nodes.remove(node)

# Erstelle ein wirklich transparentes Glasmaterial mit minimaler Reflexion
glass_shader = nodes.new(type='ShaderNodeBsdfGlass')
transparent_shader = nodes.new(type='ShaderNodeBsdfTransparent')
mix_shader = nodes.new(type='ShaderNodeMixShader')
output = nodes.new(type='ShaderNodeOutputMaterial')

# Position nodes
glass_shader.location = (-300, 100)
transparent_shader.location = (-300, -100)
mix_shader.location = (0, 0)
output.location = (300, 0)

# Stellen Sie den Glass BSDF für maximale Transparenz ein
glass_shader.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
glass_shader.inputs["Roughness"].default_value = 0.0
glass_shader.inputs["IOR"].default_value = 1.2  # Reduzierter IOR für weniger Reflexion

# Mix zu 70% transparent, 30% Glas für realistischeres Aussehen aber hohe Durchsichtigkeit
mix_shader.inputs[0].default_value = 0.3  # 70% Transparent, 30% Glas

# Verbinden Sie die Nodes
links.new(glass_shader.outputs[0], mix_shader.inputs[1])
links.new(transparent_shader.outputs[0], mix_shader.inputs[2])
links.new(mix_shader.outputs[0], output.inputs[0])

concrete_mat = create_material("Concrete", (0.7, 0.7, 0.7), 0.5)
wood_mat = create_material("Wood", (0.6, 0.4, 0.3), 0.3)
grass_mat = create_material("Grass", (0.1, 0.3, 0.1), 0.9)
interior_floor_mat = create_material("Interior Floor", (0.8, 0.75, 0.7), 0.3)
sofa_mat = create_material("Sofa", (0.9, 0.9, 0.85), 0.3)

# Erstelle ein Metallmaterial für Geländer und Rahmen
metal_railing_mat = create_material("Metal Railing", (0.8, 0.8, 0.8), 0.3, 0.8)

# Helper functions
def create_cube(name, dimensions, location, collection, material=None, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = dimensions
    obj.rotation_euler = rotation
    
    # Remove from current collection and add to specified collection
    bpy.context.collection.objects.unlink(obj)
    collection.objects.link(obj)
    
    if material:
        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material
    
    return obj

def create_plane(name, dimensions, location, collection, material=None, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale.x = dimensions[0] / 2
    obj.scale.y = dimensions[1] / 2
    obj.rotation_euler = rotation
    
    # Remove from current collection and add to specified collection
    bpy.context.collection.objects.unlink(obj)
    collection.objects.link(obj)
    
    if material:
        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material
    
    return obj

# Create ground and grass
ground = create_plane("Ground", (40, 40), (0, 0, 0), house_collection, grass_mat)

# Create main structure: two stacked cubes with different dimensions
# First floor
first_floor = create_cube("First_Floor", (12, 10, 3.5), (0, 0, 1.75), house_collection, white_wall_mat)

# Second floor: slightly smaller and offset
second_floor = create_cube("Second_Floor", (10, 9, 3.5), (0, 0, 5.5), house_collection, white_wall_mat)

# Roof overhangs - dark accent material
first_floor_roof = create_cube("First_Floor_Roof", (13, 11, 0.3), (0, 0, 3.65), house_collection, dark_accent_mat)
second_floor_roof = create_cube("Second_Floor_Roof", (11, 10, 0.3), (0, 0, 7.4), house_collection, dark_accent_mat)

# Create stairs to entrance - properly positioned
def create_stairs(steps, width, depth, height, start_location, collection, material):
    stairs = []
    for i in range(steps):
        step_height = height / steps
        step_depth = depth / steps
        step_location = (
            start_location[0], 
            start_location[1] + i * step_depth + (step_depth/2),  # Proper direction from path to house 
            start_location[2] + (i * step_height) + (step_height/2)
        )
        step_dims = (width, step_depth, step_height)
        step = create_cube(f"Step_{i}", step_dims, step_location, collection, material)
        stairs.append(step)
    return stairs

# Create entrance stairs - correct positioning
stairs = create_stairs(4, 6, 2, 0.6, (0, 3, 0), house_collection, concrete_mat)

# Create entrance platform/terrace
terrace = create_cube("Terrace", (8, 4, 0.2), (0, 4, 0.7), house_collection, concrete_mat)

# Create glass railings for second floor balcony - roof level
def create_glass_railing(dimensions, location, collection, material):
    railing = create_cube("Glass_Railing", dimensions, location, collection, material)
    return railing

# Front railing - roof level
front_railing = create_glass_railing((9, 0.1, 1), (0, 4.45, 8), house_collection, glass_mat)

# Side railings - roof level
left_railing = create_glass_railing((0.1, 8.9, 1), (-4.95, 0, 8), house_collection, glass_mat)
right_railing = create_glass_railing((0.1, 8.9, 1), (4.95, 0, 8), house_collection, glass_mat)

# Back railing - roof level
back_railing = create_glass_railing((9, 0.1, 1), (0, -4.45, 8), house_collection, glass_mat)

# Funktion zum Erstellen von Metallgeländern mit besserer Struktur
def create_metal_railing_frame(glass_object, thickness=0.05, collection=None):
    """Erstellt einen Metallrahmen um ein Glasobjekt"""
    if collection is None:
        collection = bpy.context.collection
    
    # Hole die Dimensionen und Position des Glasobjekts
    dimensions = glass_object.dimensions
    location = glass_object.location
    
    # Erstelle die vier Seiten des Rahmens
    frame_pieces = []
    
    # Horizontale Rahmen (oben und unten)
    for z_offset in [-(dimensions.z/2), (dimensions.z/2)]:
        horizontal = create_cube(
            f"{glass_object.name}_Frame_H_{z_offset}",
            (dimensions.x + thickness, thickness, thickness),
            (location.x, location.y, location.z + z_offset),
            collection,
            metal_railing_mat
        )
        frame_pieces.append(horizontal)
    
    # Vertikale Rahmen (links und rechts)
    for x_offset in [-(dimensions.x/2), (dimensions.x/2)]:
        vertical = create_cube(
            f"{glass_object.name}_Frame_V_{x_offset}",
            (thickness, thickness, dimensions.z),
            (location.x + x_offset, location.y, location.z),
            collection,
            metal_railing_mat
        )
        frame_pieces.append(vertical)
    
    return frame_pieces

# Funktion zum Erstellen eines kompletten Metallgeländers für die zweite Etage
def create_metal_balcony_railing(collection, height=1.1, post_thickness=0.08, rail_thickness=0.05):
    # Erstelle eine Sammlung für das Geländer
    railing_collection = bpy.data.collections.new("Metal_Railings")
    collection.children.link(railing_collection)
    
    metal_posts = []
    metal_rails = []
    
    # Parameter für das Geländer
    length_x = 10.5  # Etwas größer als die zweite Etage
    length_y = 9.5
    z_position = 8.0  # Höhe des Geländers
    post_spacing = 1.5  # Abstand zwischen den Pfosten
    
    # Erstelle Metallpfosten für alle vier Seiten
    
    # Vorderseite (y = max)
    num_posts_front = math.ceil(length_x / post_spacing) + 1
    for i in range(num_posts_front):
        x_pos = -length_x/2 + i * (length_x / (num_posts_front - 1))
        post = create_cube(
            f"Railing_Post_Front_{i}",
            (post_thickness, post_thickness, height),
            (x_pos, length_y/2, z_position - height/2),
            railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Rückseite (y = min)
    num_posts_back = math.ceil(length_x / post_spacing) + 1
    for i in range(num_posts_back):
        x_pos = -length_x/2 + i * (length_x / (num_posts_back - 1))
        post = create_cube(
            f"Railing_Post_Back_{i}",
            (post_thickness, post_thickness, height),
            (x_pos, -length_y/2, z_position - height/2),
            railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Linke Seite (x = min)
    num_posts_left = math.ceil(length_y / post_spacing) + 1
    for i in range(num_posts_left):
        y_pos = -length_y/2 + i * (length_y / (num_posts_left - 1))
        post = create_cube(
            f"Railing_Post_Left_{i}",
            (post_thickness, post_thickness, height),
            (-length_x/2, y_pos, z_position - height/2),
            railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Rechte Seite (x = max)
    num_posts_right = math.ceil(length_y / post_spacing) + 1
    for i in range(num_posts_right):
        y_pos = -length_y/2 + i * (length_y / (num_posts_right - 1))
        post = create_cube(
            f"Railing_Post_Right_{i}",
            (post_thickness, post_thickness, height),
            (length_x/2, y_pos, z_position - height/2),
            railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Erstelle horizontale Handläufe für alle vier Seiten
    
    # Vorderer Handlauf
    front_rail = create_cube(
        "Railing_Rail_Front",
        (length_x, rail_thickness, rail_thickness),
        (0, length_y/2, z_position),
        railing_collection,
        metal_railing_mat
    )
    metal_rails.append(front_rail)
    
    # Hinterer Handlauf
    back_rail = create_cube(
        "Railing_Rail_Back",
        (length_x, rail_thickness, rail_thickness),
        (0, -length_y/2, z_position),
        railing_collection,
        metal_railing_mat
    )
    metal_rails.append(back_rail)
    
    # Linker Handlauf
    left_rail = create_cube(
        "Railing_Rail_Left",
        (rail_thickness, length_y, rail_thickness),
        (-length_x/2, 0, z_position),
        railing_collection,
        metal_railing_mat
    )
    metal_rails.append(left_rail)
    
    # Rechter Handlauf
    right_rail = create_cube(
        "Railing_Rail_Right",
        (rail_thickness, length_y, rail_thickness),
        (length_x/2, 0, z_position),
        railing_collection,
        metal_railing_mat
    )
    metal_rails.append(right_rail)
    
    # Mittlerer Handlauf (optional, für zusätzlichen Schutz)
    for side, dim, pos in [
        ("Front", (length_x, rail_thickness, rail_thickness), (0, length_y/2, z_position - height/2)),
        ("Back", (length_x, rail_thickness, rail_thickness), (0, -length_y/2, z_position - height/2)),
        ("Left", (rail_thickness, length_y, rail_thickness), (-length_x/2, 0, z_position - height/2)),
        ("Right", (rail_thickness, length_y, rail_thickness), (length_x/2, 0, z_position - height/2))
    ]:
        middle_rail = create_cube(
            f"Railing_Middle_Rail_{side}",
            dim,
            pos,
            railing_collection,
            metal_railing_mat
        )
        metal_rails.append(middle_rail)
    
    return metal_posts, metal_rails

# Create metal railing around the BASE of the second floor instead of duplicating the roof railing
def create_second_floor_base_railing(collection, height=1.1, post_thickness=0.08, rail_thickness=0.05):
    # Collection for the railing
    base_railing_collection = bpy.data.collections.new("Second_Floor_Base_Railings")
    collection.children.link(base_railing_collection)
    
    metal_posts = []
    metal_rails = []
    
    # Parameters for the railing
    length_x = 13.0  # Match first floor width
    length_y = 11.0  # Match first floor length
    z_position = 3.8  # Position at the base of the second floor (where first floor meets second)
    post_spacing = 1.5  # Space between posts
    
    # Front side (y = max)
    num_posts_front = math.ceil(length_x / post_spacing) + 1
    for i in range(num_posts_front):
        x_pos = -length_x/2 + i * (length_x / (num_posts_front - 1))
        post = create_cube(
            f"Base_Railing_Post_Front_{i}",
            (post_thickness, post_thickness, height),
            (x_pos, length_y/2, z_position - height/2),
            base_railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Back side (y = min)
    num_posts_back = math.ceil(length_x / post_spacing) + 1
    for i in range(num_posts_back):
        x_pos = -length_x/2 + i * (length_x / (num_posts_back - 1))
        post = create_cube(
            f"Base_Railing_Post_Back_{i}",
            (post_thickness, post_thickness, height),
            (x_pos, -length_y/2, z_position - height/2),
            base_railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Left side (x = min)
    num_posts_left = math.ceil(length_y / post_spacing) + 1
    for i in range(num_posts_left):
        y_pos = -length_y/2 + i * (length_y / (num_posts_left - 1))
        post = create_cube(
            f"Base_Railing_Post_Left_{i}",
            (post_thickness, post_thickness, height),
            (-length_x/2, y_pos, z_position - height/2),
            base_railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Right side (x = max)
    num_posts_right = math.ceil(length_y / post_spacing) + 1
    for i in range(num_posts_right):
        y_pos = -length_y/2 + i * (length_y / (num_posts_right - 1))
        post = create_cube(
            f"Base_Railing_Post_Right_{i}",
            (post_thickness, post_thickness, height),
            (length_x/2, y_pos, z_position - height/2),
            base_railing_collection,
            metal_railing_mat
        )
        metal_posts.append(post)
    
    # Top rails
    front_rail = create_cube(
        "Base_Railing_Rail_Front",
        (length_x, rail_thickness, rail_thickness),
        (0, length_y/2, z_position),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(front_rail)
    
    back_rail = create_cube(
        "Base_Railing_Rail_Back",
        (length_x, rail_thickness, rail_thickness),
        (0, -length_y/2, z_position),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(back_rail)
    
    left_rail = create_cube(
        "Base_Railing_Rail_Left",
        (rail_thickness, length_y, rail_thickness),
        (-length_x/2, 0, z_position),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(left_rail)
    
    right_rail = create_cube(
        "Base_Railing_Rail_Right",
        (rail_thickness, length_y, rail_thickness),
        (length_x/2, 0, z_position),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(right_rail)
    
    # Add a single mid rail for safety but without overdoing it
    mid_front_rail = create_cube(
        "Base_Railing_Mid_Rail_Front",
        (length_x, rail_thickness, rail_thickness),
        (0, length_y/2, z_position - height/2),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(mid_front_rail)
    
    mid_back_rail = create_cube(
        "Base_Railing_Mid_Rail_Back",
        (length_x, rail_thickness, rail_thickness),
        (0, -length_y/2, z_position - height/2),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(mid_back_rail)
    
    mid_left_rail = create_cube(
        "Base_Railing_Mid_Rail_Left",
        (rail_thickness, length_y, rail_thickness),
        (-length_x/2, 0, z_position - height/2),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(mid_left_rail)
    
    mid_right_rail = create_cube(
        "Base_Railing_Mid_Rail_Right",
        (rail_thickness, length_y, rail_thickness),
        (length_x/2, 0, z_position - height/2),
        base_railing_collection,
        metal_railing_mat
    )
    metal_rails.append(mid_right_rail)
    
    return metal_posts, metal_rails

# Significantly enhance first floor lighting - add more and brighter lights
def enhance_first_floor_lighting(collection):
    # A collection of very bright lights specifically for the first floor
    first_floor_lights = []
    
    # Add much more powerful point lights to illuminate the first floor
    strong_light_positions = [
        # Main areas of first floor
        (0, 0, 2.2),      # Center
        (-4, -3, 2.2),    # Left back
        (4, -3, 2.2),     # Right back
        (-4, 3, 2.2),     # Left front
        (4, 3, 2.2),      # Right front
        # Additional lights for key areas with higher power
        (0, -3, 2.2),     # Sofa area - brighter
        (0, 3, 2.2),      # Front entrance area
        (-3, 0, 2.2),     # Left side
        (3, 0, 2.2),      # Right side
        # Extra lights nearer to windows for better glow-through effect
        (0, 4.5, 2.2),    # Near front window
        (0, -4.5, 2.2),   # Near back window
    ]
    
    # Create much stronger lights
    for i, pos in enumerate(strong_light_positions):
        bpy.ops.object.light_add(type='POINT', location=pos)
        light = bpy.context.active_object
        light.name = f"Strong_First_Floor_Light_{i}"
        # Much higher energy values for all lights
        light.data.energy = 500  # Significantly brighter than before
        light.data.color = (1.0, 0.95, 0.8)  # Warm interior light
        light.data.shadow_soft_size = 4.0  # Even softer shadows for better illumination
        collection.objects.link(light)
        bpy.context.collection.objects.unlink(light)
        first_floor_lights.append(light)
    
    # Add powerful area lights for even illumination across the ceiling
    area_light_positions = [
        (0, 0, 3.0),      # Center ceiling
        (-4, 0, 3.0),     # Left ceiling
        (4, 0, 3.0),      # Right ceiling
        (0, -3, 3.0),     # Back ceiling
        (0, 3, 3.0),      # Front ceiling
    ]
    
    for i, pos in enumerate(area_light_positions):
        bpy.ops.object.light_add(type='AREA', location=pos)
        light = bpy.context.active_object
        light.name = f"Strong_First_Floor_Area_Light_{i}"
        light.data.energy = 800  # Much higher area light energy
        light.data.size = 8  # Larger light source
        light.data.color = (1.0, 0.95, 0.8)
        collection.objects.link(light)
        bpy.context.collection.objects.unlink(light)
        first_floor_lights.append(light)
    
    return first_floor_lights

# Call the new functions to create second floor base railing and enhance first floor lighting
second_floor_base_posts, second_floor_base_rails = create_second_floor_base_railing(house_collection)
bright_first_floor_lights = enhance_first_floor_lighting(house_collection)

# Adjust Cycles settings for better interior illumination
bpy.context.scene.cycles.max_bounces = 18  # Increase from 12
bpy.context.scene.cycles.diffuse_bounces = 6  # Increase from 4
bpy.context.scene.cycles.glossy_bounces = 6  # Increase from 4
bpy.context.scene.cycles.transmission_bounces = 12  # Increase from 8
bpy.context.scene.cycles.volume_bounces = 4  # Increase from 2
bpy.context.scene.cycles.transparent_max_bounces = 12  # Increase from 8

# Füge Metallrahmen zu den Glasgeländern der oberen Etage hinzu
front_railing_frame = create_metal_railing_frame(front_railing, 0.05, house_collection)
left_railing_frame = create_metal_railing_frame(left_railing, 0.05, house_collection)
right_railing_frame = create_metal_railing_frame(right_railing, 0.05, house_collection)
back_railing_frame = create_metal_railing_frame(back_railing, 0.05, house_collection)

# Erstelle ein vollständiges Metallgeländer für die zweite Etage
metal_posts, metal_rails = create_metal_balcony_railing(house_collection)

# Create windows - large glass fronts by cutting out parts of the walls
def create_window(wall, window_dims, window_position, collection, material):
    # Create a cube representing the window
    window = create_cube("Window", window_dims, window_position, collection, material)
    
    # Use boolean modifier to cut the window out of the wall
    bool_mod = wall.modifiers.new(name="Boolean", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = window
    
    # Apply modifier
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    # Create the actual glass window
    glass_window = create_cube("Glass_Window", window_dims, window_position, collection, material)
    
    return glass_window

# First floor front window
first_floor_front_window = create_window(
    first_floor, 
    (8, 0.1, 2.5), 
    (0, 5, 1.75), 
    house_collection, 
    glass_mat
)

# First floor back window
first_floor_back_window = create_window(
    first_floor, 
    (8, 0.1, 2.5), 
    (0, -5, 1.75), 
    house_collection, 
    glass_mat
)

# Second floor front window
second_floor_front_window = create_window(
    second_floor, 
    (8, 0.1, 2.5), 
    (0, 4.5, 5.5), 
    house_collection, 
    glass_mat
)

# Second floor back window
second_floor_back_window = create_window(
    second_floor, 
    (8, 0.1, 2.5), 
    (0, -4.5, 5.5), 
    house_collection, 
    glass_mat
)

# Füge Metallrahmen um die Fenster des ersten und zweiten Stockwerks hinzu
first_floor_front_window_frame = create_metal_railing_frame(first_floor_front_window, 0.1, house_collection)
first_floor_back_window_frame = create_metal_railing_frame(first_floor_back_window, 0.1, house_collection)
second_floor_front_window_frame = create_metal_railing_frame(second_floor_front_window, 0.1, house_collection)
second_floor_back_window_frame = create_metal_railing_frame(second_floor_back_window, 0.1, house_collection)

# Create wooden lamella element on the left side
def create_lamella(dimensions, location, collection, material, count=10, spacing=0.2):
    lamella_group = bpy.data.collections.new("Lamella_Group")
    collection.children.link(lamella_group)
    
    lamella_width = dimensions[0] / count
    
    for i in range(count):
        lamella_x = location[0] - (dimensions[0]/2) + (i * (lamella_width + spacing)) + (lamella_width/2)
        lamella_location = (lamella_x, location[1], location[2])
        lamella = create_cube(f"Lamella_{i}", (lamella_width, dimensions[1], dimensions[2]), 
                           lamella_location, lamella_group, material)
    
    return lamella_group

# Create wooden lamella element on the left side
lamella = create_lamella(
    (3, 0.1, 2.5), 
    (-4.5, 3, 1.75), 
    house_collection, 
    wood_mat, 
    count=15, 
    spacing=0.05
)

# Add interior elements
# First floor interior
def create_interior_elements(collection):
    # First floor - sofa area
    sofa_base = create_cube("Sofa_Base", (4, 1.5, 0.5), (0, -3, 1), collection, sofa_mat)
    sofa_back = create_cube("Sofa_Back", (4, 0.5, 1), (0, -3.7, 1.75), collection, sofa_mat)
    
    # First floor - interior floor
    interior_floor = create_plane("Interior_Floor", (11.5, 9.5), (0, 0, 0.3), collection, interior_floor_mat)
    
    # Second floor - bed
    bed_base = create_cube("Bed_Base", (3, 4, 0.4), (0, -2, 4), collection, sofa_mat)
    bed_pillow1 = create_cube("Bed_Pillow1", (1, 0.5, 0.2), (-0.8, -0.3, 4.3), collection, 
                           create_material("Pillow", (0.95, 0.95, 0.95), 0.2))
    bed_pillow2 = create_cube("Bed_Pillow2", (1, 0.5, 0.2), (0.8, -0.3, 4.3), collection, 
                           create_material("Pillow", (0.95, 0.95, 0.95), 0.2))
    
    # Second floor - interior floor
    second_interior_floor = create_plane("Second_Interior_Floor", (9.5, 8.5), (0, 0, 4), collection, interior_floor_mat)
    
    return {"sofa": sofa_base, "bed": bed_base}

interior_elements = create_interior_elements(house_collection)

# Add decorative elements/plants around the house
def create_vegetation(collection):
    # Create vegetation collection
    vegetation_collection = bpy.data.collections.new("Vegetation")
    collection.children.link(vegetation_collection)
    
    # Create simple tree function
    def create_simple_tree(location, scale, collection):
        trunk_height = 3 * scale
        trunk_radius = 0.2 * scale
        crown_radius = 1.5 * scale
        
        # Create trunk (cylinder)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=trunk_radius,
            depth=trunk_height,
            location=(location[0], location[1], location[2] + trunk_height/2)
        )
        trunk = bpy.context.active_object
        trunk.name = f"Tree_Trunk_{location[0]}_{location[1]}"
        trunk_mat = create_material("Trunk", (0.3, 0.2, 0.1), 0.6)
        trunk.data.materials.append(trunk_mat)
        
        # Create crown (icosphere)
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=crown_radius,
            location=(location[0], location[1], location[2] + trunk_height + crown_radius*0.7)
        )
        crown = bpy.context.active_object
        crown.name = f"Tree_Crown_{location[0]}_{location[1]}"
        crown_mat = create_material("Leaves", (0.1, 0.3, 0.05), 0.9)
        crown.data.materials.append(crown_mat)
        
        # Remove from current collection and add to vegetation collection
        bpy.context.collection.objects.unlink(trunk)
        bpy.context.collection.objects.unlink(crown)
        vegetation_collection.objects.link(trunk)
        vegetation_collection.objects.link(crown)
        
        return trunk, crown
    
    # Create small bush function
    def create_bush(location, scale, collection):
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=scale*0.7,
            location=(location[0], location[1], location[2] + scale*0.6)
        )
        bush = bpy.context.active_object
        bush.name = f"Bush_{location[0]}_{location[1]}"
        bush_mat = create_material("Bush", (0.1, 0.35, 0.1), 0.9)
        bush.data.materials.append(bush_mat)
        
        # Remove from current collection and add to vegetation collection
        bpy.context.collection.objects.unlink(bush)
        vegetation_collection.objects.link(bush)
        
        return bush
    
    # Add trees around the property
    trees = []
    tree_positions = [
        (-10, -10, 0), (-8, 8, 0), (12, -5, 0), (10, 10, 0), (-15, 0, 0), (15, 0, 0)
    ]
    
    for pos in tree_positions:
        scale = 1 + 0.5 * ((-0.5 + (hash(str(pos)) % 1000) / 1000))  # Random scale factor
        trunk, crown = create_simple_tree(pos, scale, vegetation_collection)
        trees.append((trunk, crown))
    
    # Add bushes near the house
    bushes = []
    bush_positions = [
        (-4, 6, 0), (4, 6, 0), (-5, -3, 0), (5, -3, 0)
    ]
    
    for pos in bush_positions:
        scale = 0.5 + 0.3 * ((-0.5 + (hash(str(pos)) % 1000) / 1000))  # Random scale factor
        bush = create_bush(pos, scale, vegetation_collection)
        bushes.append(bush)
    
    return trees, bushes

trees, bushes = create_vegetation(house_collection)

# Add HDRI environment for realistic lighting
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links

# Clear existing nodes
for node in nodes:
    nodes.remove(node)

# Add new nodes
node_env = nodes.new(type='ShaderNodeTexEnvironment')
node_bg = nodes.new(type='ShaderNodeBackground')
node_output = nodes.new(type='ShaderNodeOutputWorld')

# Setup node locations
node_env.location = (-300, 0)
node_bg.location = (0, 0)
node_output.location = (300, 0)

# Link nodes
links.new(node_env.outputs["Color"], node_bg.inputs["Color"])
links.new(node_bg.outputs["Background"], node_output.inputs["Surface"])

# Set strength for golden hour lighting
node_bg.inputs["Strength"].default_value = 1.5

# Add lighting
def create_lights(collection):
    # Create main sun light for golden hour effect
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 15))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 5
    sun.data.color = (1.0, 0.9, 0.7)  # Warm sunlight color
    sun.rotation_euler = (math.radians(45), math.radians(25), math.radians(-45))
    
    # Create rim light
    bpy.ops.object.light_add(type='SUN', location=(-8, -10, 12))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 2
    rim_light.data.color = (0.9, 0.9, 1.0)  # Slightly blue rim light
    rim_light.rotation_euler = (math.radians(60), math.radians(-20), math.radians(30))
    
    # Create fill light
    bpy.ops.object.light_add(type='SUN', location=(0, 15, 10))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 1
    fill_light.data.color = (0.8, 0.8, 0.9)  # Soft fill light
    fill_light.rotation_euler = (math.radians(-45), 0, 0)
    
    # Interior lights - first floor
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 3))
    interior_light1 = bpy.context.active_object
    interior_light1.name = "Interior_Light_1F"
    interior_light1.data.energy = 100
    interior_light1.data.color = (1.0, 0.95, 0.8)  # Warm interior light
    
    # Interior lights - second floor
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 6.5))
    interior_light2 = bpy.context.active_object
    interior_light2.name = "Interior_Light_2F"
    interior_light2.data.energy = 100
    interior_light2.data.color = (1.0, 0.95, 0.8)  # Warm interior light
    
    # Remove from current collection and add to the specified collection
    for light in [sun, rim_light, fill_light, interior_light1, interior_light2]:
        bpy.context.collection.objects.unlink(light)
        collection.objects.link(light)
    
    return sun, rim_light, fill_light, interior_light1, interior_light2

lights = create_lights(house_collection)

# Add more interior lights for better illumination
def enhance_interior_lighting(collection):
    # Add more interior lights for first floor
    interior_lights = []
    
    # Multiple lights on first floor for better distribution
    light_positions_first_floor = [
        (0, 0, 2.5),       # Center
        (-4, -3, 2.5),     # Left back corner
        (4, -3, 2.5),      # Right back corner
        (-4, 3, 2.5),      # Left front corner
        (4, 3, 2.5),       # Right front corner
        (0, -3, 2.5)       # Back center (sofa area)
    ]
    
    for i, pos in enumerate(light_positions_first_floor):
        bpy.ops.object.light_add(type='POINT', location=pos)
        light = bpy.context.active_object
        light.name = f"Interior_Light_1F_{i}"
        light.data.energy = 200  # Brighter lights
        light.data.color = (1.0, 0.95, 0.8)  # Warm interior light
        light.data.shadow_soft_size = 3.0  # Softer shadows for better interior illumination
        collection.objects.link(light)
        bpy.context.collection.objects.unlink(light)
        interior_lights.append(light)
    
    # Multiple lights on second floor
    light_positions_second_floor = [
        (0, 0, 6),        # Center
        (-3, -3, 6),      # Left back corner
        (3, -3, 6),       # Right back corner
        (-3, 3, 6),       # Left front corner
        (3, 3, 6),        # Right front corner
        (0, -2, 6)        # Bed area
    ]
    
    for i, pos in enumerate(light_positions_second_floor):
        bpy.ops.object.light_add(type='POINT', location=pos)
        light = bpy.context.active_object
        light.name = f"Interior_Light_2F_{i}"
        light.data.energy = 200  # Brighter lights
        light.data.color = (1.0, 0.95, 0.8)  # Warm interior light
        light.data.shadow_soft_size = 3.0  # Softer shadows
        collection.objects.link(light)
        bpy.context.collection.objects.unlink(light)
        interior_lights.append(light)
    
    # Add area lights for even illumination
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3))
    ceiling_light1 = bpy.context.active_object
    ceiling_light1.name = "Ceiling_Light_1F"
    ceiling_light1.data.energy = 300
    ceiling_light1.data.size = 5
    ceiling_light1.data.color = (1.0, 0.95, 0.8)
    collection.objects.link(ceiling_light1)
    bpy.context.collection.objects.unlink(ceiling_light1)
    interior_lights.append(ceiling_light1)
    
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 6.5))
    ceiling_light2 = bpy.context.active_object
    ceiling_light2.name = "Ceiling_Light_2F"
    ceiling_light2.data.energy = 300
    ceiling_light2.data.size = 5
    ceiling_light2.data.color = (1.0, 0.95, 0.8)
    collection.objects.link(ceiling_light2)
    bpy.context.collection.objects.unlink(ceiling_light2)
    interior_lights.append(ceiling_light2)
    
    return interior_lights

# Enhance interior materials for better visibility
def enhance_interior_materials():
    # Improve interior floor material
    if 'Interior Floor' in bpy.data.materials:
        mat = bpy.data.materials['Interior Floor']
        if mat and mat.use_nodes:
            principled = mat.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs["Roughness"].default_value = 0.2  # More reflective floor
                principled.inputs["Specular IOR Level"].default_value = 0.5
    
    # Improve sofa material
    if 'Sofa' in bpy.data.materials:
        mat = bpy.data.materials['Sofa']
        if mat and mat.use_nodes:
            principled = mat.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs["Base Color"].default_value = (0.95, 0.95, 0.9, 1.0)  # Brighter sofa
                principled.inputs["Roughness"].default_value = 0.5
    
    # Make sure wall interiors have correct normals and are visible
    for obj in [first_floor, second_floor]:
        # Fix normals
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')

# Call the new functions
interior_lights = enhance_interior_lighting(house_collection)
enhance_interior_materials()

# Increase cycles light paths for better interior rendering
bpy.context.scene.cycles.max_bounces = 12
bpy.context.scene.cycles.diffuse_bounces = 4
bpy.context.scene.cycles.glossy_bounces = 4
bpy.context.scene.cycles.transmission_bounces = 8  # Important for glass
bpy.context.scene.cycles.volume_bounces = 2
bpy.context.scene.cycles.transparent_max_bounces = 8

# Create camera with good composition
bpy.ops.object.camera_add(location=(20, 15, 8), rotation=(math.radians(75), 0, math.radians(125)))
camera = bpy.context.active_object
camera.name = "Main_Camera"
bpy.context.scene.camera = camera

# Set camera parameters for architectural visualization
camera.data.lens = 35  # 35mm lens
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 22  # Focus on the house
camera.data.dof.aperture_fstop = 5.6  # Slight depth of field

# Create a subtle sloped terrain 
def create_terrain(collection):
    # Create a grid mesh for the terrain
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=32, y_subdivisions=32, size=40)
    terrain = bpy.context.active_object
    terrain.name = "Terrain"
    
    # Apply a slight displacement to create natural unevenness
    displace_mod = terrain.modifiers.new(name="Displace", type='DISPLACE')
    texture = bpy.data.textures.new("TerrainNoise", type='CLOUDS')
    texture.noise_scale = 5.0
    displace_mod.texture = texture
    displace_mod.strength = 0.5
    
    # Create terrain material with grass texture
    terrain_mat = create_material("Terrain", (0.2, 0.4, 0.1), 0.9)
    texture_node = terrain_mat.node_tree.nodes.new('ShaderNodeTexNoise')
    texture_node.inputs['Scale'].default_value = 20
    texture_node.inputs['Detail'].default_value = 6
    
    # Connect the noise texture to the material
    principled = terrain_mat.node_tree.nodes.get("Principled BSDF")
    color_mix = terrain_mat.node_tree.nodes.new('ShaderNodeMixRGB')
    color_mix.blend_type = 'MULTIPLY'
    color_mix.inputs[0].default_value = 0.3
    color_mix.inputs[1].default_value = (0.2, 0.4, 0.1, 1.0)
    color_mix.inputs[2].default_value = (0.15, 0.3, 0.05, 1.0)
    
    terrain_mat.node_tree.links.new(texture_node.outputs['Fac'], color_mix.inputs['Fac'])
    terrain_mat.node_tree.links.new(color_mix.outputs['Color'], principled.inputs['Base Color'])
    
    terrain.data.materials.append(terrain_mat)
    
    # Position the terrain slightly below ground level
    terrain.location.z = -0.2
    
    # Create a subtle slope upwards where the house sits
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Select vertices near the house to raise them slightly
    for vertex in terrain.data.vertices:
        world_co = terrain.matrix_world @ Vector(vertex.co)
        distance = math.sqrt(world_co.x**2 + world_co.y**2)
        if distance < 8:  # Radius around house
            vertex.select = True
            # Raise vertices based on distance (closer = higher)
            vertex.co.z += 0.6 * (1 - (distance / 8))
    
    # Remove from current collection and add to the specified collection
    bpy.context.collection.objects.unlink(terrain)
    collection.objects.link(terrain)
    
    return terrain

terrain = create_terrain(house_collection)

# Final render settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = False
bpy.context.scene.render.filepath = "//modern_house_render.png"

# Set up enhanced composition for post-processing
bpy.context.scene.use_nodes = True
comp_nodes = bpy.context.scene.node_tree.nodes
comp_links = bpy.context.scene.node_tree.links

# Clear default nodes
for node in comp_nodes:
    comp_nodes.remove(node)

# Create new nodes with enhanced setup - removing undefined nodes
render_layer = comp_nodes.new(type='CompositorNodeRLayers')
denoise = comp_nodes.new(type='CompositorNodeDenoise')
color_correction = comp_nodes.new(type='CompositorNodeColorCorrection')
bloom = comp_nodes.new(type='CompositorNodeGlare')
# Removed lens_distortion which is undefined
tone_mapping = comp_nodes.new(type='CompositorNodeExposure')
output = comp_nodes.new(type='CompositorNodeComposite')
viewer = comp_nodes.new(type='CompositorNodeViewer')

# Position nodes in a logical layout
render_layer.location = (-600, 0)
denoise.location = (-400, 0)
color_correction.location = (-200, 0)
bloom.location = (0, 0)
# Skip lens_distortion position
tone_mapping.location = (200, 0)
output.location = (400, 0)
viewer.location = (400, -150)

# Set up enhanced node properties
# Denoise settings for smoother image
denoise.use_hdr = True  # Better for Cycles HDR rendering

# Color correction settings
color_correction.master_saturation = 1.1  # Slightly more vibrant
color_correction.master_contrast = 1.05  # Slightly more contrast
color_correction.master_gamma = 0.95  # Slightly darker shadows

# Bloom/Glare settings - better for interior lights and glass
bloom.glare_type = 'FOG_GLOW'  # Good for indoor lighting
bloom.mix = 0.5  # More subtle effect
bloom.quality = 'HIGH'
bloom.threshold = 0.7  # Capture more of the bright areas
bloom.size = 8

# Removed lens distortion settings

# Tone mapping for final exposure adjustment
tone_mapping.inputs["Exposure"].default_value = 0.1  # Slightly brighter

# Connect all nodes - simpler node setup without undefined nodes
comp_links.new(render_layer.outputs["Image"], denoise.inputs["Image"])
comp_links.new(denoise.outputs["Image"], color_correction.inputs["Image"])
comp_links.new(color_correction.outputs["Image"], bloom.inputs["Image"])
# Skip lens_distortion connection
comp_links.new(bloom.outputs["Image"], tone_mapping.inputs["Image"])
comp_links.new(tone_mapping.outputs["Image"], output.inputs["Image"])
comp_links.new(tone_mapping.outputs["Image"], viewer.inputs["Image"])

# Connect passes for even better compositing
if "Depth" in render_layer.outputs:
    # Use depth for subtle depth effects via a color ramp
    depth_ramp = comp_nodes.new(type='CompositorNodeValToRGB')
    depth_ramp.location = (-400, -150)
    depth_mix = comp_nodes.new(type='CompositorNodeMixRGB')
    depth_mix.location = (-200, -150)
    depth_mix.blend_type = 'MULTIPLY'
    depth_mix.inputs[0].default_value = 0.15  # Subtle effect
    
    comp_links.new(render_layer.outputs["Depth"], depth_ramp.inputs["Fac"])
    comp_links.new(depth_ramp.outputs["Color"], depth_mix.inputs[2])
    comp_links.new(denoise.outputs["Image"], depth_mix.inputs[1])
    comp_links.new(depth_mix.outputs["Color"], color_correction.inputs["Image"])

# Füge mehr Möbel im Erdgeschoss hinzu
def add_more_interior_furniture(collection):
    # Erdgeschoss Möbel - Esstisch
    table_mat = create_material("Table", (0.4, 0.3, 0.2), 0.3, 0.1)
    dining_table = create_cube("Dining_Table", (3, 1.5, 0.1), (-2, 2, 1.5), collection, table_mat)
    
    # Stühle
    chair_mat = create_material("Chair", (0.3, 0.3, 0.3), 0.5)
    chair1 = create_cube("Chair_1", (0.6, 0.6, 1), (-2.5, 1.5, 1), collection, chair_mat)
    chair2 = create_cube("Chair_2", (0.6, 0.6, 1), (-1.5, 1.5, 1), collection, chair_mat)
    chair3 = create_cube("Chair_3", (0.6, 0.6, 1), (-2.5, 2.5, 1), collection, chair_mat)
    chair4 = create_cube("Chair_4", (0.6, 0.6, 1), (-1.5, 2.5, 1), collection, chair_mat)
    
    # Couchtisch
    coffee_table = create_cube("Coffee_Table", (1.5, 1, 0.05), (0, -1.5, 1), collection, table_mat)
    
    # Teppich
    carpet_mat = create_material("Carpet", (0.8, 0.7, 0.6), 0.9)
    carpet = create_plane("Carpet", (5, 4), (0, -2, 0.4), collection, carpet_mat)
    
    # TV-Möbel
    tv_stand = create_cube("TV_Stand", (3, 0.5, 0.8), (2, -4, 1.2), collection, table_mat)
    
    # TV
    tv_mat = create_material("TV", (0.05, 0.05, 0.05), 0.2)
    tv_screen_mat = create_material("TV_Screen", (0.1, 0.1, 0.1), 0.0)
    tv_screen_mat.use_nodes = True
    principled = tv_screen_mat.node_tree.nodes.get("Principled BSDF")
    
    # Handle different naming conventions for emission in different Blender versions
    emission_color = (0.2, 0.2, 0.3, 1.0)
    emission_strength = 2.0
    
    # Check for different possible emission input names
    if "Emission" in principled.inputs:
        principled.inputs["Emission"].default_value = emission_color
    elif "Emission Color" in principled.inputs:
        principled.inputs["Emission Color"].default_value = emission_color
    
    # Check for different possible emission strength input names
    if "Emission Strength" in principled.inputs:
        principled.inputs["Emission Strength"].default_value = emission_strength
    elif "Emission" in principled.inputs and len(principled.inputs["Emission"].links) == 0:
        # If "Emission" exists but hasn't been used for color
        principled.inputs["Emission"].default_value = emission_strength
    
    # Alternative approach: Create a separate emission shader and mix it
    if "Emission" not in principled.inputs and "Emission Strength" not in principled.inputs:
        nodes = tv_screen_mat.node_tree.nodes
        links = tv_screen_mat.node_tree.links
        
        # Create emission shader
        emission_shader = nodes.new(type='ShaderNodeEmission')
        emission_shader.inputs[0].default_value = emission_color  # Color
        if "Strength" in emission_shader.inputs:
            emission_shader.inputs["Strength"].default_value = emission_strength
        
        # Create mix shader
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        mix_shader.inputs[0].default_value = 0.8  # Mix factor
        
        # Create output
        output = nodes.get("Material Output")
        if not output:
            output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # Connect nodes
        links.new(principled.outputs[0], mix_shader.inputs[1])
        links.new(emission_shader.outputs[0], mix_shader.inputs[2])
        links.new(mix_shader.outputs[0], output.inputs[0])
    
    tv_frame = create_cube("TV_Frame", (2.5, 0.1, 1.5), (2, -4.3, 2.5), collection, tv_mat)
    tv_screen = create_cube("TV_Screen", (2.3, 0.05, 1.3), (2, -4.25, 2.5), collection, tv_screen_mat)
    
    # Regale/Bücherregal
    shelf_mat = create_material("Shelf", (0.3, 0.2, 0.1), 0.4)
    shelf = create_cube("Shelf", (1, 0.4, 2), (4, -4, 1.8), collection, shelf_mat)
    
    # Bücher auf dem Regal (vereinfacht)
    book_positions = [
        (4, -4, 1.0),
        (4, -4, 1.3),
        (4, -4, 1.6),
        (4, -4, 1.9),
        (4, -4, 2.2),
    ]
    
    book_colors = [
        (0.7, 0.2, 0.2),
        (0.2, 0.4, 0.7),
        (0.1, 0.5, 0.3),
        (0.6, 0.6, 0.2),
        (0.5, 0.3, 0.6),
    ]
    
    books = []
    for i, (pos, color) in enumerate(zip(book_positions, book_colors)):
        book_mat = create_material(f"Book_{i}", color, 0.8)
        book = create_cube(f"Book_{i}", (0.8, 0.3, 0.2), pos, collection, book_mat)
        books.append(book)
    
    # Innenwände für mehr Raumaufteilung
    wall_mat = bpy.data.materials.get("White Wall")
    
    # Trennwand zwischen Wohn- und Essbereich
    partition_wall = create_cube("Partition_Wall", (0.2, 4, 3), (-3, 0, 1.5), collection, wall_mat)
    
    # Küchenwand/Kücheninsel
    kitchen_island = create_cube("Kitchen_Island", (3, 1, 0.9), (3, 2, 0.95), collection, create_material("Kitchen", (0.8, 0.8, 0.8), 0.4))
    
    # Küchengeräte
    sink = create_cube("Sink", (1, 0.8, 0.1), (3, 2, 1.45), collection, create_material("Sink", (0.8, 0.8, 0.8), 0.2, 0.8))
    
    # Küchenarmaturen (vereinfacht)
    faucet = create_cube("Faucet", (0.1, 0.1, 0.4), (3, 1.8, 1.7), collection, create_material("Metal", (0.8, 0.8, 0.8), 0.2, 0.9))
    
    return {
        "dining_table": dining_table,
        "coffee_table": coffee_table,
        "tv": tv_frame,
        "shelf": shelf,
    }

# Lade ein HDRI für den Himmel mit Wolken - Fix Vector KeyError
def add_hdri_sky_with_clouds():
    world = bpy.context.scene.world
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create a procedural sky texture with clouds - more compatible version
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    sky_texture = nodes.new(type='ShaderNodeTexSky')
    cloud_texture = nodes.new(type='ShaderNodeTexNoise')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    mix_shader = nodes.new(type='ShaderNodeMixRGB')
    background = nodes.new(type='ShaderNodeBackground')
    output = nodes.new(type='ShaderNodeOutputWorld')
    
    # Position nodes
    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    sky_texture.location = (-400, 100)
    cloud_texture.location = (-400, -100)
    color_ramp.location = (-200, -100)
    mix_shader.location = (0, 0)
    background.location = (200, 0)
    output.location = (400, 0)
    
    # Setup texture mapping - safer property access
    if 'Scale' in mapping.inputs:
        mapping.inputs['Scale'].default_value[0] = 1.0
        mapping.inputs['Scale'].default_value[1] = 1.0
        mapping.inputs['Scale'].default_value[2] = 1.0
    
    # Setup sky texture with compatibility checks
    if hasattr(sky_texture, 'turbidity'):
        sky_texture.turbidity = 2.0  # Clearer sky
    if hasattr(sky_texture, 'ground_albedo'):
        sky_texture.ground_albedo = 0.3
    if hasattr(sky_texture, 'sun_direction'):
        sky_texture.sun_direction = (0.5, 0.0, 0.8)  # Late afternoon sun position
    if hasattr(sky_texture, 'sun_size'):
        sky_texture.sun_size = 4.0
    if hasattr(sky_texture, 'sun_intensity'):
        sky_texture.sun_intensity = 3.0
    
    # Setup cloud texture with safe property access
    if 'Scale' in cloud_texture.inputs:
        cloud_texture.inputs['Scale'].default_value = 2.0
    if 'Detail' in cloud_texture.inputs:
        cloud_texture.inputs['Detail'].default_value = 8.0
    if 'Roughness' in cloud_texture.inputs:
        cloud_texture.inputs['Roughness'].default_value = 0.7
    if 'Distortion' in cloud_texture.inputs:
        cloud_texture.inputs['Distortion'].default_value = 2.0
    
    # Setup color ramp for clouds
    color_ramp.color_ramp.elements[0].position = 0.4
    color_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.6
    color_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    
    # Setup mix shader with safe property access
    mix_shader.blend_type = 'OVERLAY'
    if 'Fac' in mix_shader.inputs:
        mix_shader.inputs['Fac'].default_value = 0.3  # Cloud density
    
    # Setup background
    if 'Strength' in background.inputs:
        background.inputs['Strength'].default_value = 1.0
    
    # Connect nodes with safer approach
    # Check available outputs/inputs before connecting
    # Function to safely connect nodes
    def safe_link(from_node, from_socket_name, to_node, to_socket_name):
        if from_socket_name in from_node.outputs and to_socket_name in to_node.inputs:
            links.new(from_node.outputs[from_socket_name], to_node.inputs[to_socket_name])
            return True
        return False
    
    # Try different socket names for each connection
    # 1. Texture coordinates to mapping
    if not safe_link(tex_coord, 'Generated', mapping, 'Vector'):
        # Alternative socket names to try
        for out_name in tex_coord.outputs.keys():
            if out_name in ['Generated', 'UV', 'Object', 'Window']:
                for in_name in mapping.inputs.keys():
                    if in_name in ['Vector', 'Location']:
                        safe_link(tex_coord, out_name, mapping, in_name)
                        break
    
    # 2. Mapping to sky texture and noise texture
    for out_name in mapping.outputs.keys():
        for node in [sky_texture, cloud_texture]:
            for in_name in node.inputs.keys():
                if in_name in ['Vector', 'Location', 'Coordinates']:
                    safe_link(mapping, out_name, node, in_name)
                    break
    
    # 3. Cloud texture to color ramp
    if not safe_link(cloud_texture, 'Fac', color_ramp, 'Fac'):
        for out_name in cloud_texture.outputs.keys():
            if out_name in ['Fac', 'Color', 'Factor']:
                for in_name in color_ramp.inputs.keys():
                    if in_name in ['Fac', 'Factor']:
                        safe_link(cloud_texture, out_name, color_ramp, in_name)
                        break
    
    # 4. Connect sky texture and color ramp to mix shader
    if not safe_link(sky_texture, 'Color', mix_shader, '1'):
        # Try alternative socket names
        for out_name in sky_texture.outputs.keys():
            for in_idx in range(1, 3):  # Try inputs 1 and 2
                if str(in_idx) in mix_shader.inputs:
                    safe_link(sky_texture, out_name, mix_shader, str(in_idx))
                    break
    
    if not safe_link(color_ramp, 'Color', mix_shader, '2'):
        # Try alternative socket names  
        for out_name in color_ramp.outputs.keys():
            for in_idx in range(1, 3):  # Try both standard inputs
                if str(in_idx) in mix_shader.inputs and not mix_shader.inputs[str(in_idx)].links:
                    safe_link(color_ramp, out_name, mix_shader, str(in_idx))
                    break
    
    # 5. Connect mix shader to background
    if not safe_link(mix_shader, 'Color', background, 'Color'):
        # Try alternative socket names
        for out_name in mix_shader.outputs.keys():
            for in_name in background.inputs.keys():
                if in_name != 'Strength':  # Skip strength input
                    safe_link(mix_shader, out_name, background, in_name)
                    break
    
    # 6. Connect background to output
    if not safe_link(background, 'Background', output, 'Surface'):
        # Try alternative socket names
        for out_name in background.outputs.keys():
            for in_name in output.inputs.keys():
                safe_link(background, out_name, in_name)
                break
    
    # Fallback: If procedural approach fails, create a simple sky
    if len(output.inputs[0].links) == 0:
        print("Creating simple sky background as fallback")
        # Remove all nodes and create a simple setup
        for node in nodes:
            nodes.remove(node)
        
        background = nodes.new(type='ShaderNodeBackground')
        output = nodes.new(type='ShaderNodeOutputWorld')
        
        # Set sky color
        background.inputs[0].default_value = (0.5, 0.7, 1.0, 1.0)
        
        # Link background to output
        links.new(background.outputs[0], output.inputs[0])

# Führe die neuen Funktionen aus
additional_furniture = add_more_interior_furniture(house_collection)
add_hdri_sky_with_clouds()

print("Modern house scene created successfully!")