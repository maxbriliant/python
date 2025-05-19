import bpy
import math
import bmesh
from mathutils import Vector, Matrix
import random

# Script to create a detailed pirate ship based on technical specifications
# For Blender 4.4.3
# This script generates a complete model with hull, masts, rigging, and decorative elements

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Set units to metric and scale to meters
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Create collections for organization
def create_collections():
    main_collection = bpy.data.collections.new("PirateShip")
    bpy.context.scene.collection.children.link(main_collection)
    
    collections = {
        "hull": bpy.data.collections.new("Hull"),
        "masts": bpy.data.collections.new("Masts"),
        "sails": bpy.data.collections.new("Sails"),
        "rigging": bpy.data.collections.new("Rigging"),
        "details": bpy.data.collections.new("Details"),
        "deck": bpy.data.collections.new("Deck"),
        "interior": bpy.data.collections.new("Interior"),  # Neue Sammlung für Innenräume
        "underwater": bpy.data.collections.new("Underwater")  # Neue Sammlung für Unterwasserkomponenten
    }
    
    for name, collection in collections.items():
        main_collection.children.link(collection)
    
    return collections

collections = create_collections()

# Helper functions
def add_to_collection(obj, collection_name):
    """Add object to the specified collection"""
    collections[collection_name].objects.link(obj)
    bpy.context.collection.objects.unlink(obj)

def create_material(name, color, roughness=0.5, metallic=0.0, specular=0.5):
    """Create and return a new material"""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        # Handle different Blender versions (4.x uses 'Specular IOR Level')
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
    
    return mat

def apply_material(obj, material):
    """Apply material to object"""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

def create_curve(name, points, bevel_depth=0.0, fill_mode='FULL'):
    """Create a curve object from points"""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = bevel_depth
    curve_data.fill_mode = fill_mode
    
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(len(points) - 1)
    
    for i, point in enumerate(points):
        spline.bezier_points[i].co = point
        spline.bezier_points[i].handle_left_type = 'AUTO'
        spline.bezier_points[i].handle_right_type = 'AUTO'
    
    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)
    return curve_obj

# Materials
materials = {
    "dark_wood": create_material("DarkWood", (0.05, 0.025, 0.01, 1.0), roughness=0.7),
    "light_wood": create_material("LightWood", (0.2, 0.1, 0.05, 1.0), roughness=0.6),
    "railing_wood": create_material("RailingWood", (0.12, 0.07, 0.03, 1.0), roughness=0.5),
    "sail_cloth": create_material("SailCloth", (0.9, 0.88, 0.8, 1.0), roughness=0.8),
    "ropes": create_material("Ropes", (0.1, 0.1, 0.09, 1.0), roughness=0.9),
    "brass": create_material("Brass", (0.8, 0.6, 0.2, 1.0), roughness=0.3, metallic=0.8),
    "iron": create_material("Iron", (0.3, 0.3, 0.3, 1.0), roughness=0.6, metallic=0.7),
    "red_cloth": create_material("RedCloth", (0.8, 0.1, 0.1, 1.0), roughness=0.7),
    "orange": create_material("Orange", (0.9, 0.4, 0.0, 1.0), roughness=0.6),
    "water": create_material("Water", (0.0, 0.2, 0.4, 0.9), roughness=0.1, specular=0.9),
    "wet_wood": create_material("WetWood", (0.07, 0.04, 0.02, 1.0), roughness=0.4),  # Dunkleres Holz für nasse Bereiche
    "rusty_metal": create_material("RustyMetal", (0.5, 0.2, 0.1, 1.0), roughness=0.8, metallic=0.4), # Für alte Metallteile
    "glass": create_material("Glass", (0.8, 0.9, 1.0, 0.3), roughness=0.1, specular=1.0), # Für Fenster
    "leather": create_material("Leather", (0.3, 0.2, 0.1, 1.0), roughness=0.6), # Für Möbel und Taschen
    "canvas": create_material("Canvas", (0.8, 0.75, 0.6, 1.0), roughness=0.7) # Für Zusätzliche Textilien
}

