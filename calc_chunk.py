import os

def calculate_averages(directory):
    paragraph_lengths = []
    file_lengths = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Strip leading and trailing whitespace
                    content = content.strip()
                    
                    # Split text into paragraphs by double newline
                    paragraphs = content.split('\n\n')
                    
                    # Calculate the length of each paragraph
                    for para in paragraphs:
                        paragraph_lengths.append(len(para))
                    
                    # Calculate the length of the entire file
                    file_lengths.append(len(content))
    
    # Average paragraph length
    average_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
    
    # Average file length
    average_file_length = sum(file_lengths) / len(file_lengths) if file_lengths else 0
    
    return average_paragraph_length, average_file_length

directory_path = "processed_docs"  # Path to directory with .md files
average_paragraph_length, average_file_length = calculate_averages(directory_path)
print(f"Average paragraph length: {average_paragraph_length:.2f} characters")
print(f"Average file length: {average_file_length:.2f} characters")