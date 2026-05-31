import os

folder = r'd:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\wwwroot\images\products'
files = sorted(os.listdir(folder))
with open('image_list.txt', 'w', encoding='utf-8') as out:
    for f in files:
        out.write(f + '\n')
print(f'Written {len(files)} filenames')
