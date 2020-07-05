from copy import deepcopy as copy
from status.tile_type import TileType

KOKUSHI = ['1m', '9m', '1s', '9s', '1p',
           '9p', '東', '南', '西', '北', '白', '発', '中']


def get_target_tiles(tiles, target):
    ret = []
    for tile in tiles:
        if tile.char == target:
            ret.append(tile)
    return ret


def get_target_tiles_with_num(tiles, num):
    return [t for t in tiles if t.num == num]


def judge_kokushi(tehai):
    """国士無双までのシャンテン数を求める

    Args:
        tehai ([tile.tile.Tile]): 手牌

    Returns:
        int: シャンテン数
    """
    has_janto = False
    tehai_tmp = copy(tehai)
    tehai_char = [tile.char for tile in tehai]
    for tile in KOKUSHI:
        if tile in tehai_char:
            tiles = get_target_tiles(tehai_tmp, tile)
            if not has_janto and len(tiles) > 1:
                has_janto = True
                tehai_tmp.remove(tiles[1])
            tehai_tmp.remove(tiles[0])
    return len(tehai_tmp) - 1


def judge_chitoi(tehai):
    """七対子のシャンテン数を求める

    Args:
        tehai ([tile.tile.Tile]): 手牌

    Returns:
        int: シャンテン数
    """
    tehai_tmp = sorted(tehai, key=lambda t: t.idx)
    tehai_char = [tile.char for tile in tehai_tmp]
    janto_num = 0
    for tile in set(tehai_char):
        tiles = get_target_tiles(tehai_tmp, tile)
        if len(tiles) > 1:
            tehai_tmp.remove(tiles[0])
            tehai_tmp.remove(tiles[1])
            janto_num += 1
    return 6 - janto_num


def judge_kotsu(tiles_, tile):
    ret = []
    flg = False
    tiles = [t for t in tiles_ if t.num == tile.num]
    if len(tiles) > 1:
        flg = True
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                comb = [tile, tiles[i], tiles[j]]
                ret.append(comb)
    return flg, ret


def judge_shuntsu(tiles_, tile):
    flg = False
    ret = []
    tiles = [t for t in tiles_]
    if len(tiles) >= 2:
        tiles_p1 = get_target_tiles_with_num(tiles, tile.num + 1)
        tiles_p2 = get_target_tiles_with_num(tiles, tile.num + 2)
        if len(tiles_p1) > 0 and len(tiles_p2) > 0:
            flg = True
            for p1 in tiles_p1:
                for p2 in tiles_p2:
                    ret.append([tile, p1, p2])
    return flg, ret


def judge_toitsu(tiles_, tile):
    ret = []
    flg = False
    tiles = [t for t in tiles_ if t.num == tile.num]
    if len(tiles) > 0:
        flg = True
        for i in range(len(tiles)):
            comb = [tile, tiles[i]]
            ret.append(comb)
    return flg, ret


def judge_tatsu(tiles_, tile):
    flg = False
    ret = []
    tiles = [t for t in tiles_]
    if len(tiles) >= 1:
        flg = True
        tiles_p1 = get_target_tiles_with_num(tiles, tile.num + 1)
        tiles_p2 = get_target_tiles_with_num(tiles, tile.num + 2)
        for tiles in [tiles_p1, tiles_p2]:
            for t in tiles:
                ret.append([tile, t])
    return flg, ret


def sort_combination(combination_tiles):
    ret = []
    toitsu = []
    kotsu = []
    shuntsu = []
    tatsu = []
    # 対子 > 刻子 > 順子 > 塔子の順にする
    for comb in combination_tiles:
        if len(comb) == 3:
            if comb[0].num == comb[1].num:
                kotsu.append(comb)
            else:
                shuntsu.append(comb)
        elif len(comb) == 2:
            if comb[0].num == comb[1].num:
                toitsu.append(comb)
            else:
                tatsu.append(comb)
    ret.extend(toitsu)
    ret.extend(kotsu)
    ret.extend(shuntsu)
    ret.extend(tatsu)
    return ret


def calc_shanten_recursive(tile_pair, combination_tiles):
    best_shanten, best_combs = 0, []
    if len(combination_tiles) == 0:
        return 0, []
    if len(combination_tiles) == 1:
        tiles = combination_tiles[0]
        best_shanten = 2 if len(tiles) == 3 else 1
        tiles = [tiles]
        return best_shanten, tiles
    for tile_pair in combination_tiles:
        other_combination = []
        if len(tile_pair) == 2:
            tile1 = tile_pair[0]
            tile2 = tile_pair[1]
            shanten = 1
            for comb_ in combination_tiles:
                if tile1 not in comb_ and tile2 not in comb_:
                    other_combination.append(comb_)
        elif len(tile_pair) == 3:
            tile1 = tile_pair[0]
            tile2 = tile_pair[1]
            tile3 = tile_pair[2]
            shanten = 2
            for comb_ in combination_tiles:
                if tile1 not in comb_ and tile2 not in comb_ and tile3 not in comb_:
                    other_combination.append(comb_)
        if len(other_combination) == 0:
            return shanten, [tile_pair]
        other_combination = sort_combination(other_combination)
        for tile_pair2 in other_combination:
            best_shanten2, combs2 = calc_shanten_recursive(
                tile_pair2, other_combination)
        shanten += best_shanten2
        if best_shanten < shanten:
            best_shanten = shanten
            best_combs = copy(combs2)
            best_combs.append(tile_pair)
    return best_shanten, best_combs