# Create the hull of the ship
def create_hull():
    """Create the hull of the ship"""
    # Ship dimensions from the description
    length = 48.0  # meters
    width = 11.0   # meters
    height = 8.0   # meters
    
    # Create the basic hull shape
    bpy.ops.mesh.primitive_cube_add(size=1)
    hull = bpy.context.active_object
    hull.name = "Ship_Hull"
    hull.scale = (length/2, width/2, height/2)
    hull.location = (0, 0, height/2)
    
    # Convert to mesh for editing
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(hull.data)
    
    # Taper the bow
    for v in bm.verts:
        if v.co.x > 0:  # Front part of the ship
            # Taper width
            v.co.y *= 0.7 * (1 - v.co.x / (length/2))
            
            # Raise bow
            v.co.z += 0.8 * (v.co.x / (length/2))
    
    # Taper the stern
    for v in bm.verts:
        if v.co.x < 0:  # Back part of the ship
            # Taper width less severely than bow
            v.co.y *= 0.9 * (1 + v.co.x / (length/2))
            
            # Raise stern
            if v.co.z > 0:
                v.co.z += 0.4 * (-v.co.x / (length/2))
    
    # Create underwater hull shape - more rounded for hydrodynamics
    for v in bm.verts:
        if v.co.z < 0:
            # Round the bottom
            z_factor = -v.co.z / (height/2)
            x_factor = abs(v.co.x) / (length/2)
            
            # Make the hull more bulbous underwater
            v.co.y *= 0.9 - (0.1 * z_factor)
            
            # Create keel curve
            if abs(v.co.y) < 0.5:
                v.co.z -= 0.5 * (1 - x_factor)
    
    # Update mesh
    bmesh.update_edit_mesh(hull.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add hull details (subdivide and smooth)
    bpy.ops.object.modifier_add(type='SUBSURF')
    hull.modifiers["Subdivision"].levels = 3
    
    # Optional: Add a curve modifier to give the hull a slight curve
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    hull.modifiers["SimpleDeform"].deform_method = 'BEND'
    hull.modifiers["SimpleDeform"].angle = math.radians(5)
    hull.modifiers["SimpleDeform"].deform_axis = 'Z'
    
    apply_material(hull, materials["dark_wood"])
    add_to_collection(hull, "hull")
    
    # Add the keel
    bpy.ops.mesh.primitive_cube_add(size=1)
    keel = bpy.context.active_object
    keel.name = "Keel"
    keel.scale = (length * 0.5, 0.2, height * 0.1)
    keel.location = (0, 0, 0)
    apply_material(keel, materials["dark_wood"])
    add_to_collection(keel, "hull")
    
    # Add gun ports
    gun_ports = []
    port_width = 0.8
    port_height = 0.8
    port_depth = 0.2
    num_ports = 10  # on each side
    
    for i in range(num_ports):
        x_pos = -length * 0.4 + (i * length * 0.8 / (num_ports - 1))
        
        # Port side
        bpy.ops.mesh.primitive_cube_add(size=1)
        port = bpy.context.active_object
        port.name = f"GunPort_Port_{i}"
        port.scale = (port_width/2, port_depth, port_height/2)
        port.location = (x_pos, width/2, height * 0.3)
        apply_material(port, materials["dark_wood"])
        gun_ports.append(port)
        
        # Starboard side
        bpy.ops.mesh.primitive_cube_add(size=1)
        starboard = bpy.context.active_object
        starboard.name = f"GunPort_Starboard_{i}"
        starboard.scale = (port_width/2, port_depth, port_height/2)
        starboard.location = (x_pos, -width/2, height * 0.3)
        apply_material(starboard, materials["dark_wood"])
        gun_ports.append(starboard)
    
    for port in gun_ports:
        add_to_collection(port, "hull")
    
    # Create bowsprit
    bowsprit_length = 10.0
    bowsprit_points = [
        Vector((length/2, 0, height * 0.6)),
        Vector((length/2 + bowsprit_length * 0.3, 0, height * 0.7)),
        Vector((length/2 + bowsprit_length, 0, height * 0.8))
    ]
    
    bowsprit = create_curve("Bowsprit", bowsprit_points, bevel_depth=0.15)
    apply_material(bowsprit, materials["dark_wood"])
    add_to_collection(bowsprit, "hull")
    
    # Create the figurehead (detaillierter)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8)
    figurehead_base = bpy.context.active_object
    figurehead_base.name = "Figurehead_Base"
    figurehead_base.location = (length/2 + bowsprit_length, 0, height * 0.8)
    apply_material(figurehead_base, materials["red_cloth"])
    
    # Füge eine einfache Figur hinzu (z.B. eine Frauenfigur oder ein Tier)
    bpy.ops.mesh.primitive_cone_add(radius1=0.5, radius2=0, depth=1.5)
    figurehead_body = bpy.context.active_object
    figurehead_body.name = "Figurehead_Body"
    figurehead_body.location = (length/2 + bowsprit_length + 0.5, 0, height * 0.8 - 0.5)
    figurehead_body.rotation_euler = (math.pi/2, 0, 0)
    apply_material(figurehead_body, materials["red_cloth"])
    
    # Gruppiere die Gallionsfigur
    figurehead_parts = [figurehead_base, figurehead_body]
    for part in figurehead_parts:
        add_to_collection(part, "details")
    
    # Schaffung des unterwasser Rumpfes für mehr Realismus
    # Verstärkung der Wasserlinie
    bpy.ops.mesh.primitive_cylinder_add(vertices=32)
    waterline = bpy.context.active_object
    waterline.name = "Waterline"
    waterline.scale = (length/2 * 1.01, width/2 * 1.01, 0.05)
    waterline.location = (0, 0, 0)
    apply_material(waterline, materials["wet_wood"])
    add_to_collection(waterline, "hull")
    
    # Hinzufügen von Kupferplatten unter der Wasserlinie (typisch für Piratenschiffe)
    hull_underwater_parts = []
    plate_rows = 5
    plate_cols = 20
    plate_width = length / plate_cols
    plate_height = 2.0 / plate_rows
    
    for row in range(plate_rows):
        for col in range(plate_cols):
            bpy.ops.mesh.primitive_cube_add(size=1)
            plate = bpy.context.active_object
            plate.name = f"CopperPlate_R{row}_C{col}"
            
            # Position berechnen
            x_pos = -length/2 + col * plate_width + plate_width/2
            z_pos = -height/4 + row * plate_height * 0.8
            y_factor = 1.0 - 0.1 * (row / plate_rows)  # Schmaler werden nach unten
            
            # Skalieren und positionieren
            plate.scale = (plate_width/2 * 0.9, y_factor * width/2, plate_height/2 * 0.9)
            
            # Die Platte an die Rumpfkontur anpassen
            bow_factor = max(0, min(1, (col / plate_cols - 0.5) * 2))  # 0 am Mittelpunkt, 1 am Bug
            stern_factor = max(0, min(1, (0.5 - col / plate_cols) * 2))  # 0 am Mittelpunkt, 1 am Heck
            
            # Bug verengen
            if bow_factor > 0:
                plate.scale.y *= 1 - bow_factor * 0.3
            
            # Heck formen
            if stern_factor > 0:
                plate.scale.y *= 1 - stern_factor * 0.1
            
            plate.location = (x_pos, 0, z_pos)
            
            # Materialien alternieren für realistischeren Look
            rust_factor = random.uniform(0, 0.2)
            plate_material = create_material(
                f"CopperPlate_R{row}_C{col}", 
                (0.65 - rust_factor, 0.4 - rust_factor, 0.1, 1.0), 
                roughness=0.3 + random.uniform(0, 0.4), 
                metallic=0.6
            )
            apply_material(plate, plate_material)
            
            # Für Port und Steuerbord duplizieren
            for side_factor in [-1, 1]:
                if side_factor == -1:
                    # Original-Platte benutzen für Steuerbord
                    plate.location.y = side_factor * (width/2 * 0.98) * y_factor
                else:
                    # Kopie für Backbord erstellen
                    new_plate = plate.copy()
                    new_plate.data = plate.data.copy()
                    new_plate.name = f"CopperPlate_R{row}_C{col}_Port"
                    new_plate.location.y = side_factor * (width/2 * 0.98) * y_factor
                    bpy.context.collection.objects.link(new_plate)
                    hull_underwater_parts.append(new_plate)
            
            hull_underwater_parts.append(plate)
    
    # Hinzufügen von Unterwasserverstärkungen (Spanten)
    num_ribs = 15
    for i in range(num_ribs):
        x_pos = -length/2 + i * length/(num_ribs-1)
        
        # Der Faktor gestaltet die Spanten unterschiedlich je nach Position
        bow_factor = max(0, min(1, (i / (num_ribs-1) - 0.5) * 2))
        stern_factor = max(0, min(1, (0.5 - i / (num_ribs-1)) * 2))
        
        bpy.ops.mesh.primitive_cube_add(size=1)
        rib = bpy.context.active_object
        rib.name = f"Hull_Rib_{i}"
        
        # Anpassung der Spante an Rumpfform
        rib.scale = (0.2, width/2 * (0.9 - bow_factor * 0.3 - stern_factor * 0.1), height/3)
        rib.location = (x_pos, 0, -height/6)
        
        # Material mit leichten Variationen
        rib_wood_color = (0.1 - random.uniform(0, 0.03), 0.05 - random.uniform(0, 0.02), 0.02, 1.0)
        rib_material = create_material(f"RibWood_{i}", rib_wood_color, roughness=0.6 + random.uniform(0, 0.1))
        apply_material(rib, rib_material)
        
        hull_underwater_parts.append(rib)
    
    for part in hull_underwater_parts:
        add_to_collection(part, "underwater")
    
    return hull

def create_masts(hull):
    """Create the masts with proper rotation (corrected 90 degrees)"""
    # Get hull dimensions
    hull_length = hull.scale.x * 2
    hull_width = hull.scale.y * 2
    hull_height = hull.scale.z * 2
    
    # Define mast positions and heights
    # Three masts as described: foremast, mainmast, mizzenmast
    mast_data = [
        {  # Foremast (front)
            "name": "Foremast",
            "position": (hull_length * 0.25, 0, hull_height * 0.5),
            "height": 18.0,
            "thickness": 0.5
        },
        {  # Mainmast (center) - tallest
            "name": "Mainmast",
            "position": (0, 0, hull_height * 0.5),
            "height": 22.0,
            "thickness": 0.6
        },
        {  # Mizzenmast (rear)
            "name": "Mizzenmast",
            "position": (-hull_length * 0.2, 0, hull_height * 0.7),  # On the quarterdeck
            "height": 17.0,
            "thickness": 0.45
        }
    ]
    
    masts = []
    for data in mast_data:
        # Create the main mast pole - CORRECTLY ROTATED (90 degrees fixed)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=data["thickness"],
            depth=data["height"],
            end_fill_type='NGON',
            location=(data["position"][0], data["position"][1], data["position"][2] + data["height"]/2)
        )
        
        mast = bpy.context.active_object
        mast.name = data["name"]
        
        # The mast is correctly aligned with Z-axis pointing up
        # No need for 90-degree rotation as cylinders are created with correct orientation
        
        apply_material(mast, materials["railing_wood"])
        add_to_collection(mast, "masts")
        masts.append(mast)
        
        # Create a small platform (crow's nest) near the top of each mast
        platform_height = data["height"] * 0.75
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=data["thickness"] * 3,
            depth=0.1,
            location=(data["position"][0], data["position"][1], data["position"][2] + platform_height)
        )
        platform = bpy.context.active_object
        platform.name = f"Platform_{data['name']}"
        apply_material(platform, materials["light_wood"])
        add_to_collection(platform, "masts")
        
        # Add railing to platform
        bpy.ops.mesh.primitive_torus_add(
            major_radius=data["thickness"] * 3,
            minor_radius=data["thickness"] * 0.2,
            location=(data["position"][0], data["position"][1], data["position"][2] + platform_height + 0.4)
        )
        railing = bpy.context.active_object
        railing.name = f"Railing_{data['name']}"
        apply_material(railing, materials["railing_wood"])
        add_to_collection(railing, "masts")
        
        # Add horizontal yards (spars) to each mast
        num_yards = 4  # Number of horizontal spars
        yard_objects = []
        
        for i in range(num_yards):
            # Height factor determines the position on the mast
            height_factor = 0.4 + (i * 0.15)
            yard_height = data["position"][2] + data["height"] * height_factor
            yard_length = hull_width * (1.0 - (i * 0.15))  # Yards get shorter toward the top
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=data["thickness"] * 0.6,
                depth=yard_length,
                location=(data["position"][0], data["position"][1], yard_height)
            )
            
            # Rotate yards 90 degrees around Z to be perpendicular to the mast
            # This is the correct way to align yards with the ship's width
            yard = bpy.context.active_object
            yard.rotation_euler = (0, math.pi/2, 0)  # Rotate around Y-axis (90 degrees)
            
            yard.name = f"{data['name']}_Yard_{i}"
            apply_material(yard, materials["railing_wood"])
            add_to_collection(yard, "masts")
            yard_objects.append(yard)
        
        # Add a small flag to the top of each mast
        bpy.ops.mesh.primitive_cube_add(size=1)
        flag = bpy.context.active_object
        flag.name = f"{data['name']}_Flag"
        flag.scale = (0.05, data["thickness"] * 4, data["thickness"] * 3)
        flag.location = (data["position"][0], data["position"][1], data["position"][2] + data["height"] - 0.5)
        
        # Add a simple wind effect to the flag
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        flag.modifiers["SimpleDeform"].deform_method = 'BEND'
        flag.modifiers["SimpleDeform"].angle = math.radians(30)
        flag.modifiers["SimpleDeform"].deform_axis = 'Y'
        
        apply_material(flag, materials["red_cloth"])
        add_to_collection(flag, "details")
    
    return masts

