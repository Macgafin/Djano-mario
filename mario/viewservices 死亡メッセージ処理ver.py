import re
from time import time  # time()を使って現在時刻を取得する

CODE_TEXTS = {
    "0": "Small Mario ：",
    "1": "Big Mario ：",
    "2": "Fire Mario ：",
    "3": "Fish ：",
    "4": "Nokonoko ：",
    "5": "Kuribo ：",
    "6": "Hatena Block ：",
    "7": "Kinoko ：",
    "8": "Pipe ：",
    "9": "P Flower ：",
    "10": "Togezo ：",
    "11": "Star ：",
    "12": "Hummer Bros ：",
    "13": "Hummer ：",
    "14": "Blooper ：",
    "15": "Kuppa ：",
    "16": "Killer ：",
    "17": "Patapata ：",
    "18": "Met ：",
    "19": "Scaffold Normal ：",
    "20": "Scaffold Sky ：",
    "21": "Scaffold Kuppa ：",
    "22": "Fire Ball ：",
    "23": "Fire Stick ：",
    "24": "Fire Kuppa ：",
    "25": "Lava ：",
    "26": "Elevator ：",
    "27": "Kuppa Hummer ：",
}


# # 変数を追加：死亡時刻とメッセージの有効期間
# death_time = None  # 死亡時刻
# death_message = None  # 死亡時のメッセージ

# # 定義：死亡後に同じメッセージを送信する期間
# DEATH_MESSAGE_DURATION = 20  # 5秒間メッセージを繰り返す


