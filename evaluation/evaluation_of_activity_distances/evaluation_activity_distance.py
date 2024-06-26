from pm4py.statistics.variants.log import get as variants_module
# from pm4py.algo.evaluation.earth_mover_distance import algorithm as emd_evaluator
from pm4py.statistics.variants.log import get as variants_module
from pm4py.objects.log.importer.xes import importer as xes_importer

from definitions import ROOT_DIR
from evaluation.data_util.algorithm import get_log_control_flow_perspective, get_alphabet, get_activities_to_replace, \
    get_logs_with_replaced_activities_dict, get_activity_distance_matrix_dict, get_n_nearest_neighbors

log = xes_importer.apply(ROOT_DIR + '/repairExample.xes')

log_control_flow_perspective = get_log_control_flow_perspective(
    log)  # transform log to a list of lists of activity labels
alphabet = get_alphabet(log_control_flow_perspective)

different_activities_to_replace_count = 2
activities_to_replace_with_count = 10

# 1: get the activities that we want to replace in each run
activities_to_replace_in_each_run_list = get_activities_to_replace(alphabet, different_activities_to_replace_count)
# 2: replace activities
logs_with_replaced_activities_dict = get_logs_with_replaced_activities_dict(activities_to_replace_in_each_run_list,
                                                                            log_control_flow_perspective,
                                                                            different_activities_to_replace_count,
                                                                            activities_to_replace_with_count)

# 3: compute for all logs all activity distance matrices
# activity_distance_functions we want to evaluate
activity_distance_functions = []
activity_distance_functions.append("Bose 2009 Substitution Scores")

activity_distance_matrix_dict = get_activity_distance_matrix_dict(activity_distance_functions,
                                                                  logs_with_replaced_activities_dict)

# 4: evaluation of all activity distance matrices
for replaced_activities in activity_distance_matrix_dict["Bose 2009 Substitution Scores"].keys():
    nearest_neighbors = get_n_nearest_neighbors(activities_to_replace_with_count, replaced_activities,
                                                activity_distance_matrix_dict["Bose 2009 Substitution Scores"][
                                                    replaced_activities], activities_to_replace_with_count)

language = variants_module.get_language(log)

# emd = emd_evaluator.apply(language, language)
