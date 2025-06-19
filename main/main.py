import pandas as pd
from pathlib import Path
from rag import Retriever


def main():
    input_folder = Path(r"C:\Users\bekal\OneDrive\Desktop\AI4SE\Litterature\RAG\test-input")
    output_folder = Path(r"C:\Users\bekal\OneDrive\Desktop\AI4SE\Litterature\RAG\test-output")
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