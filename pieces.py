# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:17:26 2018

@author: bleat
"""

from helper import *

class Piece():
    def __init__(self, i, j,colour):
        self.pieceCode='none'
        self.colour=colour
        self.i=i
        self.j=j
        self.movesMade=0
        
    def setPieceCode(self,piececode):
        self.pieceCode=piececode
        
    def getPieceCode(self):
        return self.pieceCode
    
    def move(self,newi,newj):
        #if newi and newj in range
            self.i=newi
            self.j=newj
            self.movesMade +=1
    #The following 2 check functions run through the chessboard in each direction until the distance is exhausted,
    #or a piece is in the way, giving a relevant list of coordinates
    def checkMoves(self,range_list,a,b,distance,chessboard):
        for k in range (1,1+distance):
            if isInChessBoard((self.i+a*k,self.j+b*k)):
                pieceCode = chessboard[self.i+a*k][self.j+b*k].getPieceCode()
                if (pieceCode == "none"):
                    range_list.append((self.i+a*k,self.j+b*k))
                else:
                    infoList = pieceCode.split('_')
                    if(infoList[1]!=self.colour):
                        range_list.append((self.i+a*k,self.j+b*k))
                        break
                    else:
                        break
        return range_list
    
    def checkAttacks(self,a,b,distance,chessboard):
        range_list=[]
        for k in range (1,1+distance):
            
            if isInChessBoard((self.i+a*k,self.j+b*k)):
                pieceCode = chessboard[self.i+a*k][self.j+b*k].getPieceCode()
                if (pieceCode == "none"):
                    range_list.append((self.i+a*k,self.j+b*k))
                else:
                    range_list.append((self.i+a*k,self.j+b*k))
                    break
        return range_list
    
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range, done inside each piece.
        return []
            
            
class Knight(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='knight'
        self.pieceCode=self.name+'_'+self.colour
        
    def attackRange(self,chessboard):
        rangelist=[]
        rangelist.append((self.i+1,self.j+2))
        rangelist.append((self.i+1,self.j-2))
        rangelist.append((self.i+2,self.j+1))
        rangelist.append((self.i+2,self.j-1))
        rangelist.append((self.i-1,self.j+2))
        rangelist.append((self.i-1,self.j-2))
        rangelist.append((self.i-2,self.j+1))
        rangelist.append((self.i-2,self.j-1))
        
        range_in_board=list(filter(isInChessBoard,rangelist))
                
        return range_in_board
        
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range.
        attack_range=self.attackRange(chessboard)
        valid_range=[]
        info_list=[]
        for x in attack_range:
            pieceCode=chessboard[x[0]][x[1]].piece.getPieceCode()
            if pieceCode=='none':
                valid_range.append(x)
            else:
                info_list=pieceCode.split('_')
                if info_list[1]!=self.colour:
                    valid_range.append(x)
                
        return valid_range
    
    
            
                  
class Pawn(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='pawn'
        self.pieceCode=self.name+'_'+self.colour
        self.movesMade=0
        self.previous_position=(i,j)
        
    def updatePreviousPosition(self,i,j):
        self.previous_position=(i,j)
        
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range.
        valid_range=[]
        distance=1
        if self.movesMade==0:
            distance=2
        if self.colour=='white':
            valid_range=valid_range+self.checkPawnMoves(valid_range,-1,0,distance,chessboard)
            valid_range=valid_range+self.checkPawnMoves(valid_range,-1,1,1,chessboard)
            valid_range=valid_range+self.checkPawnMoves(valid_range,-1,-1,1,chessboard)
        else:
            valid_range=valid_range+self.checkPawnMoves(valid_range,1,0,distance,chessboard)
            valid_range=valid_range+self.checkPawnMoves(valid_range,1,-1,1,chessboard)
            valid_range=valid_range+self.checkPawnMoves(valid_range,1,1,1,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        return range_in_board
        
    
    def checkPawnMoves(self,range_list,a,b,distance,chessboard):
        #Cases specific to pawns in determining straight and diagonal moves
        if b==0:
            #its a straight move
            for k in range (1,1+distance):
                i_coord=self.i+a*k
                j_coord=self.j+b*k
                if isInChessBoard((i_coord,j_coord)):
                    pieceCode = chessboard[i_coord][j_coord].piece.getPieceCode()
                    if (pieceCode == "none"):
                        range_list.append((i_coord,j_coord))
                    else:
                         break
                
            
        else:
            #its a diagonal move
            for k in range (1,1+distance):
                i_coord=self.i+a*k
                j_coord=self.j+b*k
                if isInChessBoard((i_coord,j_coord)):
                    pieceCode = chessboard[i_coord][j_coord].piece.getPieceCode()
                    #en passant:
                    if self.colour=='white':
                        rank5=3
                        adjustment=1
                        difference_needed=2
                    else:
                        rank5=4
                        adjustment=-1
                        difference_needed=-2
                    neighbour_piececode=chessboard[i_coord+adjustment][j_coord].piece.getPieceCode()
                    if (neighbour_piececode.split('_')[0] == "pawn"):
                        previous_position=chessboard[i_coord+adjustment][j_coord].piece.previous_position
                        if self.i==rank5:
                            bsCondition=(self.i+a*k+adjustment-previous_position[0]==difference_needed)
                            if bsCondition==True:
                                range_list.append((self.i+a*k,self.j+b*k))
                                
                                #capture pawn, done in movePiece
                    if (pieceCode == "none"):
                        break
                            
                        
                    else:
                        infoList = pieceCode.split('_')
                        if(infoList[1]!=self.colour):
                            range_list.append((self.i+a*k,self.j+b*k))
                            break
                        else:
                            break
        
        return range_list
    
    def attackRange(self,chessboard):
        rangeList = []
        
        if (self.colour == "white"):
            rangeList.append((self.i-1,self.j-1))
            rangeList.append((self.i-1,self.j+1))
        
        elif(self.colour == "black"):            
            rangeList.append((self.i+1,self.j-1))
            rangeList.append((self.i+1,self.j+1))

        else:
            print("Pawn must be either black or white!!!")
            
        range_in_board = list(filter(isInChessBoard,rangeList))
        
        return range_in_board
    
    def pawnRange(self):
        #Lists where the pawn could move to, ignoring the state of the board.
        pawn_range=[]
        i=self.i
        j=self.j
        if self.colour=='white':
            adjustment=-1
        else:
            adjustment=1
        pawn_range=[(i+adjustment,j-1),(i+adjustment,j),(i+adjustment,j+1),(i+2*adjustment,j)]
        pawn_range_in_board=list(filter(isInChessBoard,pawn_range))
        return pawn_range_in_board
        
    
    
        
class Bishop(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        self.name='bishop'
        self.pieceCode=self.name+'_'+self.colour
        
    
        
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range
        valid_range=[]
        valid_range=valid_range+self.checkMoves(valid_range,1,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,-1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,-1,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        
        return range_in_board
    
    def attackRange(self,chessboard):
        valid_range=[]
        valid_range=valid_range+self.checkAttacks(1,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(1,-1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,-1,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        
        return range_in_board
        
        
        
                
                
class Rook(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='rook'
        self.pieceCode=self.name+'_'+self.colour
        
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range
        valid_range=[]
        valid_range=valid_range+self.checkMoves(valid_range,0,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,0,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,0,-1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,0,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        return range_in_board
    
    def attackRange(self,chessboard):
        valid_range=[]
        valid_range=valid_range+self.checkAttacks(0,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,0,7,chessboard)
        valid_range=valid_range+self.checkAttacks(0,-1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(1,0,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        return range_in_board
    
    
        
class Queen(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='queen'
        self.pieceCode=self.name+'_'+self.colour
        
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range
        valid_range=[]
        valid_range=valid_range+self.checkMoves(valid_range,1,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,-1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,-1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,0,1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,0,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,0,-1,7,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,0,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        return range_in_board
    
    def attackRange(self,chessboard):
        valid_range=[]
        valid_range=valid_range+self.checkAttacks(1,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(1,-1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,-1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(0,1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(-1,0,7,chessboard)
        valid_range=valid_range+self.checkAttacks(0,-1,7,chessboard)
        valid_range=valid_range+self.checkAttacks(1,0,7,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        return range_in_board
        
class King(Piece):
    def __init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='king'
        self.pieceCode=self.name+'_'+self.colour
        
    def canCastle(self,chessboard,checkboard,with_piece):
        #checks whether castling is possible
        if(self.movesMade > 0 or with_piece.movesMade > 0):
            return False
        else:
            if(with_piece.getPieceCode().split("_")[0] == "rook"):
                if(with_piece.j == 0):
                    for x in range(3):
                        if(checkboard[self.i][self.j-x]):
                            return False
                    
                    #can I castle because no pieces in the way?
                    #if(self.colour == "white"):
                    for x in range(3):
                        x+=1
                        if("none" != chessboard[self.i][self.j-x].piece.getPieceCode()):
                            return False

                elif(with_piece.j == 7):
                    for x in range(3):
                        if(checkboard[self.i][self.j+x]):
                            return False
                        
                    #can I catle because no pieces in the way?
                    #if(self.colour == "white"):
                    for x in range(2):
                        x+=1
                        if("none" != chessboard[self.i][self.j+x].piece.getPieceCode()):
                            return False
                
                else:
                    print("Castling attempt invalid, rook not at correct place!")
                    return False
                return True
            return False
                
                
    def computeRange(self,chessboard):
        #Lists where this piece can move to in the given board,
        #accounting for being blocked and its basic range
        valid_range=[]
        
        if self.movesMade==0:
            valid_range=valid_range+self.checkMoves(valid_range,0,1,2,chessboard)
            valid_range=valid_range+self.checkMoves(valid_range,0,-1,2,chessboard)
            
        valid_range=valid_range+self.checkMoves(valid_range,1,1,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,1,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,-1,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,-1,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,0,1,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,-1,0,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,1,0,1,chessboard)
        valid_range=valid_range+self.checkMoves(valid_range,0,-1,1,chessboard)
        range_in_board=list(filter(isInChessBoard,valid_range))
        actual_range=[]
        
        return valid_range
    
    def attackRange(self,chessboard):
        valid_range = []
        
        if(self.movesMade == 0):
            valid_range = self.checkMoves(valid_range,0,1,2,chessboard)
            valid_range = self.checkMoves(valid_range,0,-1,2,chessboard)
        
        valid_range = self.checkMoves(valid_range,1,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,1,-1,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,-1,1,chessboard)
        
        valid_range = self.checkMoves(valid_range,0,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,0,-1,1,chessboard)
        valid_range = self.checkMoves(valid_range,1,0,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,0,1,chessboard)
        
        range_in_board = list(filter(isInChessBoard,valid_range))
        return range_in_board
        
    def checkCheck(checkboard,i,j):
        return checkboard[i][j]
    
    def castleRange(self):
        castle_range=[]
        if self.colour=='white':
            castle_range.append((7,2))
            castle_range.append((7,6))
        else:
            castle_range.append((0,2))
            castle_range.append((0,6))
        return castle_range
            
            
        
class NonePiece(Piece):
    def _init__(self,i,j,colour):
        super().__init__(i,j,colour)
        
        self.name='nonepiece'
        self.pieceCode='none'
        self.i=i
        self.j=j
        self.colour=colour