import math

def reward_function(params):
    """
    Index 기반 Reinvent-2018 트랙 보상 함수 (스케일 1.0 기준)
    • graded off-track penalty
    • straight-only steering penalty
    • cornering steering bonus
    • progress bonus + finish bonus
    """

    # 1) 기본 변수
    track_width      = params["track_width"]
    distance_center  = params["distance_from_center"]
    center_variance  = distance_center / track_width
    next_wp          = params["closest_waypoints"][1]
    speed            = params["speed"]
    steering         = params["steering_angle"]
    progress         = params.get("progress", 0)

    # 2) 레인 구역 인덱스
    left_lane   = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,
                   37,38,39,40,41,42,43,44,45,46,47,
                   81,82,83,84,85,86,87,88,89,90,91,92,
                   135,136,137,138,139,140,141,142,143,144,
                   145,146,147,148,149,150,151,152,153]
    center_lane = [0,1,2,5,15,16,17,18,31,32,33,34,35,36,
                   48,49,50,51,52,53,54,55,56,57,58,59,60,
                   61,62,63,64,65,66,67,68,69,70,71,72,
                   77,78,79,80,93,94,95,96,97,98,99,100,
                   101,102,103,104,105,106,107,108,109,110,
                   111,112,113,114,132,133,134,153]
    right_lane  = [19,20,21,22,23,24,25,26,27,28,29,30,
                   73,74,75,76,115,116,117,118,119,120,
                   121,122,123,124,125,126,127,128,129,
                   130,131]

    # 3) 베이스 리워드
    reward = 1.0

    # 4) Off-track graded penalty (no early exit)
    if not params["all_wheels_on_track"]:
        half_w = track_width / 2.0
        off_ratio = min(distance_center / half_w, 2.0)
        penalty = max(0.01, 1.0 - off_ratio * 0.9)
        reward *= penalty

    # 5) On-track bonus
    else:
        reward += 0.2

    # 6) Racing-line position bonus
    if next_wp in left_lane and params["is_left_of_center"]:
        reward += 0.2
    elif next_wp in right_lane and not params["is_left_of_center"]:
        reward += 0.2
    elif next_wp in center_lane and center_variance < 0.3:
        reward += 0.2
    else:
        reward -= 0.1

    # 7) Speed scaling (0.6 → 1.0)
    s1, s2 = 0.8, 2.5
    if speed < s1:
        reward *= 0.6
    elif speed <= s2:
        factor = (speed - s1) / (s2 - s1)
        reward *= (0.6 + 0.4 * factor)

    # 8) Steering penalty only on straights
    STEER_TH = 12
    if abs(steering) > STEER_TH and next_wp in center_lane:
        reward -= 0.1

    # 9) Cornering steering bonus
    if next_wp in right_lane and steering > 2:
        reward += 0.1
    if next_wp in left_lane and steering < -2:
        reward += 0.1

    # 10) Progress bonus & finish bonus
    reward += (progress / 100.0) * 0.1
    if progress >= 100:
        reward += 1.0

    return float(max(reward, 1e-3))
