import os
import re
from difflib import ndiff
from termcolor import colored
from collections import Counter


def check_plagiarism(file1_path, file2_path, threshold=50, case_sensitive=False):
    # Check if files exist
    if not os.path.exists(file1_path):
        print(f"Error: {file1_path} does not exist.")
        return
    if not os.path.exists(file2_path):
        print(f"Error: {file2_path} does not exist.")
        return

    try:
        # Open both files and read content
        with open(file1_path, 'r', encoding='utf-8') as first_file, open(file2_path, 'r', encoding='utf-8') as second_file:
            file1 = first_file.read()
            file2 = second_file.read()

            # Case comparison if needed
            if not case_sensitive:
                file1 = file1.lower()
                file2 = file2.lower()

            #  whitespace and split into exact words
            file1_words = re.findall(r'\b\w+\b', file1)
            file2_words = re.findall(r'\b\w+\b', file2)

            # Find exact matches
            common_words = set(file1_words) & set(file2_words)
            total_words = set(file1_words) | set(file2_words)

            # Similarity calculation 
            similarity_percentage = int((len(common_words) / max(len(total_words), 1)) * 100)

            print(f"Plagiarism Check Result: {similarity_percentage}% Similarity")

            # Word length
            word_count_1 = len(file1_words)
            word_count_2 = len(file2_words)
            print(f"File 1 Word Count: {word_count_1}")
            print(f"File 2 Word Count: {word_count_2}")
            print(f"Common Words: {len(common_words)}")

            # Word frequency counts
            word_freq1 = Counter(file1_words)
            word_freq2 = Counter(file2_words)
            print(f"\nTop words in File 1: {word_freq1.most_common(5)}")
            print(f"Top words in File 2: {word_freq2.most_common(5)}")

            # Color-coded differences
            print("\nDifferences (with color):")
            diff = ndiff(file1.splitlines(), file2.splitlines())
            for line in diff:
                if line.startswith('-'):
                    print(colored(line, 'red'))  # Lines in file1
                elif line.startswith('+'):
                    print(colored(line, 'green'))  # Lines in file2
                else:
                    print(line)  # Unchanged lines

            # Threshold-based warning
            if similarity_percentage >= threshold:
                print("Warning: This content may be plagiarized!")
            else:
                print("Content is not plagiarized.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
file1_path = 'file1.txt'
file2_path = 'file2.txt'
threshold = 40

check_plagiarism(file1_path, file2_path, threshold)
