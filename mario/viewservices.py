import re


CODE_TEXTS = {
    '0': 'Small Mario ：',
    '1': 'Big Mario ：',
    '2': 'Fire Mario ：',
    '3': 'Fish ：',
    '4': 'Nokonoko ：',
    '5': 'Kuribo ：',
    '6': 'Hatena Block ：',
    '7': 'Kinoko ：',
    '8': 'Pipe ：',
    '9': 'P Flower ：',
    '10': 'Togezo ：',
    '11': 'Star ：',
    '12': 'Hummer Bros ：',
    '13': 'Hummer ：',
    '14': 'Blooper ：',
    '15': 'Kuppa ：',
    '16': 'Killer ：',
    '17': 'Patapata ：',
    '18': 'Met ：',
    '19': 'Scaffold Normal ：',
    '20': 'Scaffold Sky ：',
    '21': 'Scaffold Kuppa ：',
    '22': 'Fire Ball ：',
    '23': 'Fire Stick ：',
    '24': 'Fire Kuppa ：',
    '25': 'Lava ：',
    '26': 'Elevator ：',
    '27': 'Kuppa Hummer ：',
}

TESTARRAY = {
    'Small Mario ：','Big Mario ：','Fire Mario ：'
}

def process_game_info(game_info, current_time):
    mario_state = None
    hatena_block_time = None
    collision_message = "問題はなし"
    elements = []  # マリオ以外の要素を格納するリスト

    # マリオの状態を特定し、他の要素をelementsに格納
    for element in game_info:

        # elementが辞書であることを確認
        if not isinstance(element, dict):
            continue  # elementが辞書でない場合はスキップ
        
        # `code` を取得して、末尾のスペースやコロンを取り除く
        code = str(element.get('code')).strip()  # strip()で前後のスペースや全角コロンを削除

        # マリオの状態が設定されていない場合、または他の要素と重なっていない場合にチェック
        if mario_state is None or element != mario_state:
            # Marioの状態を判定
            code = str(element.get('code'))
            if 'Small Mario ：' in code:
                mario_state = {'state': 'Small Mario', 'x': element['x'], 'y': element['y'], 'width': element['width'], 'height': element['height']}  # Marioの状態を設定
            elif 'Big Mario ：' in code:
                mario_state = {'state': 'Big Mario', 'x': element['x'], 'y': element['y'], 'width': element['width'], 'height': element['height']}  # Big Marioに設定
            elif 'Fire Mario ：' in code:
                mario_state = {'state': 'Fire Mario', 'x': element['x'], 'y': element['y'], 'width': element['width'], 'height': element['height']}  # Fire Marioに設定

        # ハテナブロックがあった場合、ハテナブロックのタイムスタンプを記録
        if 'Hatena Block' in CODE_TEXTS.get(str(element.get('code')), ''):
            hatena_block_time = element.get('timestamp')  # ハテナブロックの時間を記録
            
            
    # マリオの状態が設定されていない場合はエラーメッセージを返す
    if mario_state is None:
        return "マリオの状態が設定されていません。"

    # マリオの状態を元に衝突判定
    for element in elements:
        label = CODE_TEXTS.get(element['code'], '')

        # 衝突判定の条件
        if (
            mario_state['x'] < element['x'] + element['width'] and
            mario_state['x'] + mario_state['width'] > element['x'] and
            mario_state['y'] < element['y'] + element['height'] and
            mario_state['y'] + mario_state['height'] > element['y']
        ):
            # 衝突メッセージの設定
            if 'Kuribo' in label:
                collision_message = (
                    "クリボーにぶつかって死亡しました！\n"
                    "ゲームオーバーになったので、5秒前に戻って再挑戦してください。\n"
                    "クリボーはジャンプで避けるか、踏みつけて倒せます。"
                )
            elif 'Hummer Bros' in label:
                collision_message = (
                    "ハンマーブロスのハンマーに当たって死亡しました！\n"
                    "ハンマーを避けるためにはタイミングよくジャンプし、または下をくぐって回避できます。\n"
                    "5秒前に戻って、もう一度挑戦してみてください。"
                )
            elif 'Fire Ball' in label:
                collision_message = (
                    "ファイアボールに当たって死亡しました！\n"
                    "ファイアボールはジャンプで避けることができます。ジャンプのタイミングを調整して再挑戦してください。\n"
                    "5秒前に戻って、もう一度チャレンジ！"
                )
            elif 'P Flower' in label:
                collision_message = (
                    "パックンフラワーに近づきすぎて死亡しました！\n"
                    "パックンフラワーは出てくるタイミングを見計らって、注意深く進んでください。\n"
                    "5秒前に戻り、パックンフラワーの攻撃を避けながら進んでみましょう。"
                )
            elif 'Kuppa' in label:
                collision_message = (
                    "クッパに倒されました！\n"
                    "クッパの攻撃を避けるためには、ジャンプで火の玉を避けつつ、クッパの動きを見極めて進むことが重要です。\n"
                    "クッパ戦ではタイミングと位置取りがカギです。5秒前に戻って挑戦しましょう。"
                )
            elif hatena_block_time is not None and current_time - hatena_block_time <= 10:
                if 'Big Mario' not in mario_state['code'] and 'Fire Mario' not in mario_state['code']:
                    collision_message = (
                        "ハテナブロックに触れると、ファイヤーマリオになれます！\n"
                        "10秒以内にブロックを取ることでファイヤーマリオに変身し、強力な攻撃を使えます。\n"
                        "10秒前に戻って、ブロックを取りに行きましょう！"
                    )
            elif 'Met' in label:
                collision_message = (
                    "メットにぶつかって死亡しました！\n"
                    "メットはジャンプで踏みつけることができます。\n"
                    "タイミングを見てジャンプし、メットを倒して進んでください。\n"
                    "5秒前に戻って、もう一度チャレンジ！"
                )
            elif 'Togezo' in label:
                collision_message = (
                    "トゲゾーにぶつかって死亡しました！\n"
                    "トゲゾーは動いている場合が多いので、上手にタイミングを見計らって避けましょう。\n"
                    "トゲゾーが地面や天井から降りてきたときに進むか、ジャンプして避けることが必要です。\n"
                    "5秒前に戻って、もう一度チャレンジ！"
                )
            break  # 衝突を検出したらループを終了

    return collision_message
