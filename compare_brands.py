import csv

def compare_brands(file1, file2, output_file):
    """
    Compares the 'BrandName' column in file1 with the 'Name' column in file2
    and writes the discrepancies to a new CSV file.
    """
    discrepancies = []

    with open(file1, 'r', encoding='utf-8') as f1, \
            open(file2, 'r', encoding='utf-8') as f2:
        reader1 = csv.DictReader(f1)
        reader2 = csv.DictReader(f2, delimiter='\t')

        # Create dictionaries for faster lookup
        brands1 = {row['BrandName'].strip(): row for row in reader1}
        brands2 = {row['Name'].strip(): row for row in reader2}

        discrepancies = []

        # Find discrepancies
        for brand_name, row1 in brands1.items():
            if brand_name not in brands2:
                discrepancies.append({
                    'BrandName (from DATA_FILE)': brand_name,
                    'Name (from STATISTICS_FILE)': None,
                    'Should Be': brand_name
                })

        for name, row2 in brands2.items():
            if name not in brands1:
                discrepancies.append({
                    'BrandName (from DATA_FILE)': None,
                    'Name (from STATISTICS_FILE)': name,
                    'Should Be': name
                })

    # Write discrepancies to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['BrandName (from DATA_FILE)', 'Name (from STATISTICS_FILE)', 'Should Be']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(discrepancies)

if __name__ == "__main__":
    file1 = "BrandList.csv"
    file2 = "Brands-Statistics-2025-02-25-16-54-04.csv"
    output_file = "brand_discrepancies.csv"
    compare_brands(file1, file2, output_file)
    print(f"Discrepancies written to {output_file}")