def create_sails(masts):
    """Create detailed furled sails for each mast"""
    sails = []
    
    # For each mast, create furled sails on each yard
    for mast_idx, mast in enumerate(masts):
        mast_position = mast.location
        mast_height = mast.dimensions.z
        mast_thickness = mast.dimensions.x / 2  # Radius of mast
        
        # Get all yards (horizontal spars) associated with this mast
        yards = []
        for obj in collections["masts"].objects:
            if obj.name.startswith(mast.name) and "_Yard_" in obj.name:
                yards.append(obj)
        
        # Create furled sails for each yard
        for yard_idx, yard in enumerate(yards):
            yard_position = yard.location
            yard_length = yard.dimensions.z  # Because the yard was rotated
            
            # Create a furled sail as a cylinder with deformation
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=24,
                radius=0.25,
                depth=yard_length * 0.9,  # Slightly shorter than the yard
                location=(yard_position.x, yard_position.y, yard_position.z - 0.4)  # Position slightly below the yard
            )
            
            # Rotate the sail cylinder to align with the yard
            sail = bpy.context.active_object
            sail.rotation_euler = (0, math.pi/2, 0)  # Same rotation as yards
            
            sail.name = f"Furled_Sail_{mast.name}_{yard_idx}"
            
            # Add a noise modifier to create folds in the furled sail
            bpy.ops.object.modifier_add(type='DISPLACE')
            mod = sail.modifiers["Displace"]
            
            # Create a new texture for the displacement
            tex = bpy.data.textures.new(f"Sail_Texture_{mast.name}_{yard_idx}", 'CLOUDS')
            tex.noise_scale = 0.2
            tex.noise_depth = 1
            mod.texture = tex
            mod.strength = 0.05
            mod.direction = 'Z'
            
            # Add a subdivision surface modifier for smoother folds
            bpy.ops.object.modifier_add(type='SUBSURF')
            sail.modifiers["Subdivision"].levels = 2
            
            # Create custom sail color with slight variations
            sail_color = (
                0.9 - random.uniform(0, 0.1),  # Slightly off-white
                0.88 - random.uniform(0, 0.1),
                0.8 - random.uniform(0, 0.1),
                1.0
            )
            sail_material = create_material(
                f"Sail_{mast.name}_{yard_idx}",
                sail_color,
                roughness=0.8 + random.uniform(0, 0.1)
            )
            apply_material(sail, sail_material)
            
            # Add ropes connecting sail to yard
            num_ropes = int(yard_length / 0.8)
            for i in range(num_ropes):
                # Position along the yard
                pos_factor = (i / (num_ropes - 1) - 0.5) if num_ropes > 1 else 0
                rope_pos_y = yard_position.y + pos_factor * yard_length * 0.9
                
                # Create a short rope segment
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.03,
                    depth=0.5,
                    location=(yard_position.x, rope_pos_y, yard_position.z - 0.2)
                )
                rope = bpy.context.active_object
                rope.name = f"Sail_Rope_{mast.name}_{yard_idx}_{i}"
                apply_material(rope, materials["ropes"])
                add_to_collection(rope, "rigging")
            
            add_to_collection(sail, "sails")
            sails.append(sail)
    
    return sails

