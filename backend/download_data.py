import os
import requests

DATA_DIR = "data"

CATEGORIES = {
    "Handwritten Prescription": [
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop1.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop2.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop3.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop4.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop5.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop6.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop7.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop8.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop9.jpg",
        "https://raw.githubusercontent.com/Infi-09/Doctor-Prescripton-Handwritten-Recoginition/main/demo/tes1/crop10.jpg",
        "https://raw.githubusercontent.com/shubhm-gupta/Keywords-Identification-from-Handwritten-Doctor-Prescription/master/pres.jpg",
        "https://raw.githubusercontent.com/djdhar/Handwritten-and-Printed-Text-Classification-in-Doctors-Prescription/master/Prescription%20Text%20Localization%20and%20Classification/Prescription_Samples/sample1.jpg",
        "https://raw.githubusercontent.com/djdhar/Handwritten-and-Printed-Text-Classification-in-Doctors-Prescription/master/sample12.jpg",
        "https://raw.githubusercontent.com/djdhar/Handwritten-and-Printed-Text-Classification-in-Doctors-Prescription/master/Prescription%20Text%20Localization%20and%20Classification/Prescription_Samples/sample3.png",
        "https://raw.githubusercontent.com/djdhar/Handwritten-and-Printed-Text-Classification-in-Doctors-Prescription/master/Prescription%20Text%20Localization%20and%20Classification/Prescription_Samples/sample4.jpg"
    ],
    "Printed Prescription": [
        "https://raw.githubusercontent.com/JohnSnowLabs/spark-nlp-workshop/master/healthcare-nlp/data/ocr/prescription_01.png",
        "https://raw.githubusercontent.com/JohnSnowLabs/spark-nlp-workshop/master/healthcare-nlp/data/ocr/prescription_02.png",
        "https://upload.wikimedia.org/wikipedia/commons/1/14/Drug1-page0001.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/07/SMS_format_of_eRecept.png",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr_output/1.png",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr_output/2.png",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr/test_images/1.jpg",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr/test_images/2.jpg",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr/test_images/3.jpg",
        "https://raw.githubusercontent.com/Aniket025/Medical-Prescription-OCR/master/Model-5/ocr/test_images/4.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/bd/Forma_107-1-u.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/ba/Forma_n_148-1u-88.png",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/MedicalCannabisPrescription_NY.jpg"
    ],
    "Printed Lab Report": [
        "https://raw.githubusercontent.com/DeepLumiere/MedOCR/main/labimage.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Gnuhealth_lab_test_report.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/Sars-cov-2_neutralizing_antibody_test_result.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Blood_test_report_of_an_Indian_man.jpg/1024px-Blood_test_report_of_an_Indian_man.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Lipid_panel_report.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/69/Blood_Donor_Health_Screening_Report.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/4c/CBC_report.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/Complete_blood_count_and_differential.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3b/Example_of_a_Complete_Blood_Count.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/Example_of_complete_blood_count_and_differential_results_in_chronic_myeloid_leukemia.png"
    ],
    "Medical Scans (X-Ray-MRI)": [
        "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/000001-1.jpg",
        "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/000001-2.jpg",
        "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/000001-3.jpg",
        "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/000001-4.jpg",
        "https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/images/000001-5.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/71/Jaccoud_arthropathy_hand_x-ray_front.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/79/First_medical_X-ray_by_Wilhelm_R%C3%B6ntgen_of_his_wife_Anna_Bertha_Ludwig%27s_hand_-_18951222.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/77/X-ray_of_hand%2C_where_bone_age_is_automatically_found_by_BoneXpert_software.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/45/X-Ray_Photograph_of_Tesla%27s_left_hand.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e2/X-ray_of_normal_hand_by_dorsoplantar_projection.jpg"
    ]
}

def download_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    for category, urls in CATEGORIES.items():
        cat_path = os.path.join(DATA_DIR, category)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)
            print(f"Created category directory: {cat_path}")

        for i, url in enumerate(urls):
            ext = url.split('.')[-1]
            if len(ext) > 4: ext = "jpg" # fallback
            filename = f"sample_{i+1}.{ext}"
            filepath = os.path.join(cat_path, filename)
            
            print(f"Downloading {category} sample {i+1}...")
            try:
                headers = {'User-Agent': 'MedicalClassifier/1.0 (contact: admin@medclassify.org)'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved to {filepath}")
                else:
                    print(f"Failed to download {url}: Status {response.status_code}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    download_data()
