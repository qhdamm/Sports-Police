"""
nsaqa.py
Author: Lauren Okamoto
"""
import os
import sys
sys.path.append('./NSAQA')
import pickle
from models.detectron2.detectors import get_platform_detector, get_diver_detector, get_splash_detector
from models.pose_estimator.pose_estimator_model_setup import get_pose_estimation, get_pose_model
from rule_based_programs.scoring_functions import *
from score_report_generation.generate_report_functions import *
from rule_based_programs.aqa_metaProgram import aqa_metaprogram, abstractSymbols, extract_frames
import argparse
from bs4 import BeautifulSoup
import openai


def main(video_path):
    platform_detector = get_platform_detector()
    splash_detector = get_splash_detector()
    diver_detector = get_diver_detector()
    pose_model = get_pose_model()
    template_path = 'report_template_tables.html'
    dive_data = {}

    frames = extract_frames(video_path)
    dive_data = abstractSymbols(frames, platform_detector=platform_detector, splash_detector=splash_detector, diver_detector=diver_detector, pose_model=pose_model)
    dive_data = aqa_metaprogram(frames, dive_data, platform_detector=platform_detector, splash_detector=splash_detector, diver_detector=diver_detector, pose_model=pose_model)
    intermediate_scores = get_all_report_scores(dive_data)
    html, html_id = generate_report_from_frames(template_path, intermediate_scores, frames)

    import os
    # Define the save path
    save_directory = "./output"
    save_path = os.path.join(save_directory, "{}_report.html".format("".join(video_path.split('.')[:-1])))
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Save the HTML report
    with open(save_path, 'w') as f:
        print("saving html report into " + save_path)
        f.write(html)

    return html_id, save_path

    





    