def create_rigging(hull, masts):
    """Create detailed rigging system for the ship"""
    rigging_objects = []
    
    # Get hull dimensions
    hull_length = hull.scale.x * 2
    hull_width = hull.scale.y * 2
    hull_height = hull.scale.z * 2
    
    # Mast positions and heights for reference
    mast_positions = [mast.location for mast in masts]
    mast_heights = [mast.dimensions.z for mast in masts]
    
    # Create standing rigging - main support lines
    for i, mast in enumerate(masts):
        mast_position = mast_positions[i]
        mast_height = mast_heights[i]
        
        # Create fore and aft stays (lines from mast top to deck)
        # These provide fore and aft support
        stays_points = [
            # Fore stay - goes forward from mast top to deck
            [(mast_position.x, mast_position.y, mast_position.z + mast_height/2),
             (min(hull_length/2, mast_position.x + hull_length/4), mast_position.y, hull_height * 0.6)],
            
            # Aft stay - goes backward from mast top to deck
            [(mast_position.x, mast_position.y, mast_position.z + mast_height/2),
             (max(-hull_length/2, mast_position.x - hull_length/4), mast_position.y, hull_height * 0.6)]
        ]
        
        for j, points in enumerate(stays_points):
            stay = create_curve(f"Stay_{mast.name}_{j}", points, bevel_depth=0.05)
            apply_material(stay, materials["ropes"])
            add_to_collection(stay, "rigging")
            rigging_objects.append(stay)
        
        # Create shrouds - lines from mast top to sides of hull
        # These provide lateral support
        num_shrouds = 6  # 3 per side
        for j in range(num_shrouds):
            side = 1 if j < num_shrouds/2 else -1  # Alternate between port and starboard
            offset = (j % (num_shrouds//2)) * 0.7 - 0.7  # Spaced out along the deck
            
            points = [
                (mast_position.x, mast_position.y, mast_position.z + mast_height/2),
                (mast_position.x + offset, side * hull_width/2, hull_height * 0.55)
            ]
            
            shroud = create_curve(f"Shroud_{mast.name}_{j}", points, bevel_depth=0.04)
            apply_material(shroud, materials["ropes"])
            add_to_collection(shroud, "rigging")
            rigging_objects.append(shroud)
    
    # Create ratlines - horizontal ropes between shrouds forming ladders
    for mast_idx, mast in enumerate(masts):
        mast_position = mast_positions[mast_idx]
        
        # Create ratlines for port and starboard separately
        for side in [-1, 1]:
            # Calculate shroud positions
            shroud_base_positions = []
            for j in range(3):  # 3 shrouds per side
                offset = j * 0.7 - 0.7
                shroud_base_positions.append((mast_position.x + offset, side * hull_width/2, hull_height * 0.55))
            
            # Create horizontal ratlines connecting shrouds
            num_ratlines = 8  # 8 horizontal rungs per side
            for j in range(num_ratlines):
                height_factor = 0.2 + j * (0.8 / (num_ratlines - 1))
                height = hull_height * 0.55 + height_factor * (mast_heights[mast_idx] / 2 - hull_height * 0.05)
                
                # Create a curve using all shroud positions at this height
                points = []
                for shroud_pos in shroud_base_positions:
                    # Calculate position along the shroud at this height
                    direction = Vector((mast_position.x, mast_position.y, mast_position.z + mast_heights[mast_idx]/2)) - Vector(shroud_pos)
                    direction.normalize()
                    
                    # Calculate how far up the shroud to place the ratline
                    shroud_length = Vector((mast_position.x, mast_position.y, mast_position.z + mast_heights[mast_idx]/2)).distance_to(Vector(shroud_pos))
                    t = (height - shroud_pos[2]) / (direction.z * shroud_length) if direction.z != 0 else 0
                    
                    # Position on the shroud
                    pos = Vector(shroud_pos) + direction * t * shroud_length
                    points.append(tuple(pos))
                
                # Create the ratline
                if len(points) > 1:
                    ratline = create_curve(f"Ratline_{mast.name}_{side}_{j}", points, bevel_depth=0.015)
                    apply_material(ratline, materials["ropes"])
                    add_to_collection(ratline, "rigging")
                    rigging_objects.append(ratline)
    
    # Create running rigging - ropes for sail control
    for i, mast in enumerate(masts):
        mast_position = mast_positions[i]
        
        # Get all yards for this mast
        yards = []
        for obj in collections["masts"].objects:
            if obj.name.startswith(mast.name) and "_Yard_" in obj.name:
                yards.append(obj)
        
        # For each yard, create braces (ropes from yard ends to the deck)
        for yard_idx, yard in enumerate(yards):
            yard_position = yard.location
            yard_length = yard.dimensions.z  # Due to rotation
            
            # Create braces from each end of the yard to the deck
            for side in [-1, 1]:
                # Yard end position
                yard_end = (
                    yard_position.x,
                    yard_position.y + side * yard_length/2,
                    yard_position.z
                )
                
                # Deck attachment point - diagonal backwards
                deck_point = (
                    yard_position.x - hull_length * 0.15,
                    yard_position.y + side * hull_width * 0.4,
                    hull_height * 0.5
                )
                
                points = [yard_end, deck_point]
                brace = create_curve(f"Brace_{mast.name}_{yard_idx}_{side}", points, bevel_depth=0.025)
                apply_material(brace, materials["ropes"])
                add_to_collection(brace, "rigging")
                rigging_objects.append(brace)
    
    # Add anchors (on both sides of the bow)
    for side in [-1, 1]:
        # Create the main anchor shaft
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.1,
            depth=2.0,
            location=(hull_length * 0.4, side * hull_width * 0.4, hull_height * 0.3)
        )
        shaft = bpy.context.active_object
        shaft.name = f"Anchor_Shaft_{side}"
        shaft.rotation_euler = (math.pi/2, 0, 0)
        apply_material(shaft, materials["iron"])
        
        # Create the anchor stock (cross piece at top)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.06,
            depth=1.2,
            location=(hull_length * 0.4, side * hull_width * 0.4, hull_height * 0.3 + 0.8)
        )
        stock = bpy.context.active_object
        stock.name = f"Anchor_Stock_{side}"
        stock.rotation_euler = (0, 0, math.pi/2)
        apply_material(stock, materials["iron"])
        
        # Create the anchor arms
        bpy.ops.mesh.primitive_cube_add(size=1)
        arms = bpy.context.active_object
        arms.name = f"Anchor_Arms_{side}"
        arms.scale = (0.1, 0.5, 0.7)
        arms.location = (hull_length * 0.4, side * hull_width * 0.4, hull_height * 0.3 - 1.0)
        apply_material(arms, materials["iron"])
        
        # Create anchor chain
        points = [
            (hull_length * 0.4, side * hull_width * 0.4, hull_height * 0.3 + 1.0),
            (hull_length * 0.45, side * hull_width * 0.45, hull_height * 0.4),
            (hull_length * 0.47, side * hull_width * 0.46, hull_height * 0.5 + 0.3),
        ]
        
        chain = create_curve(f"Anchor_Chain_{side}", points, bevel_depth=0.04)
        apply_material(chain, materials["iron"])
        
        # Add all anchor parts to rigging collection
        for obj in [shaft, stock, arms, chain]:
            add_to_collection(obj, "rigging")
            rigging_objects.append(obj)
    
    return rigging_objects

