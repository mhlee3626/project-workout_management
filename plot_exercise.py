# plot_generator.py
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta


from collections import OrderedDict

def exercise_plot( formatted_data, title):


    # print('formatted_data',formatted_data)

    dates = [datetime.strptime(item[-1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') for item in formatted_data]
    dates2 =[datetime.strptime(item, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') + ' 00:00:00' for item in dates]
    
    #익일 추가
    # # Find the most recent date
    # most_recent_date = max(dates2)

    # # Convert it to a datetime object
    # most_recent_datetime = datetime.strptime(most_recent_date, '%Y-%m-%d %H:%M:%S')

    # # Calculate the next date
    # next_date = most_recent_datetime + timedelta(days=1)

    # # Convert the next date back to string format
    # next_date_str = next_date.strftime('%Y-%m-%d') + ' 00:00:00'

    # # Append the next date to dates2
    # dates2.append(next_date_str)

    dates_line=(sorted(dates+dates2))

    weights = [item[2] for item in formatted_data]
    weights2 = [weights[dates.index(date)] if date in dates else 0 for date in dates_line]

    reps = [item[3] for item in formatted_data]
    reps2 = [reps[dates.index(date)] if date in dates else 0 for date in dates_line]

    sets = [item[4] for item in formatted_data]
    sets2 = [sets[dates.index(date)] if date in dates else 0 for date in dates_line]

    depth = ['보통' if item[5] in ['2', 2] else '깊게' if item[5] in ['3', 3] else '얕게' for item in formatted_data]
    depth2 = [depth[dates.index(date)] if date in dates else '' for date in dates_line]

    width = ['보통' if item[6] in ['2', 2] else '넓게' if item[6] in ['3', 3] else '좁게' for item in formatted_data]
    width2 = [width[dates.index(date)] if date in dates else '' for date in dates_line]

    angle = ['플랫' if item[7] in ['2', 2] else '인클라인' if item[7] in ['3', 3] else '디클라인' for item in formatted_data]
    angle2 = [angle[dates.index(date)] if date in dates else '' for date in dates_line]

    rest = [item[8] for item in formatted_data]
    rest2 = [rest[dates.index(date)] if date in dates else 0 for date in dates_line]

    total_score = []

    for item in formatted_data:
        # Check if any of the values is 0
        if 0 in (item[2], item[3], item[4], item[5], item[8]):
            # Replace 0 values with 1
            modified_item = [1 if x == 0 else x for x in (item[2], item[3], item[4], item[5], item[8])]
            # Calculate total_score and append to the list
            total_score.append(modified_item[0] * modified_item[1] * modified_item[2] * modified_item[3] / modified_item[4])
        else:
            # Calculate total_score and append to the list directly
            total_score.append(item[2] * item[3] * item[4] * item[5] / item[8])

    total_score2=[total_score[dates.index(date)] if date in dates else 0 for date in dates_line]
    # total_score2=[total_score[dates.index(date)] if date in dates else None for date in dates_line] >>y축값 순서가 뒤섞임

# weights2, reps2, sets2, depth2, width2, angle2, rest2, total_score 사용


    
    plt.figure(figsize=(6, 50))


    # weights plot
    plt.subplot(8, 1, 1)
    plt.plot(dates_line, weights2, marker='o', color='blue')
    plt.ylabel('kg')
    plt.title(f'{title} 중량', fontweight='bold')
    plt.xticks(rotation=45)
    # 일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 2)
    plt.plot(dates_line, reps2, marker='o', color='green')
    plt.ylabel('reps')
    plt.title(f'{title} 반복 횟수', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 3)
    plt.plot(dates_line, sets2, marker='o', color='orange')
    plt.ylabel('sets')
    plt.title(f'{title} 셋트 수', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 4)
    plt.plot(dates_line, depth2, marker='o', color='purple')
    plt.title(f'{title} 깊이', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 5)
    plt.plot(dates_line, width2, marker='o', color='skyblue')
    plt.title(f'{title} 너비', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 6)
    plt.plot(dates_line, angle2, marker='o', color='skyblue')
    plt.title(f'{title} 각도', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 7)
    plt.plot(dates_line, rest2, marker='o', color='navy')
    plt.ylabel('분')
    plt.title(f'{title} 휴식시간', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

    plt.subplot(8, 1, 8)
    plt.plot(dates_line, total_score2, marker='o', color='red')
    plt.title(f'{title} 총 운동량', fontweight='bold')
    plt.xticks(rotation=45)
    #일별 경계선 추가
    for date in dates2:
        plt.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)


    plt.subplots_adjust(wspace=0.5, hspace=0.5)


    # # Add markers and labels for depth, width, angle, and rest above the points on the first y-axis plot
    # for i, (x, y, rep, s, d, w, a, r) in enumerate(zip(time_data, weights, reps, sets, depth, width, angle, rest)):
    #     if d is not None and w is not None and a is not None and r is not None:
    #         ax1.annotate(f"Weights {y}\nReps: {rep}\nSets: {s}\nDepth: {d}\nWidth: {w}\nAngle: {a}\nRest: {r}",
    #                       (x, y),
    #                       textcoords="offset points",
    #                       xytext=(0, 10),
    #                       ha='center')

    # # 그래프 제목과 범례 추가
    # plt.title(title)
    # ax1.legend(loc='upper left')
    # ax2.legend(loc='upper right')

    # 그래프를 이미지로 변환
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    # 메모 데이터 생성
    memo_data = [item[-2] for item in formatted_data]
    print('memo_data',memo_data)
    date_memo_dict = dict(zip(dates_line, memo_data))
    print('date_memo_data',date_memo_dict)


    return img_data,date_memo_dict
