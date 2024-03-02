import utils_email_converter as uec
import os

def main():
    input_directory = 'samples'
    output_mbox_file = 'samples_res/emails-samples.mbox'

    # Clear the output directory first
    output_directory = os.path.dirname(output_mbox_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        uec.clear_directory(output_directory)

    uec.eml_to_mbox(input_directory, output_mbox_file)

if __name__ == '__main__':
    main()