def create_ship_details(hull):
    """Create additional details for the ship"""
    # Get hull dimensions
    hull_length = hull.scale.x * 2
    hull_width = hull.scale.y * 2
    hull_height = hull.scale.z * 2
    
    details = []
    
    # Create additional decorative figurehead details
    bpy.ops.mesh.primitive_cube_add(size=1)
    figurehead_decoration = bpy.context.active_object
    figurehead_decoration.name = "Figurehead_Decoration"
    figurehead_decoration.scale = (1.5, 0.8, 0.3)
    figurehead_decoration.location = (hull_length/2 + 9, 0, hull_height * 0.8)
    
    # Add more detail with a Subdivision Surface modifier
    bpy.ops.object.modifier_add(type='SUBSURF')
    figurehead_decoration.modifiers["Subdivision"].levels = 2
    
    # Apply a curved shape with a Simple Deform modifier
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    figurehead_decoration.modifiers["SimpleDeform"].deform_method = 'BEND'
    figurehead_decoration.modifiers["SimpleDeform"].angle = math.radians(45)
    figurehead_decoration.modifiers["SimpleDeform"].deform_axis = 'Y'
    
    # Red decoration
    apply_material(figurehead_decoration, materials["red_cloth"])
    add_to_collection(figurehead_decoration, "details")
    details.append(figurehead_decoration)
    
    # Create ship's name plate on the stern
    bpy.ops.mesh.primitive_cube_add(size=1)
    name_plate = bpy.context.active_object
    name_plate.name = "Ship_Name_Plate"
    name_plate.scale = (0.2, hull_width * 0.4, 0.8)
    name_plate.location = (-hull_length/2 + 0.1, 0, hull_height * 0.6)
    
    name_plate_material = create_material("NamePlate", (0.8, 0.7, 0.2, 1.0), roughness=0.3, metallic=0.8)
    apply_material(name_plate, name_plate_material)
    add_to_collection(name_plate, "details")
    details.append(name_plate)
    
    # Create cannon ball stacks (pyramids)
    num_stacks = 3
    for i in range(num_stacks):
        x_pos = -hull_length * 0.1 + i * hull_length * 0.2
        
        # Create pyramid of cannon balls (4 at base, then 1 on top)
        ball_positions = [
            (x_pos - 0.3, hull_width * 0.2, hull_height * 0.5 + 0.3),
            (x_pos + 0.3, hull_width * 0.2, hull_height * 0.5 + 0.3),
            (x_pos - 0.3, hull_width * 0.2 + 0.6, hull_height * 0.5 + 0.3),
            (x_pos + 0.3, hull_width * 0.2 + 0.6, hull_height * 0.5 + 0.3),
            (x_pos, hull_width * 0.2 + 0.3, hull_height * 0.5 + 0.8)
        ]
        
        for j, pos in enumerate(ball_positions):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=pos)
            ball = bpy.context.active_object
            ball.name = f"CannonBall_{i}_{j}"
            apply_material(ball, materials["iron"])
            add_to_collection(ball, "details")
            details.append(ball)
    
    # Create ropes coiled on deck
    num_coils = 4
    for i in range(num_coils):
        x_pos = -hull_length * 0.3 + i * hull_length * 0.2
        y_pos = (1 if i % 2 == 0 else -1) * hull_width * 0.3
        
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.5, 
            minor_radius=0.1,
            location=(x_pos, y_pos, hull_height * 0.5 + 0.1)
        )
        rope_coil = bpy.context.active_object
        rope_coil.name = f"Rope_Coil_{i}"
        apply_material(rope_coil, materials["ropes"])
        add_to_collection(rope_coil, "details")
        details.append(rope_coil)
    
    # Add detailed grating on deck
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=10,
        y_subdivisions=10,
        size=2.0, 
        location=(hull_length * 0.1, 0, hull_height * 0.5 + 0.05)
    )
    grating = bpy.context.active_object
    grating.name = "Deck_Grating"
    apply_material(grating, materials["light_wood"])
    add_to_collection(grating, "deck")
    details.append(grating)
    
    # Add lanterns at strategic locations
    lantern_positions = [
        (-hull_length * 0.25, 0, hull_height * 1.2),  # Captain's cabin
        (hull_length * 0.25, hull_width * 0.2, hull_height * 0.6 + 0.5),  # Forecastle
        (0, 0, hull_height * 0.5 + 0.5),  # Main deck
        (-hull_length/2 + 1, 0, hull_height * 0.6)  # Stern
    ]
    
    for i, pos in enumerate(lantern_positions):
        # Create lantern body
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.15,
            depth=0.3,
            location=pos
        )
        lantern = bpy.context.active_object
        lantern.name = f"Lantern_{i}"
        apply_material(lantern, materials["brass"])
        
        # Create lantern glass
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.12,
            depth=0.25,
            location=pos
        )
        glass = bpy.context.active_object
        glass.name = f"Lantern_Glass_{i}"
        
        # Create a glowing material for the lantern
        glow_mat = create_material(
            f"Lantern_Glow_{i}", 
            (1.0, 0.9, 0.5, 1.0), 
            roughness=0.3
        )
        
        # Add emission to the glass material
        nodes = glow_mat.node_tree.nodes
        links = glow_mat.node_tree.links
        
        # Create emission node
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 0.9, 0.5, 1.0)
        emission.inputs['Strength'].default_value = 5.0
        emission.location = (-200, 0)
        
        # Connect emission to output
        output = nodes.get('Material Output')
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        apply_material(glass, glow_mat)
        
        # Add lantern top
        bpy.ops.mesh.primitive_cone_add(
            vertices=8,
            radius1=0.17,
            radius2=0.05,
            depth=0.2,
            location=(pos[0], pos[1], pos[2] + 0.25)
        )
        top = bpy.context.active_object
        top.name = f"Lantern_Top_{i}"
        apply_material(top, materials["brass"])
        
        # Add to details collection
        for obj in [lantern, glass, top]:
            add_to_collection(obj, "details")
            details.append(obj)
            
    # Create additional crew quarters and furnishings
    # Captain's quarters
    bpy.ops.mesh.primitive_cube_add(size=1)
    desk = bpy.context.active_object
    desk.name = "Captain_Desk"
    desk.scale = (0.8, 1.5, 0.4)
    desk.location = (-hull_length * 0.25, 0, hull_height * 0.9 - 0.4)
    apply_material(desk, materials["dark_wood"])
    add_to_collection(desk, "interior")
    details.append(desk)
    
    # Add a chair
    bpy.ops.mesh.primitive_cube_add(size=1)
    chair = bpy.context.active_object
    chair.name = "Captain_Chair"
    chair.scale = (0.4, 0.4, 0.6)
    chair.location = (-hull_length * 0.25 - 0.5, 0, hull_height * 0.9 - 0.6)
    apply_material(chair, materials["dark_wood"])
    add_to_collection(chair, "interior")
    details.append(chair)
    
    # Add ship's wheel details
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.6,
        minor_radius=0.05,
        location=(-hull_length * 0.2, 0, hull_height * 0.7 + 0.3)
    )
    wheel_rim = bpy.context.active_object
    wheel_rim.name = "Wheel_Rim"
    apply_material(wheel_rim, materials["dark_wood"])
    add_to_collection(wheel_rim, "details")
    details.append(wheel_rim)
    
    # Create a helm stand
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=1.0,
        location=(-hull_length * 0.2, 0, hull_height * 0.7 - 0.2)
    )
    helm_stand = bpy.context.active_object
    helm_stand.name = "Helm_Stand"
    apply_material(helm_stand, materials["dark_wood"])
    add_to_collection(helm_stand, "details")
    details.append(helm_stand)
    
    # Create detailed ship's bell
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.2,
        depth=0.3,
        location=(-hull_length * 0.1, hull_width * 0.3, hull_height * 0.7 + 0.5)
    )
    bell = bpy.context.active_object
    bell.name = "Ship_Bell"
    bell.scale.z = 0.8
    bell.scale.x = 1.2
    bell.scale.y = 1.2
    
    # Create a bell material
    bell_material = create_material("Bell_Material", (0.8, 0.7, 0.2, 1.0), roughness=0.1, metallic=1.0)
    apply_material(bell, bell_material)
    add_to_collection(bell, "details")
    details.append(bell)
    
    # Create a small bell clapper inside the bell
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.05,
        location=(-hull_length * 0.1, hull_width * 0.3, hull_height * 0.7 + 0.3)
    )
    clapper = bpy.context.active_object
    clapper.name = "Bell_Clapper"
    apply_material(clapper, materials["iron"])
    add_to_collection(clapper, "details")
    details.append(clapper)
    
    # Create mounting frame for the bell
    bpy.ops.mesh.primitive_cube_add(size=1)
    bell_mount = bpy.context.active_object
    bell_mount.name = "Bell_Mount"
    bell_mount.scale = (0.05, 0.3, 0.05)
    bell_mount.location = (-hull_length * 0.1, hull_width * 0.3, hull_height * 0.7 + 0.7)
    apply_material(bell_mount, materials["dark_wood"])
    add_to_collection(bell_mount, "details")
    details.append(bell_mount)
    
    # Create treasure chest
    bpy.ops.mesh.primitive_cube_add(size=1)
    chest = bpy.context.active_object
    chest.name = "Treasure_Chest"
    chest.scale = (0.7, 0.4, 0.4)
    chest.location = (-hull_length * 0.3, -hull_width * 0.2, hull_height * 0.3 - 0.5)
    apply_material(chest, materials["dark_wood"])
    
    # Create chest lid
    bpy.ops.mesh.primitive_cube_add(size=1)
    chest_lid = bpy.context.active_object
    chest_lid.name = "Treasure_Chest_Lid"
    chest_lid.scale = (0.7, 0.4, 0.1)
    chest_lid.location = (-hull_length * 0.3, -hull_width * 0.2, hull_height * 0.3 - 0.1)
    apply_material(chest_lid, materials["dark_wood"])
    
    # Add chest hardware (lock and hinges)
    bpy.ops.mesh.primitive_cube_add(size=1)
    chest_lock = bpy.context.active_object
    chest_lock.name = "Chest_Lock"
    chest_lock.scale = (0.1, 0.1, 0.1)
    chest_lock.location = (-hull_length * 0.3 + 0.4, -hull_width * 0.2, hull_height * 0.3 - 0.2)
    apply_material(chest_lock, materials["iron"])
    
    # Add all chest parts to details
    for part in [chest, chest_lid, chest_lock]:
        add_to_collection(part, "interior")
        details.append(part)
    
    # Create navigation tools
    # Compass
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.2,
        depth=0.05,
        location=(-hull_length * 0.2 + 0.7, 0, hull_height * 0.7 + 0.3)
    )
    compass = bpy.context.active_object
    compass.name = "Compass"
    compass_material = create_material("Compass_Material", (0.1, 0.1, 0.1, 1.0), roughness=0.3)
    apply_material(compass, compass_material)
    add_to_collection(compass, "details")
    details.append(compass)
    
    # Create needle for compass
    bpy.ops.mesh.primitive_cube_add(size=1)
    needle = bpy.context.active_object
    needle.name = "Compass_Needle"
    needle.scale = (0.15, 0.02, 0.01)
    needle.location = (-hull_length * 0.2 + 0.7, 0, hull_height * 0.7 + 0.33)
    needle.rotation_euler = (0, 0, math.radians(45))
    
    # Two-colored needle material
    needle_n_material = create_material("Needle_North", (0.8, 0.1, 0.1, 1.0), roughness=0.3)
    # Apply to just one half of the needle
    apply_material(needle, needle_n_material)
    add_to_collection(needle, "details")
    details.append(needle)
    
    # Complete the pirate flag - create a proper Jolly Roger
    bpy.ops.mesh.primitive_plane_add(
        size=2.0,
        location=(0, 0, hull_height * 0.5 + 18)
    )
    flag = bpy.context.active_object
    flag.name = "Pirate_Flag"
    flag.scale = (1.0, 0.7, 1.0)
    flag.rotation_euler = (0, math.radians(45), 0)
    
    # Create black flag material
    flag_material = create_material("Flag_Black", (0.02, 0.02, 0.02, 1.0), roughness=0.8)
    apply_material(flag, flag_material)
    
    # Add cloth-like ripples to the flag
    bpy.ops.object.modifier_add(type='WAVE')
    flag.modifiers["Wave"].use_normal = True
    flag.modifiers["Wave"].use_normal_x = False
    flag.modifiers["Wave"].use_normal_y = True
    flag.modifiers["Wave"].use_normal_z = False
    flag.modifiers["Wave"].height = 0.1
    flag.modifiers["Wave"].width = 1.2
    flag.modifiers["Wave"].narrowness = 1.5
    flag.modifiers["Wave"].speed = 0.3
    
    # Add subdivision for smoother flag
    bpy.ops.object.modifier_add(type='SUBSURF')
    flag.modifiers["Subdivision"].levels = 2
    
    add_to_collection(flag, "details")
    details.append(flag)
    
    return details

