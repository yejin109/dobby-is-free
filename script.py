from itertools import product


conf_years = [2022]
conf_keywords = [
    'graph', 'generative',
]

arxiv_dates = ["Tue, 18 Jul 2023",
               ]

with open('./routine.bat', 'w') as f:
    for year, keyword in product(conf_years, conf_keywords):
        f.write(f"python main.py --target_conf --conf_year {year} --conf_keyword {keyword}\n")

    for date in product(arxiv_dates):
        date = date[0]
        # f.write(f'python main.py --target_arxiv --date "{str(date)}"\n')
