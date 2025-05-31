def reward_function(params):
    """
    Index 기반으로 Reinvent 2018 트랙 레이싱 라인을 따라가도록 설계된 보상 함수
    """

    # 1) 중앙선 편차 계산 (0.0 = 중앙, 1.0 = 트랙 가장자리)
    center_variance = params["distance_from_center"] / params["track_width"]

    # 2) 미리 정의한 웨이포인트 인덱스 구역
    left_lane = [
        0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,
        37,38,39,40,41,42,43,44,45,46,47,
        81,82,83,84,85,86,87,88,89,90,91,92,
        135,136,137,138,139,140,141,142,143,144,
        145,146,147,148,149,150,151,152,153
    ]
    center_lane = [
        0,1,2,5,15,16,17,18,31,32,33,34,35,36,
        48,49,50,51,52,53,54,55,56,57,58,59,60,
        61,62,63,64,65,66,67,68,69,70,71,72,
        77,78,79,80,93,94,95,96,97,98,99,100,
        101,102,103,104,105,106,107,108,109,110,
        111,112,113,114,132,133,134,153
    ]
    right_lane = [
        19,20,21,22,23,24,25,26,27,28,29,30,
        73,74,75,76,115,116,117,118,119,120,
        121,122,123,124,125,126,127,128,129,
        130,131
    ]

    # 3) 기본 보상
    reward = 21.0

    # 4) 트랙 이탈 페널티 / 온트랙 보너스
    if params["all_wheels_on_track"]:
        reward += 10
    else:
        reward -= 10

    # 5) 다음 웨이포인트 인덱스에 따른 위치 보상
    next_wp = params["closest_waypoints"][1]
    if next_wp in left_lane and params["is_left_of_center"]:
        reward += 10
    elif next_wp in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif next_wp in center_lane and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10

    # 6) 속도 보정
    SPEED_THRESHOLD_1 = 1.3
    SPEED_THRESHOLD_2 = 3.2
    speed = params["speed"]
    if reward > 0:
        if speed < SPEED_THRESHOLD_1:
            reward *= 0.6
        elif speed <= SPEED_THRESHOLD_2:
            factor = (speed - SPEED_THRESHOLD_1) / (SPEED_THRESHOLD_2 - SPEED_THRESHOLD_1)
            reward *= (0.6 + 0.4 * factor)

    # 7) 과도한 조향 페널티
    ABS_STEERING_THRESHOLD = 5
    if abs(params["steering_angle"]) > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
