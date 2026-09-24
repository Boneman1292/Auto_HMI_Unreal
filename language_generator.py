import csv
import polib
import os

def generate_po_files_from_csv(csv_filepath):
    # Open the CSV using utf-8-sig to handle any BOM characters from Excel
    with open(csv_filepath, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        
        # Read the first row to determine the structure dynamically
        headers = next(reader)
        
        # Ensure the CSV has at least Key, SourceString, and one target language
        if len(headers) < 3:
            raise ValueError("CSV requires at least 3 columns: Key, SourceString, and one Target Language.")
            
        languages = headers[2:]
        
        # Initialize a separate PO file object for each language column
        po_catalogs = {}
        for lang in languages:
            clean_lang = lang.strip()
            po = polib.POFile()
            po.metadata = {
                'Project-Id-Version': '1.0',
                'Language': clean_lang,
                'MIME-Version': '1.0',
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Transfer-Encoding': '8bit',
            }
            po_catalogs[clean_lang] = po
            
        # Process each subsequent row in the CSV
        for row in reader:
            # Skip completely empty rows or rows without a Key
            if not row or not row[0].strip():
                continue 
                
            key = row[0].strip()
            source_string = row[1].strip() if len(row) > 1 else ""
            
            # Create an entry for each language and append it to the respective PO object
            for index, lang in enumerate(languages):
                clean_lang = lang.strip()
                col_index = index + 2
                
                # Safely get the translation (handles rows missing trailing commas)
                translation = row[col_index].strip() if col_index < len(row) else ""
                
                entry = polib.POEntry(
                    msgctxt=f"UI_Strings,{key}",
                    msgid=source_string,
                    msgstr=translation
           	)
                po_catalogs[clean_lang].append(entry)
                
    # Save all generated PO files to the current directory
    for lang, po in po_catalogs.items():
        filename = f"{lang}.po"
        po.save(filename)
        print(f"Generated {filename} containing {len(po)} translated entries.")

if __name__ == "__main__":
    generate_po_files_from_csv('Language_Table.csv')