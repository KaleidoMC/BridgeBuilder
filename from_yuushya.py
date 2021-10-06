import os
import json
from pathlib import Path
import shutil
import sys

from utils.tagspaces_getter import Tags
from utils.tagspaces_getter import TagDef
import tagdefs

def main():
	#namespace = input("Namespace: ")
	folder = "yuushya"
	namespace = "yuushya"

	os.chdir(folder)

	regist = Path("./regist/block.json")
	regist = json.loads(regist.read_text())["block"]
	fails = list()

	for reg in regist:
		print("Process " + reg["name"])
		try:
			states_json = json.loads(Path("./blockstates/" + reg["name"] + ".json").read_text())
			models = [];
			for variant in states_json["variants"].keys():
				variant = states_json["variants"][variant]
				if isinstance(variant, list):
					for subvar in variant:
						models.append(subvar["model"])
				else:
					models.append(variant["model"])
			models = set(models)
			
			defs = []
			if "rendertype" in reg:
				if reg["rendertype"] == "translucent":
					defs.append(tagdefs.layer.translucent)
				elif reg["rendertype"] == "cutout":
					defs.append(tagdefs.layer.cutout)
			else:
				if reg["itemgroup"] == "yuushya_decoration" or reg["itemgroup"] == "yuushya_signs":
					defs.append(tagdefs.layer.cutout)

			if reg["classtype"] == "PlainBlock" and "properties" not in reg:
				defs.append(tagdefs.template.block)
			if reg["classtype"] == "TableBlock":
				defs.append(tagdefs.shape_block)
			elif reg["classtype"] == "IntactBlock" and "issoild" in reg and reg["issoild"]:
				defs.append(tagdefs.template.horizontal)
			elif reg["classtype"] == "SemiBlock" or reg["classtype"] == "LayerBlock":
				defs.append(tagdefs.skip)
			elif reg["classtype"] == "BoardBlock" or reg["classtype"] == "PlantBlock":
				if "rendertype" not in reg:
					defs.append(tagdefs.layer.cutout)
			
			if len(models) > 1:
				group = TagDef("g." + reg["name"], "#4986e7ff", "white")
				defs.append(group)
			for model in models:
				model = model[model.find(":")+1:]
				model_path = Path("./models/" + model + ".json")
				tags = Tags(model_path)
				tags.remove("skip2")
				for tagdef in defs:
					tags.add(tagdef)
			
			"""
			tags = Tags(model_path)
			skip = False
			for prefix in skip_prefixes:
				if filename.startswith(prefix):
					print("Skip template model " + prefix)
					skip = True
					break
			if skip:
				tags.add(tagdefs.skip)
				continue
			
			with open(model_path) as json_file:
				json_text = json.load(json_file)
				glass = filename.startswith("window_")
				cutout = False
				solid = False
				if glass:
					cutout = True
				elif "leaves" in filename:
					cutout = True
				elif filename.startswith("neon_"):
					tags.add(tagdefs.layer.translucent)
				
				if "parent" in json_text:
					parent = json_text["parent"]
					if parent in skip_models:
						print("Skip " + json_text["parent"])
						tags.add(tagdefs.skip)
						continue
					if parent in block_models:
						solid = True
					elif parent.startswith("block/cube"):
						solid = True
					if not cutout:
						if parent in cutout_models:
							cutout = True
				elif "textures" not in json_text:
					print("Skip template model")
					tags.add(tagdefs.skip)
					continue
				if not cutout:
					for prefix in cutout_prefixes:
						if filename.startswith(prefix):
							cutout = True
							break
					
				if glass:
					tags.add(tagdefs.glass)
				if cutout:
					tags.add(tagdefs.layer.cutout)
					if solid:
						tags.add(tagdefs.shape_block)
				elif solid:
					tags.add(tagdefs.template.block)
			"""
				
		except Exception as e:
			print(e)
			raise e
			fails.append(filename)

	print("Fails:\n" + "\n".join(fails))

main()
