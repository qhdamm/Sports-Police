import os
import sys
sys.path.append('./NSAQA')
import pickle
from models.detectron2.detectors import get_platform_detector, get_diver_detector, get_splash_detector
from models.pose_estimator.pose_estimator_model_setup import get_pose_estimation, get_pose_model
from rule_based_programs.scoring_functions import *
from score_report_generation.generate_report_functions import *
from rule_based_programs.aqa_metaProgram import add_difficulty, aqa_metaprogram, abstractSymbols, extract_frames, extract_frames_ocr
import argparse

def main(video_path):
    platform_detector = get_platform_detector()
    splash_detector = get_splash_detector()
    diver_detector = get_diver_detector()
    pose_model = get_pose_model()
    template_path = 'report_template_tables.html'
    summary_template_path = 'report_summary_template_table.html'
    dive_data = {}

    frames = extract_frames(video_path)
    ocr_frames = extract_frames_ocr(video_path)
    dive_data = abstractSymbols(frames, platform_detector=platform_detector, splash_detector=splash_detector, diver_detector=diver_detector, pose_model=pose_model)
    dive_data = add_difficulty(ocr_frames, dive_data)   # difficulty 추가 부분
    dive_data = aqa_metaprogram(frames, dive_data, platform_detector=platform_detector, splash_detector=splash_detector, diver_detector=diver_detector, pose_model=pose_model)
    
    intermediate_scores = get_all_report_scores(dive_data)
    html, html_id = generate_report_from_frames(template_path, intermediate_scores, frames)
    summary_html, summary_html_id = generate_report_from_frames(summary_template_path, intermediate_scores, frames)

    import os
    # Define the save path
    save_directory = "./output"
    filename = os.path.basename(video_path)
    
    save_path_html = os.path.join(save_directory, f"{os.path.splitext(filename)[0]}_report.html")
    save_path_summary_html = os.path.join(save_directory, f"{os.path.splitext(filename)[0]}_summary_report.html")
    
    # Save the main HTML report
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Save the HTML report
    with open(save_path_html, 'w') as f:
        print("Saving HTML report into " + save_path_html)
        f.write(html)
    
    with open(save_path_summary_html, 'w') as f:
        print("Saving summary HTML report into " + save_path_summary_html)
        f.write(summary_html)
        
    return html_id, save_path_html, summary_html_id, save_path_summary_html

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NSAQA Dive Score Report Generator")
    parser.add_argument('video_path', type=str, help="Path to the dive video")

    args = parser.parse_args()

    main(args.video_path)