def setup_scene_and_render():
    """Set up scene, lighting, camera and render settings"""
    # Configure world settings
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.05, 0.1, 0.2, 1.0)  # Dark blue sky
    bg.inputs[1].default_value = 1.0  # Strength
    
    # Create water surface
    bpy.ops.mesh.primitive_plane_add(size=200.0, location=(0.0, 0.0, -0.1))
    water = bpy.context.active_object
    water.name = "Ocean"
    apply_material(water, materials["water"])
    
    # Add water material nodes for realistic water effect
    water_mat = water.data.materials[0]
    nodes = water_mat.node_tree.nodes
    links = water_mat.node_tree.links
    
    # Add noise texture for water waves
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    noise = nodes.new(type='ShaderNodeTexNoise')
    bump = nodes.new(type='ShaderNodeBump')
    principled = nodes.get('Principled BSDF')
    
    # Position nodes
    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    noise.location = (-400, 0)
    bump.location = (-200, 0)
    
    # Configure noise
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 10.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # Configure bump
    bump.inputs['Strength'].default_value = 0.3
    
    # Connect nodes
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # Set alpha transparency
    if 'Alpha' in principled.inputs:
        principled.inputs['Alpha'].default_value = 0.9
    elif 'Transmission Weight' in principled.inputs:
        principled.inputs['Transmission Weight'].default_value = 0.1
    
    # Set material blend mode for transparency
    water_mat.blend_method = 'BLEND'
    
    # Add sun light for main illumination
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 5.0
    sun.data.angle = 0.1
    sun.rotation_euler = (math.radians(60), math.radians(30), math.radians(-45))
    
    # Add rim light to highlight the ship's contours
    bpy.ops.object.light_add(type='SUN', location=(-5, 5, 15))
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.energy = 2.0
    rim.data.color = (1.0, 0.9, 0.8)  # Warm rim light
    rim.rotation_euler = (math.radians(60), math.radians(-30), math.radians(45))
    
    # Add fill light for subtle illumination of shadowed areas
    bpy.ops.object.light_add(type='AREA', location=(0, -15, 10))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 20.0
    fill.data.color = (0.8, 0.9, 1.0)  # Cool fill light
    fill.data.size = 10.0
    fill.rotation_euler = (math.radians(90), 0, 0)
    
    # Create camera with good composition
    bpy.ops.object.camera_add(location=(30, -30, 15), rotation=(math.radians(60), 0, math.radians(45)))
    camera = bpy.context.active_object
    camera.name = "Main_Camera"
    
    # Set camera as active
    bpy.context.scene.camera = camera
    
    # Camera settings
    camera.data.lens = 50  # 50mm lens
    camera.data.sensor_width = 36.0  # 35mm film
    
    # Add depth of field for more realistic look
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 25.0
    camera.data.dof.aperture_fstop = 5.6
    
    # Set render settings
    render = bpy.context.scene.render
    render.engine = 'CYCLES'
    render.film_transparent = False
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100
    
    # Cycles settings for quality
    cycles = bpy.context.scene.cycles
    cycles.samples = 256
    cycles.use_denoising = True
    cycles.preview_samples = 32
    
    # Add compositor nodes for post-processing
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    
    # Clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    
    # Add render layers node
    render_layers = tree.nodes.new(type='CompositorNodeRLayers')
    render_layers.location = (0, 0)
    
    # Add color correction
    color_correction = tree.nodes.new(type='CompositorNodeColorCorrection')
    color_correction.location = (300, 0)
    
    # Enhance the blue colors for sea atmosphere
    color_correction.master_saturation = 1.1
    color_correction.master_contrast = 1.05
    if hasattr(color_correction, 'blue_gain'):
        color_correction.blue_gain = 1.05
    
    # Add vignette for more dramatic look
    lens_distortion = tree.nodes.new(type='CompositorNodeLensdist')
    lens_distortion.location = (600, 0)
    lens_distortion.use_jitter = True
    lens_distortion.use_projector = True
    
    # Slightly distort edges for more realism
    if hasattr(lens_distortion, 'dispersion'):
        lens_distortion.dispersion = 0.02
    
    # Add glare for highlights on water and metal
    glare = tree.nodes.new(type='CompositorNodeGlare')
    glare.location = (900, 0)
    glare.glare_type = 'FOG_GLOW'
    glare.quality = 'HIGH'
    glare.threshold = 0.8
    
    # Output node
    composite = tree.nodes.new(type='CompositorNodeComposite')
    composite.location = (1200, 0)
    
    # Connect nodes
    links = tree.links
    links.new(render_layers.outputs['Image'], color_correction.inputs['Image'])
    links.new(color_correction.outputs['Image'], lens_distortion.inputs['Image'])
    links.new(lens_distortion.outputs['Image'], glare.inputs['Image'])
    links.new(glare.outputs['Image'], composite.inputs['Image'])
    
    # Return references to important scene objects
    return {
        "sun": sun,
        "camera": camera,
        "water": water
    }

