from output_scorer import score_output_direct_non_destructive as score
from io_helper import parse_input, parse_output
from shutil import copyfile
import os

path_output_1 = "./outputs_1"
path_output_2 = "./outputs_2"
path_output_3 = "./outputs_3"

def compare_find_best_solution(size, input_folder, input_path, *output_args):
	'''
	Compares 3 output files and determines the best output file
	'''
	dest_file = "./outputs/" + size + "/" + input_folder + ".out"

	graph, num_buses, size_bus, constraints = parse_input(input_path)

	outputs = list(output_args)
	ass = [parse_output(o) for o in outputs]
	scores = [score(graph, num_buses, size_bus, constraints, a) for a in ass]

	src_file = outputs[scores.index(max(scores))]

	fw = open(dest_file, "w")
	fw.close()
	copyfile(src_file, dest_file)


def comprehensive(s_size="", start=""):
	all_size = ["small", "medium", "large"]
	for size in all_size:
		inputs = os.listdir("./all_inputs/" + size)
		if ".DS_Store" in inputs:
			inputs.remove(".DS_Store")
		for input_folder in inputs:
			ip = "./all_inputs/" + size + "/" + input_folder
			o1 = path_output_1 + "/" + size + "/" + input_folder + ".out"
			o2 = path_output_2 + "/" + size + "/" + input_folder + ".out"
			o3 = path_output_3 + "/" + size + "/" + input_folder + ".out"
			print("Comparing {} {}.".format(size, input_folder))
			compare_find_best_solution(size, input_folder, ip, o1, o2, o3)

if __name__ == '__main__':
	comprehensive()
	
