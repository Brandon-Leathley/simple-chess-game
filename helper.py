# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:39:59 2018

@author: bleat
"""

def InitialPosition(i,j):
    pieceCode='none'
    #for black pieces
    if(i==0 and (j==0 or j==7)):
        pieceCode='rook_black'
    if(i==0 and (j==1 or j==6)):
        pieceCode='knight_black'
    if(i==0 and (j==2 or j==5)):
        pieceCode='bishop_black'
    if(i==0 and (j==0 or j==7)):
        pieceCode='rook_black'
    if(i==0 and j==3):
        pieceCode='queen_black'
    if(i==0 and j==4):
        pieceCode='king_black'
    if(i==1):
        pieceCode='pawn_black'
    #for white pieces    
    if(i==7 and (j==0 or j==7)):
        pieceCode='rook_white'
    if(i==7 and (j==1 or j==6)):
        pieceCode='knight_white'
    if(i==7 and (j==2 or j==5)):
        pieceCode='bishop_white'
    if(i==7 and (j==0 or j==7)):
        pieceCode='rook_white'
    if i==7 and j==3:
        pieceCode='queen_white'
    if i==7 and j==4:
        pieceCode='king_white'
    if(i==6):
        pieceCode='pawn_white'
    
    return pieceCode
"""
def bullshitinitialposition(i,j):
    pieceCode='none'
    if i==1 and j==1:
        pieceCode='king_white'
    if i==5 and j==1:
        pieceCode='king_black'
    if i==1 and j==5:
        pieceCode='rook_white'
    if i==3 and j==3:
        pieceCode='knight_black'
    return pieceCode"""

def isInChessBoard(position):
    
    if position[0]>=0 and position[0]<8 and position[1]>=0 and position[1]<8:
        return True
    else:
        return False
    
def oppositeColour(colour):
    if colour=='white':
        return 'black'
    elif colour=='black':
        return 'white'
    else:
        print('Colour must be black or white.')
    



