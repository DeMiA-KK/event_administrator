from tokenize import group

from django.db import IntegrityError
from .models import (
    Member,
    Team,
    Wallet,
    Star,
    Product,
    Purchase,
    Transaction,
    Answer,
    Quiz,
    QuizOption,
    FinishedQuiz,
)

# チーム数の算出
def culc_team_num(job):
    # チーム数初期化
    team_num = 0
    people_per_team = 0
    # プレイヤー全体の数
    players = Member.objects.filter(is_present=True, is_late=False, job=job, group=None)
    players_num = players.count()
    # 雇用中(リーダー候補)の数
    mentors = Member.objects.filter(
        is_present=True, is_late=False, job=job, is_employee=True, group=None
    )
    mentors_num = mentors.count()

    team_dict = {
        "job": job,
        "team_num": team_num,
        "people_per_team": people_per_team,
        "players": players,
        "mentors": mentors,
    }

    if players_num <= 0 or mentors_num <= 0:
        return team_dict
    # 　比率の整数除算
    ratio_int = players_num // mentors_num

    if ratio_int >= 4:
        # メンターにつき人数が多すぎる時→どうしようもないのでそのまま
        # メンターにつき人数がちょうどよかった(4,5人)の時→そのまま
        people_per_team = ratio_int
        team_dict["team_num"] = mentors_num
        team_dict["people_per_team"] = people_per_team
    elif ratio_int <= 3:
        # 1メンターにつき人数が少なすぎる時
        new_ratio_int = ratio_int
        while new_ratio_int < 4:
            # メンター数が1の時は0除算になる
            if mentors_num >= 2:
                mentors_num -= 1
                new_ratio_int = players_num // mentors_num
            else:
                # 極端に数が少ない時→合計が3以下の時
                if mentors_num == 1 and new_ratio_int <= 3:
                    team_dict["team_num"] = 1
                    team_dict["people_per_team"] = new_ratio_int
                break

        people_per_team = new_ratio_int
        team_dict["team_num"] = mentors_num
        team_dict["people_per_team"] = people_per_team

    return team_dict


# offsetとlimitの話ややこしい
def create_team(team_dict):
    all_players = team_dict["players"].order_by("?")
    mentors = team_dict["mentors"].order_by("?")
    team_num = team_dict["team_num"]
    people_per_team = team_dict["people_per_team"]
    print("チーム数", team_num)
    print("１チームの人数", people_per_team)
    # 不正な値の場合は弾く
    if team_num == 0 or people_per_team == 0:
        return None
    # チーム数だけメンターを取得
    leaders = mentors[:team_num]
    print("リーダーは", leaders)
    normal_mentors = None if team_num == mentors.count() else mentors[: team_num : mentors.count()]
    print("非リーダー", normal_mentors)
    if normal_mentors:
        for normal_mentor in normal_mentors:
            # リーダーじゃない人間は雇用フラグを折る
            normal_mentor.is_employee = False
            normal_mentor.save()
    # チーム作成とリーダー自身に登録
    for leader in leaders:
        try:
            team = Team.objects.create(leader=leader, score=0)
            leader.group = team
            leader.save()
        except IntegrityError:
            # 作るの二回目の場合はpass
            continue
    # チームが入ってないものだけ取り出す。
    teams = Team.objects.filter(leader__job=team_dict["job"])
    normal_players = all_players.filter(group=None)
    print("チームなし人間", normal_players, normal_players.count())
    for i, team in enumerate(teams):
        members_num = people_per_team - 1
        print("現状の無所属人数", normal_players.count())
        if members_num <= normal_players.count():
            team_members = normal_players[:members_num]
            print(i, team_members)
        else:
            team_members = normal_players[: normal_players.count()]
            print("else", i, team_members)
        for team_member in team_members:
            team_member.group = team
            team_member.save()

    return normal_players
