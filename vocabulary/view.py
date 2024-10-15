import csv
from django.shortcuts import render


def display_csv(request):
    # Path to your CSV file
    csv_file_path = 'path/to/your/csvfile.csv'
    data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    return render(request, 'display_csv.html', {'data': data})