def create_pirate_ship():
    """Main function to create the entire pirate ship"""
    # Create hull
    hull = create_hull()
    
    # Create deck structures
    main_deck, quarter_deck, forecastle = create_deck_structures(hull)
    
    # Create masts with proper rotation
    masts = create_masts(hull)
    
    # Create furled sails
    sails = create_sails(masts)
    
    # Create rigging
    rigging = create_rigging(hull, masts)
    
    # Create additional details
    details = create_ship_details(hull)
    
    # Setup scene, lighting, and camera
    scene_elements = setup_scene_and_render()
    
    # Print completion message with statistics
    num_objects = len(bpy.data.objects)
    print(f"\nPirate ship created successfully with {num_objects} objects!")
    print(f"- Hull components: {len([obj for obj in bpy.data.objects if obj.name.startswith('Ship_') or obj.name.startswith('Keel')])}")
    print(f"- Masts: {len(masts)}")
    print(f"- Sails: {len(sails)}")
    print(f"- Rigging elements: {len(rigging)}")
    print(f"- Detailed parts: {len(details)}")
    print("\nCamera positioned for optimal view. Ready to render!")
    
    return hull, masts, sails, rigging, details

# Execute the main function to create the ship
if __name__ == "__main__":
    hull, masts, sails, rigging, details = create_pirate_ship()