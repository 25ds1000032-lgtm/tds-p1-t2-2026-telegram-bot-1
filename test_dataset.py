from dataset import download_file, analyze_dataset


url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


file = download_file(url)


result = analyze_dataset(file)


print(result)