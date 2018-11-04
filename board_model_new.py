# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:10:23 2018

@author: bleat
"""
from helper import *
from pieces import *
from copy import *

        
#Initialise pieces
def pieceGenerator(pieceCode,i,j):
    info_list=pieceCode.split('_')
    if info_list[0]=='pawn':
        return Pawn(i,j,info_list[1])
    if info_list[0]=='knight':
        return Knight(i,j,info_list[1])
    if info_list[0]=='rook':
        return Rook(i,j,info_list[1])
    if info_list[0]=='bishop':
        return Bishop(i,j,info_list[1])
    if info_list[0]=='queen':
        return Queen(i,j,info_list[1])
    if info_list[0]=='king':
        return King(i,j,info_list[1])
    if info_list[0]=='none':
        return NonePiece(i,j,'none')
        

class Field():
    def __init__(self,i,j,piece):
        self.i=i
        self.j=j
        self.piece=piece
        self.pieceCode=piece.getPieceCode()
        
    def getPieceCode(self):
        return self.pieceCode
    
    def setPieceCode(self,newpieceCode):
        self.pieceCode=newpieceCode
        


        
    
        

class Chessboard():
    def __init__(self):
        my_board=[]
        for i in range(8):
            my_row=[]
            for j in range(8):
                pieceCode=InitialPosition(i,j)
                field=Field(i,j,pieceGenerator(pieceCode,i,j))
                my_row.append(field)
            my_board.append(my_row)
            
        self.board=my_board
        self.highlightedfield=(8,8)#field that isnt in board
        self.previous_boards=[my_board]
        self.player_turn='white'
        self.game_status='Game in progress...'
        
    def updateGameStatus(self,colour):
        if not self.anyMovesPossible(colour):
            if self.kingInCheck(colour):
                self.game_status=oppositeColour(colour)+' wins!'
                return True
            else:
                self.game_status='Stalemate.'
                return True
        if self.drawByInsufficientMaterial():
            self.game_status='Draw by insufficient material'
            return True
        if self.repetitions():
            self.game_status='3 repetitions reached. You may claim a draw now.'
            return True
        return False
    
        
    def getBoard(self):
        return self.board
    
    def getPlayerTurn(self):
        return self.player_turn
    
    def setPlayerTurn(self,player_colour):
        self.player_turn=player_colour
        
    def computeCheckboard(self,board,player_colour):
        #Creates a list of lists which indicates whether a coordinate in the chessboard is under attack by opponent's pieces
        checkboard=[[False for i in range(8)] for j in range(8)]
        for x in board:
            for y in x:
                if y.piece.colour!=player_colour and y.piece.colour!='none':
                    for z in y.piece.attackRange(board):
                        checkboard[z[0]][z[1]]=True
        return checkboard
    
    def kingInCheck(self,colour):
        #checks if that colour king is in check
        king_position=self.findKing(self.board,colour)
        checkboard=self.computeCheckboard(self.board,colour)
        return checkboard[king_position[0]][king_position[1]]
    
        
                
    def hasPiece(self,i,j):
        if i in range(8) and j in range(8):
            return self.board[i][j].getPieceCode()
        else:
            print('please select starting field')
            return 'none_white'
        
    def movePiece(self,i1,j1,i2,j2,old_board,player_colour):
    
        new_board = deepcopy(old_board)
        movedPiece = new_board[i1][j1].piece        
        #variables needed for castling
        with_piece = "No piece yet"
        castle_fail = False
        castling_happening = False
        if(movedPiece.name == "king"):
            #check whether selected move is castling and whether it is viable
            old_check_board = self.computeCheckboard(new_board,player_colour)
            if(movedPiece.movesMade == 0):
                if((j2-j1) == 2):
                    with_piece = new_board[i2][7].piece
                    castle_fail = not movedPiece.canCastle(new_board,old_check_board,with_piece)
                    castling_happening = True
                if((j2-j1) == -2):
                    with_piece = new_board[i2][0].piece
                    castle_fail = not movedPiece.canCastle(new_board,old_check_board,with_piece)
                    castling_happening = True
        
        none_piece = pieceGenerator("none",i1,j1)
        curr_field = Field(i1,j1,none_piece)
        movedPiece.move(i2,j2)
        
        infoList = movedPiece.pieceCode.split("_")
        if(infoList[0] == "pawn"):
            movedPiece.updatePreviousPosition(i1,j1)
            if (infoList[1] == "white" and i2 == 0):
                #transform white pawn
                movedPiece = pieceGenerator("queen_white",i2,j2)
            if (infoList[1] == "black" and i2 == 7):
                #transform black pawn
                movedPiece = pieceGenerator("queen_black",i2,j2)
            
        
        new_field = Field(i2,j2,movedPiece)
        new_board[i1][j1] = curr_field
        new_board[i2][j2] = new_field
        
        en_passant = False
        passant_fail = False
        pieceThere = old_board[i2][j2].piece.getPieceCode()
        if ((infoList[0] == "pawn") and (pieceThere=="none")):
            if(movedPiece.colour == "white"):
                adjustment = 1
            elif(movedPiece.colour == "black"):
                adjustment = -1
            #check if move diagonal
            if (j1 != j2):
                #check if move just happened
                if(isInChessBoard((i2+adjustment,j2)) and len(chessboard.previous_boards) > 1):
                    pieceBefore = chessboard.previous_boards[-2][i2+adjustment][j2].piece.getPieceCode()
                    if(pieceBefore == "none"):
                        en_passant = True 
                        #A diagonal move to empty space can only be en_passant, 
                        #and the other pawn must've just have made that move
                    else:
                        #This move should not have been valid in the first place
                        passant_fail = True

        if (en_passant):
            new_none_piece = pieceGenerator("none",i2+adjustment,j2)
            new_noneField = Field(i2+adjustment,j2,new_none_piece)
            new_board[i2+adjustment][j2] = new_noneField
        
        
            
        if(not castle_fail and castling_happening):
            #move rook too
            none_piece = pieceGenerator("none",with_piece.i,with_piece.j)
            none_field = Field(with_piece.i,with_piece.j,none_piece)
            
            average = int((j2+j1)/2)
            
            old_rook_coords = (with_piece.i,with_piece.j)
            with_piece.move(with_piece.i,average)
            
            new_rook_field = Field(with_piece.i,average,with_piece)
        
            new_board[old_rook_coords[0]][old_rook_coords[1]] = none_field
            new_board[with_piece.i][average] = new_rook_field
            
            
        if (self.boardValid(new_board,i1,j1,i2,j2,player_colour,passant_fail,castle_fail)):
            return new_board
        else:
            return old_board


    def boardValid(self,nominated_board,i1,j1,i2,j2,player_colour,en_passant_fail,castle_fail):
        if en_passant_fail or castle_fail:
            return False
        #check if move is within piece's range
        old_board=self.previous_boards[-1]
        if (i2,j2) not in old_board[i1][j1].piece.computeRange(old_board):
            return False
        #check if move puts own king in check
        checkboard=self.computeCheckboard(nominated_board,player_colour)
        (king_i,king_j)=self.findKing(nominated_board,player_colour)
        if checkboard[king_i][king_j]==True:
            return False
        
        return True
    
    def updateBoard(self,new_board,player_colour):
        if self.board!=new_board:
            self.previous_boards.append(new_board)
            self.board=new_board
            self.setPlayerTurn(oppositeColour(player_colour))
            
    
        
    def findKing(self,board,player_colour):
        for x in board:
            for y in x:
                infolist=y.piece.pieceCode.split('_')
                if infolist[0]=='king'and infolist[1]==player_colour:
                    return (y.i,y.j)
        
       
    def boardsEqual(self,board1,board2):
        for i in range(8):
            for j in range(8):
                if board1[i][j].getPieceCode()!=board2[i][j].getPieceCode():
                    return False
        return True

    def kingMoves(self,board,colour):
        #used for highlighting king's possible moves
        king_position=self.findKing(board,colour)
        king=board[king_position[0]][king_position[1]].piece
        steps=[]
        for destination in king.attackRange(board):
            new_board=self.movePiece(king_position[0],king_position[1],destination[0],destination[1],board,colour)
            if self.boardsEqual(board,new_board)==False:
                steps.append(destination)
        for destination in king.castleRange():
            new_board=self.movePiece(king_position[0],king_position[1],destination[0],destination[1],board,colour)
            if self.boardsEqual(board,new_board)==False:
                steps.append(destination)
        return steps
    
    def pieceMoves(self,i,j,board):
        #used for highlighting possible moves
        piece=board[i][j].piece
        i=piece.i
        j=piece.j
        moves=[]
        for destination in piece.computeRange(board):
            new_board=self.movePiece(i,j,destination[0],destination[1],board,piece.colour)
            if not self.boardsEqual(board,new_board):
                moves.append(destination)
        return moves
    
    def pawnMoves(self,pawn,board):
        #used for highlighting pawn's possible
        i=pawn.i
        j=pawn.j
        moves=[]
        for destination in pawn.pawnRange():
            new_board=self.movePiece(i,j,destination[0],destination[1],board,pawn.colour)
            if self.boardsEqual(board,new_board)==False:
                moves.append(destination)
                
        return moves
    
    
    def possibleMoves(self,i,j):
        #used for highlighting possible moves
        piece=self.board[i][j].piece
        board=self.board
        if piece.pieceCode=='none':
            return []
        if piece.name=='pawn':
            return self.pawnMoves(piece,board)
        elif piece.name=='king':
            return self.kingMoves(board,piece.colour)
        else:
            return self.pieceMoves(i,j,board)
    
    def allPossibleMoves(self,colour):
        all_moves=[]
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece.colour==colour:
                    all_moves+=self.possibleMoves(i,j)
                    
        return all_moves
    
    def anyMovesPossible(self,colour):
        #used for checking stalemates
        return self.allPossibleMoves(colour)!=[]
    
    def repetitions(self):
        #check if 3 repetitions of the board have occurred
        repetitors=0
        board_count=len(self.previous_boards)
        if board_count>3:
            for i in range(board_count-1):
                if self.boardsEqual(self.previous_boards[-i-2],self.board):
                    repetitors=repetitors+1
                if repetitors>=2:
                    return True
        return False
    
    def drawByInsufficientMaterial(self):
        pieces=[]
        for i in range(8):
            for x in self.board[i]:
                if x.piece.getPieceCode()!='none':
                    pieces.append(x.piece)
            if len(pieces)>5:
                return False
        for piece in pieces:
            if piece.name=='queen' or piece.name=='rook' or piece.name=='pawn':
                return False
        if len(pieces)<=3:
            return True
        for piece in pieces:
            if piece.name=='king':
                pieces.remove(piece)
        black_pieces=[]
        white_pieces=[]
        for piece in pieces:
            if piece.colour=='black':
                black_pieces.append(piece)
            else:
                white_pieces.append(piece)
        if len(black_pieces)>2 or len(white_pieces)>2:
            return False
        
        #black has two knights, white has no pieces
        if white_pieces==[]:
            for piece in black_pieces:
                if piece.name!='knight':
                    return False
            return True
        
        #white has two knights, black has no pieces
        if black_pieces==[]:
            for piece in white_pieces:
                if piece.name!='knight':
                    return False
            return True
        return False
        
                
            
                
        
        
            
        
    def getHighlightedField(self):
        return self.highlightedfield
    
    def setHighlightedField(self,field):
        if isInChessBoard(field):
            if self.hasPiece(field[0],field[1])!='none':
                self.highlightedfield=field
        
        
chessboard=Chessboard()