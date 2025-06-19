import pandas as pd
from pathlib import Path
from rag import Retriever


INPUT_FILE_PATH = "input_files" # Path to the folder containing input files
OUTPUT_FILE_PATH = "output_files" # Path to the folder where output files will be saved

def main():
    input_folder = Path(INPUT_FILE_PATH)
    output_folder = Path(OUTPUT_FILE_PATH)
    output_folder.mkdir(exist_ok=True)

    query = "Summarize the key points of this document or the main argument."
    retriever = Retriever(model_name="deepseek-r1:7b")
    files = set(list(input_folder.glob("*.txt")) + list(input_folder.glob("*.pdf")) + list(input_folder.glob("*.PDF")))
    print(f"Found {len(files)} files in the input folder.")

    if not files:
        print("No supported files found in the input folder.")
        return

    results = []
    for file in files:
        print(f"\nProcessing file: {file.name} with RAG.")
        result = retriever(file, output_folder, query)
        if result:
            results.append(result)

    if results:
        df = pd.DataFrame(results, columns=["Filename", "Summary"])
        excel_path = output_folder / "summaries.xlsx"
        df.to_excel(excel_path, index=False)
        print(f"\nAll summaries saved to {excel_path}")


if __name__ == "__main__":
    main()