import chess.pgn
import chess
import typing

class TransformNotPossibleException(Exception):
    pass

def get_moves(game: chess.pgn.Game) -> typing.List[chess.Move]:
    out = []
    node = game.game()
    while not node.is_end():
        node = node.next()
        out.append(node.move)
    return out

def mirror_moves(moves: typing.List[chess.Move]) -> typing.List[chess.Move]:
    out = []
    for move in moves:
        n = chess.Move(
            chess.square_mirror(move.from_square), 
            chess.square_mirror(move.to_square),
            move.promotion,
            move.drop)
        out.append(n)
    return out

def hflip_square(square: chess.Square) -> chess.Square:
    rank = square//8
    file = square%8
    return rank*8+(7-file)

def get_hflipped_moves(game: chess.pgn.Game) -> typing.List[chess.Move]:
    out = []
    node = game.game()
    while not node.is_end():
        last_node = node
        node = node.next()
        move = node.move
        if last_node.board().is_castling(move):
            raise TransformNotPossibleException
        n = chess.Move(
            hflip_square(move.from_square),
            hflip_square(move.to_square),
            move.promotion,
            move.drop)
        out.append(n)
    return out

COMMON_HEADERS = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]

def make_new_headers(game: chess.pgn.Game) -> typing.Dict:
    headers = game.headers
    new_headers = {}
    for h in COMMON_HEADERS:
        new_headers[h] = headers[h]
    if "PlyCount" in headers:
        new_headers["PlyCount"] = headers["PlyCount"]
    return new_headers

def mirror_game(game: chess.pgn.Game) -> chess.pgn.Game:
    new_headers = make_new_headers(game)
    board = game.board()
    new_board = board.mirror()
    new_moves = mirror_moves(get_moves(game))
    [new_board.push(new_move) for new_move in new_moves]
    new_game = chess.pgn.Game.from_board(new_board)
    new_game.headers.update(new_headers)
    return new_game

def hflip_game(game: chess.pgn.Game) -> chess.pgn.Game:
    new_headers = make_new_headers(game)
    board = game.board()        
    new_board = board.transform(chess.flip_horizontal)
    new_moves = get_hflipped_moves(game)
    [new_board.push(new_move) for new_move in new_moves]
    new_game = chess.pgn.Game.from_board(new_board)
    new_game.headers.update(new_headers)
    return new_game

def vflip_game(game: chess.pgn.Game) -> chess.pgn.Game:
    new_headers = make_new_headers(game)
    board = game.board()
    if board.pawns > 0:
        raise TransformNotPossibleException
    new_board = board.transform(chess.flip_vertical)
    new_moves = mirror_moves(get_moves(game))
    [new_board.push(new_move) for new_move in new_moves]
    new_game = chess.pgn.Game.from_board(new_board)
    new_game.headers.update(new_headers)
    return new_game

rotate_game = lambda x:hflip_game(vflip_game(x))

IN_FOLDER = "in"
OUT_FOLDER = "out"

if __name__ == "__main__":
    from pathlib import Path
    import argparse
    parser = argparse.ArgumentParser(description="Creates mirrored/flipped versions of a chessboards in in/ and outputs them to out/")
    parser.add_argument('-m', action="store_true", help="Mirror the board")
    parser.add_argument('-v', action="store_true", help="Flip the board vertically (top becomes bottom)")
    parser.add_argument('-z', action="store_true", help="Flip the board horizontally (left becomes right)")
    parser.add_argument('-r', action="store_true", help="Rotate the board 180 degrees")
    args = parser.parse_args()

    do_mirrors = args.m
    do_hflip = args.z
    do_vflip = args.v
    do_rotation = args.r

    pathlist = Path(IN_FOLDER).glob('*.pgn')
    
    for in_path in pathlist:
        in_path = str(in_path)
        print(f"Processing file \"{in_path}\"")
        with open(in_path, "r", encoding="utf-8-sig") as in_file:
            base_path = OUT_FOLDER+in_path.removeprefix(IN_FOLDER).removesuffix(".pgn")
            transforms = [] # List of files and transforms to be applied

            # Make a transform for each desired transform
            if do_mirrors:
                mirrored_path = base_path+"_mirrored.pgn"
                mirror_file = open(mirrored_path, "w")
                transforms.append((mirror_file, mirror_game))
            if do_hflip:
                hflip_path = base_path+"_hflipped.pgn"
                hflip_file = open(hflip_path, "w")
                transforms.append((hflip_file, hflip_game))
            if do_vflip:
                vflip_path = base_path+"_vflipped.pgn"
                vflip_file = open(vflip_path, "w")
                transforms.append((vflip_file, vflip_game))
            if do_rotation:
                rotation_path = base_path+"_rotated.pgn"
                rotation_file = open(rotation_path, "w")
                transforms.append((rotation_file, rotate_game))

            # Parse our games
            while True:
                game = chess.pgn.read_game(in_file)
                if game is None:
                    break

                # Generate all the mirrored/flipped versions we want
                for (out_file, function) in transforms:
                    try:
                        print(function(game), file=out_file, end="\n\n")
                    except TransformNotPossibleException:
                        pass
                
            # Close out our files
            for (file, _) in transforms:
                file.close()
            print("Done")