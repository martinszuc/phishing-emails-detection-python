import os
import utils_feature_extraction as ufe

def main():
    # Define the resources directory where your .mbox files are located
    resources_dir = 'res/'
    
    # Process emails-phishing-pot.mbox
    phishing_pot_path = os.path.join(resources_dir, "emails-phishing-pot.mbox")
    print(f"Processing {phishing_pot_path} with encoding iso-8859-1, limit 2279, is_phishy True...")
    ufe.process_mbox_to_csv(phishing_pot_path, "iso-8859-1", limit=2279, is_phishy=True)
    
    # Process emails-enron.mbox
    enron_path = os.path.join(resources_dir, "emails-enron.mbox")
    print(f"Processing {enron_path}  limit 2257, is_phishy False..")
    ufe.process_mbox_to_csv(enron_path, "ascii", limit=2257, is_phishy=False)
    
    print("Finished processing all files.")

if __name__ == "__main__":
    main()
