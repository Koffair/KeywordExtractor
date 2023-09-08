from src.hu_keywords import extract_keywords

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="the path to the input directory")
    parser.add_argument("-o", "--output", help="the path to the output directory")
    args = parser.parse_args()

    txt_files = [os.path.join(args.input, f) for f in os.listdir(args.input)
                 if os.path.isfile(os.path.join(args.input, f))]
    for txt_file in txt_files:
        with open(txt_file, "r") as infile:
            txt = infile.read()
        try:
            keywords = "\n".join(extract_keywords(txt)) # complains if it is empty
            kw_file = os.path.join(args.output, txt_file.split("/")[-1])
            with open(kw_file, "w") as outfile:
                outfile.write(keywords)
        except Exception as e:  ## if it is empty, pass
            continue


    # take input folder
    # for file in input folder
    ##### extract keywords
    ##### save keywords into a text file in output folder

