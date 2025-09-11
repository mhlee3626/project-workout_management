import matplotlib.pyplot as plt
from io import BytesIO
import base64

from collections import defaultdict

from datetime import datetime
import pytz

def korea_time():
    # 한국 시간대를 설정합니다.
    korea_tz = pytz.timezone('Asia/Seoul')

    # 현재 시각을 가져와 한국 시간대로 변환합니다.
    now_korea = datetime.now(korea_tz)
    # 년월일 정보를 가져옵니다.
    year = now_korea.year
    month = now_korea.month
    day = now_korea.day

    # Y:M:D 형식으로 날짜 정보를 출력합니다.
    today = f"{year:04d}-{month:02d}-{day:02d}"
    print("한국 시간:", today)
    return today


def calory_plot(data1,data2):

    
    # Merged dictionary
    merged_data = defaultdict(dict)

    # Merge data1 into merged_data
    for key, value in data1.items():
        date_key = key.split()[0]  # Extracting the date part
        merged_data[date_key].update(value)

    # Merge data2 into merged_data
    for key, value in data2.items():
        # date_key = key.split()[0]  # Extracting the date part
        merged_data[key].update(value)

    # Convert defaultdict back to a regular dictionary
    data = dict(merged_data)
    # data=sorted(data.keys())

    # Extracting dates and corresponding calorie values
    dates = sorted(list(data.keys()))
    calories = [data[date]['calories'] if 'calories' in data[date] else 0 for date in dates]
    req_calories = [data[date]['req_calories'] if 'req_calories' in data[date] else 0 for date in dates]

    protein = [data[date]['protein'] if 'calories' in data[date] else 0 for date in dates]
    req_protein = [data[date]['req_protein'] if 'req_calories' in data[date] else 0 for date in dates]

    today=korea_time()

    print('(req_calories[-1],calories[-1],req_protein[-1],protein[-1])',req_calories[-1],calories[-1],req_protein[-1],protein[-1])

    if today==dates[-1]:
        alert_calories=int(req_calories[-1]-calories[-1])
        alert_protein=int(req_protein[-1]-protein[-1])
    else:
        alert_calories,alert_protein=None,None
    
    # Plotting
    plt.figure(figsize=(8, 6))

    # Calories plot
    plt.subplot(2, 1, 1)
    plt.plot(dates, calories, marker='o', label='섭취한 칼로리', color='blue')
    plt.plot(dates, req_calories, marker='x', label='필요한 칼로리', color='red')
    plt.ylabel('kcal', fontweight='bold')
    plt.title('칼로리 섭취량과 칼로리 필요량')
    plt.xticks(rotation=45)
    plt.legend()

    # Protein plot
    plt.subplot(2, 1, 2)
    plt.plot(dates, protein, marker='o', label='단백질 섭취량', color='green')
    plt.plot(dates, req_protein, marker='x', label='단백질 필요량', color='purple')
    plt.ylabel('g', fontweight='bold')
    plt.title('단백질 섭취량과 단백질 필요량')
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplots_adjust(wspace=0.5, hspace=1)

    # 그래프를 이미지로 변환
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    plt.close()  # Close the plot to free up resources

    return img_data,alert_calories,alert_protein,today
