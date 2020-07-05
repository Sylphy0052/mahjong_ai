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


def function(combination_tiles, tile_pair):
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
    return shanten, other_combination


def calc_shanten_recursive(combination_tiles):
    best_shanten1, best_combs1 = 0, []
    for tile_pair1 in combination_tiles:
        shanten1, other_combination1 = function(combination_tiles, tile_pair1)
        best_shanten2, best_combs2 = 0, []
        for tile_pair2 in other_combination1:
            shanten2, other_combination2 = function(
                other_combination1, tile_pair2)
            print(other_combination2)
            if best_shanten2 < shanten2:
                best_shanten2 = shanten2
                best_combs2.append(tile_pair2)
        shanten1 += best_shanten2
        if best_shanten1 < shanten1:
            best_shanten1 = shanten1
            best_combs1 = copy(best_combs2)
            best_combs1.append(tile_pair1)

    return best_shanten1, best_combs1


def calc_shanten_by_type(combination_tiles):
    shanten, tiles = calc_shanten_recursive(combination_tiles)
    print(shanten, tiles)
    return shanten, tiles


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

    for combination in [manzu_combination, souzu_combination, pinzu_combination, jihai_combination]:
        print('-----')
        print('A')
        print(combination)
        shanten, tiles = calc_shanten_by_type(combination)
        print('-----')

    return best_shanten


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

    shanten = calc_shanten(combination_tiles)
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
    # print(shanten)