def process_game_info(game_info, current_time):
    # global death_time, death_message  # グローバル変数を使用

    mario_state = None
    hatena_block_time = None
    elements = []  # マリオ以外の要素を格納するリスト
    environment = []  # ステージの環境を格納するリスト
    bros_y_coordinate = []  # ハンマーブロスの環境を格納するリスト
    mario_history = []  # マリオの位置履歴を格納
    collision_message = None
    # マリオの状態を特定し、他の要素をelementsに格納
    for element in game_info:   #間違えやすいが、ここのelementは格納されるelementsとは別のことである
        # マリオの状態を判定し、マリオの状態を設定
        if "Small Mario" in element["code"]:
            mario_state = {
                "state": "Small Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        elif "Big Mario" in element["code"]:
            mario_state = {
                "state": "Big Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        elif "Fire Mario" in element["code"]:
            mario_state = {
                "state": "Fire Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        else:
            # マリオ以外の要素は elements に追加
            elements.append(element)

        # # マリオの位置履歴を保存
        # if mario_state:
        #     mario_history.append(
        #         {
        #             "time": element.get("timestamp"),
        #             "x": mario_state["x"],
        #             "y": mario_state["y"],
        #         }
        #     )

        # ハテナブロックがあった場合、ハテナブロックのタイムスタンプを記録
        if "Hatena Block" in element["code"]:
            hatena_block_time = element.get("timestamp")  # ハテナブロックの時間を記録

        # 空中の足場の座礁を記録
        if "Scaffold Normal" in element["code"]:
            environment.append({"y": element["y"]})  # ステージの種類とy座標を追加

        # ハンマーブロスの座標を記録
        if "Hummer Bros" in element["code"]:
            bros_y_coordinate.append({"y": element["y"]})  # ステージの種類とy座標を追加

    # マリオの状態が設定されていない場合はエラーメッセージを返す
    if mario_state is None:
        no_mario = "巻き戻し中！"
    else:
        no_mario = ""
        
    print("--------------------------------")
    print(elements) #マリオ以外が格納されているはず

    # # 死亡2秒前のマリオの状態を取得
    # death_time = current_time - 2  # 死亡の2秒前の時刻
    # mario_state_before_death = mario_state
    # for history in reversed(mario_history):
    #     if history['time'] <= death_time:
    #         mario_state_before_death = history
    #         break

    # # mario_state_before_deathに有効な情報がある場合のみ、状態を更新
    # if isinstance(mario_state_before_death, dict) and 'state' in mario_state_before_death:
    #     mario_state = {'state': mario_state_before_death['state'],
    #                 'x': mario_state_before_death['x'],
    #                 'y': mario_state_before_death['y'],
    #                 'width': mario_state_before_death['width'],
    #                 'height': mario_state_before_death['height']}

    # マリオの状態を元に衝突判定
    collision_detected = False  # 衝突が検出されたかどうかのフラグ
    for element in elements:
        default_label = element["code"]
        label = [line.split("：")[0].strip() for line in default_label.splitlines()] #じゃまなものを消す
        

        # 衝突判定の条件 マリオ
        tolerance = 4  # 余裕を持たせる距離（ピクセル単位で調整）

        # マリオの矩形の左上隅と右下隅を計算
        mario_left = mario_state["x"] - mario_state["width"] / 2
        mario_right = mario_state["x"] + mario_state["width"] / 2
        mario_top = mario_state["y"] + mario_state["height"] / 2
        mario_bottom = mario_state["y"] - mario_state["height"] / 2

        # elementの矩形の左上隅と右下隅を計算
        element_left = element["x"] - element["width"] / 2
        element_right = element["x"] + element["width"] / 2
        element_top = element["y"] + element["height"] / 2
        element_bottom = element["y"] - element["height"] / 2
        print("++++++++++++++++++++++")
        print(elements) #上記のelementと一致するかどうか
        print("++++++++++++++++++++++")

        # print(f"マリオ状態　{mario_state['state']}　マリオ右　{mario_right}　)マリオ左　{mario_left} マリオ上　{mario_top}マリオした {element_bottom}")
        # print(f"element名　{element["code"]}　element右　{element_right}　element左　{element_left} element上　{element_top}　element下 {element_bottom}")

        if (
            abs(mario_state["y"] - element["y"]) <= tolerance  # y座標がほぼ同じ
            and (
                mario_right > element_left  # マリオの右端がelementの左端より右
                or mario_left < element_right
            )  # マリオの左端がelementの右端より左
        ) or (
            abs(mario_state["x"] - element["x"]) <= tolerance  # x座標がほぼ同じ
            and (
                mario_bottom > element_top  # マリオの下端がelementの上端より下
                or mario_top < element_bottom
            )  # マリオの上端がelementの下端より上
        ):
            collision_detected = True  # 衝突を検出

            collision_message = generate_collision_message(
                label=label,
                mario_state=mario_state,
                environment=environment,
                bros_y_coordinate=bros_y_coordinate,
                current_time=current_time,
                hatena_block_time=hatena_block_time,
                no_mario = no_mario
            )

        # # 衝突時にdeath_messageを設定し、death_timeを現在時刻にセット
        # death_message = collision_message
        # death_time = current_time  # 衝突した時点でdeath_timeを現在時刻にセット

    # 死亡後5秒間メッセージを送信
    # if death_time and current_time - death_time <= DEATH_MESSAGE_DURATION:
    #         collision_message = death_message
    
    print("-------------------------------------")
    return collision_message


def generate_collision_message(
    label, mario_state, environment, bros_y_coordinate, current_time, hatena_block_time, no_mario
):
    # 衝突メッセージ関数
    collision_message = no_mario

    # 衝突メッセージの設定
    if "Kuribo" in label:
        if "Fire Mario" in mario_state["state"]:
            collision_message = (
                "ファイヤーマリオでクリボーに当たって死亡しました！\n"
                "ファイヤーマリオなら、ファイアボールを使ってクリボーを倒すことができます。\n"
                "次は火を使って進むと良いでしょう。5秒前に戻って再挑戦してください！"
            )
        else:
            collision_message = (
                "クリボーにぶつかって死亡しました！\n"
                "さては落ちついていないですね…\n"
                "見なかったことにしますので、5秒前に戻って再挑戦しましょう！"
            )

    # ハンマーブロスにぶつかった場合
    elif "Hummer Bros" in label:
        if mario_state["y"] < bros_y_coordinate["y"]:  # マリオより上にブロスがいる時
            collision_message = (
                "ハンマーブロスのハンマーに当たって死亡しました！\n"
                "下に通り抜けるチャンスがあります。足元の足場を使って下をくぐったり\n"
                "また、上の足場を叩いて倒すことも可能です。5秒前に戻って再挑戦！"
            )
        else:
            collision_message = (
                "ハンマーブロスのハンマーに当たって死亡しました！\n"
                "ハンマーの動きを注意深く見て近づき、ジャンプするタイミングで通り抜けてみましょう\n"
                "踏みつけて倒すこともできますよ、再挑戦してみてください！"
            )

    # げっそー（Blooper）の動き
    elif "Blooper" in label:
        # ゲッソーの判定もできるようにしたかったのですけどね
        # if 'escape' in blooper_state:  # 逃げるタイプのげっそー
        #     collision_message = (
        #         "げっそーにやられました！\n"
        #         "逃げるタイプのげっそーは近づいても問題ありませんが、慎重に進んでください。\n"
        #         "足場があれば、冷静に進みましょう。5秒前に戻って再挑戦してください！"
        #     )
        # elif 'aggressive' in blooper_state:  # 近づいてくるタイプのげっそー
        #     collision_message = (
        #         "げっそーにやられました！\n"
        #         "近づいてくるタイプのげっそーには、逃げられなくなることが多いです。\n"
        #         "そのため、○○秒前に戻って安全な場所を探しながら進みましょう。"
        #     )
        # else:
        #     collision_message = (
        #         "げっそーにやられました！\n"
        #         "どちらのタイプか不明ですが、足場を活用して回避するのが重要です。\n"
        #         "5秒前に戻って、安全な場所を探しながら進んでみましょう。"
        #     )
        collision_message = (
            "げっそーにやられました！\n"
            "どちらのタイプか不明ですが、足場を活用して回避するのが重要です。\n"
            "5秒前に戻って、安全な場所を探しながら進んでみましょう。"
        )

    # パックンフラワーに近づきすぎた場合
    elif "P Flower" in label:
        if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオが有効な場合
            collision_message = (
                "パックンフラワーに近づきすぎて死亡しました！\n"
                "ファイヤーマリオなら、ファイアボールでパックンフラワーを倒せます。\n"
                "安全に進むために、5秒前に戻って再挑戦してみましょう。"
            )
        else:
            collision_message = (
                "パックンフラワーぶつかって死亡しました！\n"
                "パックンフラワーは出てくるタイミングを見計らって進む必要があります。\n"
                "土管の近くに立っていれば出てこなくなるので、一旦待ってみましょう。では5秒前に戻って慎重に進んでみましょう。"
            )

    # トゲゾーにぶつかった場合
    elif "Togezo" in label:
        if mario_state["y"] < environment["y"]:  # 空中に足場がある場合
            collision_message = (
                "トゲゾーにぶつかって死亡しました！\n"
                "トゲゾーが空から降りてきた場合、周りの足場を確認してみましょう。\n"
                "上に足場がある場合は、そこに一時避難してから進みましょう。5秒前に戻って再挑戦！"
            )
        else:  # 地面の足場がある場合
            collision_message = (
                "トゲゾーにぶつかって死亡しました！\n"
                "トゲゾーは、タイミングを見計らって避けることが大切です。\n"
                "周囲に穴があればうまいこと、そこに落として見ましょう。5秒前に戻って再挑戦！"
            )

    # エレベーターで死亡した場合
    elif "Elevator" in label:
        collision_message = (
            "エレベーターで死亡しました！\n"
            "エレベーターは不安定な足場なので、急がず落ち着いて移動しましょう。\n"
            "周りの足場を利用して、足元に気をつけて進んでください。5秒前に戻って再挑戦！"
        )

    # ノコノコに遭遇した場合
    elif "Nokonoko" in label:
        if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
            collision_message = (
                "ノコノコにぶつかって死亡しました！\n"
                "ファイヤーマリオなら、ノコノコを倒すためにファイアボールを使うことができます。\n"
                "5秒前に戻って、ファイアボールを使って進みましょう！"
            )
        else:
            collision_message = (
                "ノコノコにぶつかって死亡しました！\n"
                "ノコノコはジャンプで踏みつけて倒せます。\n"
                "また、甲羅を利用して遠くの敵を倒すことができます。5秒前に戻って再挑戦！"
            )

    # パタパタに遭遇した場合
    elif "Patapata" in label:
        if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
            collision_message = (
                "パタパタにぶつかって死亡しました！\n"
                "ファイヤーマリオなら、パタパタを倒すためにファイアボールを使うことができます。\n"
                "5秒前に戻って、ファイアボールを使って進みましょう！"
            )
        else:
            collision_message = (
                "パタパタにぶつかって死亡しました！\n"
                "パタパタは難しいですが、タイミングをよく見てジャンプで踏みつけて倒せます。\n"
                "また、その甲羅を利用して遠くの敵を倒すことができます。5秒前に戻って再挑戦！"
            )

    # パタパタに遭遇した場合
    elif "Met" in label:
        if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
            collision_message = (
                "パタパタにぶつかって死亡しました！\n"
                "メットはファイヤーマリオの火を防ぎます。\n"
                "倒す方法は踏みつけることです！動きが遅いので避けてみるのもいいかもしれません。５秒前に戻って再挑戦！"
            )
        else:
            collision_message = (
                "パタパタにぶつかって死亡しました！\n"
                "パタパタは難しいですが、タイミングをよく見てジャンプで踏みつけて倒せます。\n"
                "また、その甲羅を利用して遠くの敵を倒すことができます。5秒前に戻って再挑戦！"
            )

    # クッパにぶつかった場合
    elif "Kuppa" in label:
        if (
            "Fire Mario" in mario_state["state"] or "Big Mario" in mario_state["state"]
        ):  # ファイヤーマリオかつビッグマリオ
            if mario_state["y"] < environment["y"]:  # マリオのy座標が足場より高い場合
                collision_message = (
                    "クッパに倒されました！\n"
                    "足場などを使ってクッパの攻撃をかわすことができます。5秒前に戻って再挑戦しましょう！"
                )
            else:
                collision_message = (
                    "クッパに倒されました！\n"
                    "今の状態ならば、クッパにぶつかってみても一瞬無敵になれます。\n"
                    "5秒前に戻って再挑戦してみましょう！"
                )
        else:
            collision_message = (
                "クッパに倒されました！\n"
                "クッパの攻撃を避けるためには、タイミングを見計らってジャンプし、または周囲の足場を利用して攻撃をかわしましょう。\n"
                "5秒前に戻って慎重に進んでください！"
            )

    elif hatena_block_time is not None and current_time - hatena_block_time <= 10:
        if (
            "Big Mario" not in mario_state["code"]
            and "Fire Mario" not in mario_state["code"]
        ):
            collision_message += (
                "ちなみに10秒以内はてなブロックがありました、\n"
                "今の状態で叩いてフラワーが入っていればファイヤーマリオに変身して、火を出せます。\n"
            )
            
    return collision_message