def calc_shanten_by_type(combination_tiles):
    if len(combination_tiles) == 0:
        return 0, []
    if len(combination_tiles) == 1:
        tiles = combination_tiles[0]
        best_shanten = 2 if len(tiles) == 3 else 1
        return best_shanten, [tiles]
    combination_tiles = sort_combination(combination_tiles)
    for tile_pair in combination_tiles:
        shanten, combs = calc_shanten_recursive(tile_pair, combination_tiles)
    return shanten, combs


def calc_shanten(combination_tiles):
    best_shanten = 8
    manzu_combination = [
        ts for ts in combination_tiles if ts[0].tile_type is TileType.MANZU]
    souzu_combination = [
        ts for ts in combination_tiles if ts[0].tile_type is TileType.SOUZU]
    pinzu_combination = [
        ts for ts in combination_tiles if ts[0].tile_type is TileType.PINZU]
    jihai_combination = [
        ts for ts in combination_tiles if ts[0].tile_type is TileType.JIHAI]

    shanten_list = []
    tiles_list = []
    for combination in [manzu_combination, souzu_combination, pinzu_combination, jihai_combination]:
        shanten, tiles = calc_shanten_by_type(combination)
        shanten_list.append(shanten)
        tiles_list.append(tiles)

    block_num = 0
    mentsu_num = 0
    toitsu_num = 0
    for shanten, combs in zip(shanten_list, tiles_list):
        if len(combs) != 0:
            best_shanten -= shanten
            for comb in combs:
                block_num += 1
                if len(comb) == 3:
                    mentsu_num += 1
                elif len(comb) == 2:
                    if comb[0].num == comb[1].num:
                        toitsu_num += 1
    tatsu_num = block_num - mentsu_num - toitsu_num
    if block_num > 5:
        if toitsu_num == 0:
            best_shanten += 1
        while block_num > 5:
            if tatsu_num > 0:
                block_num -= 1
                tatsu_num -= 1
                best_shanten += 1
            else:
                if toitsu_num > 0:
                    block_num -= 1
                    toitsu_num -= 1
                    best_shanten += 1
                else:
                    block_num -= 1
                    mentsu_num -= 1
                    best_shanten += 2

    # print(tiles_list)
    # print('block {} mentsu {} toitsu {}'.format(
    #     block_num, mentsu_num, toitsu_num))
    # print('best shanten {}'.format(best_shanten))

    return best_shanten, tiles_list


def judge_tehai_shanten(tehai):
    # 理牌する
    tehai_tmp = sorted(tehai, key=lambda t: t.idx)
    # 萬子，筒子，索子,字牌で分ける
    manzu = [t for t in tehai_tmp if t.tile_type is TileType.MANZU]
    souzu = [t for t in tehai_tmp if t.tile_type is TileType.SOUZU]
    pinzu = [t for t in tehai_tmp if t.tile_type is TileType.PINZU]
    jihai = [t for t in tehai_tmp if t.tile_type is TileType.JIHAI]
    combination_tiles = []

    for tiles in([manzu, souzu, pinzu]):
        # 孤立牌を削除
        num_tiles = [t.num for t in tiles]
        remove_idx = []
        for i, tile in enumerate(tiles):
            num_tiles = [t.num for t in tiles if tile.idx != t.idx]
            nums = list(range(tile.num - 2, tile.num + 2 + 1))
            nums = [n for n in nums if n > 0 and n < 10]
            tmp = [t for t in num_tiles if t in nums]
            if len(tmp) == 0:
                remove_idx.append(i)
        for idx in reversed(remove_idx):
            del tiles[idx]
        # 組み合わせを考える
        for i, tile in enumerate(tiles):
            other_tehai = tiles[i + 1:]
            flg, tiles_ = judge_kotsu(other_tehai, tile)
            if flg:
                combination_tiles.extend(tiles_)
            flg, tiles_ = judge_shuntsu(other_tehai, tile)
            if flg:
                combination_tiles.extend(tiles_)
            flg, tiles_ = judge_tatsu(other_tehai, tile)
            if flg:
                combination_tiles.extend(tiles_)
            flg, tiles_ = judge_toitsu(other_tehai, tile)
            if flg:
                combination_tiles.extend(tiles_)

    # 孤立牌を削除
    tiles = jihai
    num_tiles = [t.num for t in tiles]
    remove_idx = []
    for i, tile in enumerate(tiles):
        num_tiles = [t.num for t in tiles if tile.idx != t.idx]
        tmp = [t for t in num_tiles if t == tile.num]
        if len(tmp) == 0:
            remove_idx.append(i)
    for idx in reversed(remove_idx):
        del tiles[idx]
    # 組み合わせを考える
    for i, tile in enumerate(tiles):
        other_tehai = tiles[i + 1:]
        flg, tiles_ = judge_kotsu(other_tehai, tile)
        if flg:
            combination_tiles.extend(tiles_)
        flg, tiles_ = judge_toitsu(other_tehai, tile)
        if flg:
            combination_tiles.extend(tiles_)

    shanten, comb_tiles = calc_shanten(combination_tiles)
    return shanten


def judge_yaku(tehai, misehai, doras, status):
    pass


def judge_shanten(tehai, misehai):
    print('-----')
    print(tehai)
    if len(misehai) == 0:
        kokushi_shanten = judge_kokushi(tehai)
        chitoi_shanten = judge_chitoi(tehai)
    shanten = judge_tehai_shanten(tehai)
    shanten = min(kokushi_shanten, chitoi_shanten, shanten)
    print(shanten)
    return shanten
