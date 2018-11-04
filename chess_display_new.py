# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 15:29:05 2018

@author: bleat
"""
#import files and modules
from tkinter import *
from math import *
import board_model_new
from helper import *


def hasHere(i,j):
    pieceCode=board_model_new.chessboard.hasPiece(i,j)
    return pieceCode
    
def pathFromCode(pieceCode):
    path1='chess_images/'
    path=path1 + pieceCode + ".gif"
    return path

def drawChessBoard(canvas):
    for i in range(0,8):
        for j in range(0,8):
            colour = ''
            if((i+j) % 2 ==0):
                colour='white'
            else:
                colour='brown'
            canvas.create_rectangle(30+90*i,30+90*j,120+90*i,120+90*j,fill=colour)


def drawChessPieces(canvas):
    for i in range(8):
        for j in range(8):
            pieceCode=hasHere(i,j)
            if pieceCode != 'none':
                path=pathFromCode(pieceCode)
                pieceimg=PhotoImage(file=path)
                canvas.create_image(75+90*j,75+90*i,image=pieceimg)
                label = Label(image=pieceimg)
                label.image = pieceimg 
                # keep a reference of the image so the data isnt discarded when the function is called
      
                
def pixelsToModel(x,y):
    i=floor((y-30)/90)
    j=floor((x-30)/90)
    return (i,j) 
   
def moveFirst(event):
    #Bound to the left mouseclick. Highlights the position of the piece and where it can move.
    position=pixelsToModel(event.x,event.y)
    if(position[0]<8 and position[0]>=0 and position[1]<8 and position[1]>=0):
        piece=board_model_new.chessboard.board[position[0]][position[1]].piece
        piece_colour=piece.colour
        player_turn=board_model_new.chessboard.getPlayerTurn()
        
        if piece.pieceCode=='none':
            game_status['text']='Click a piece to make a move.'
        
        elif(player_turn==piece_colour):
            board_model_new.chessboard.setHighlightedField(position)
            drawChessBoard(canvas)
            #highlight piece position
            highlight=canvas.create_rectangle(30+90*position[1],30+90*position[0],120+90*position[1],120+90*position[0],fill='green')
            #highlight possible moves
            for move in board_model_new.chessboard.possibleMoves(position[0],position[1]):
                highlight=canvas.create_rectangle(30+90*move[1],30+90*move[0],120+90*move[1],120+90*move[0],fill='light green')
            drawChessPieces(canvas)
        else:
            game_status["text"]='Cannot move out of turn. It is '+player_turn+"'s turn."
    
    
def moveSecond(event):
    #Bound to right mouseclick. Moves highlighted piece to selected location inboard model if the move is valid.
    destination=pixelsToModel(event.x,event.y)
    start=board_model_new.chessboard.getHighlightedField()
    startpiece=board_model_new.chessboard.hasPiece(start[0],start[1])
    if(startpiece!='none'):
        if(start!=(8,8) and destination[0]<8 and destination[0]>=0 and destination[1]<8 and destination[1]>=0):
            i1=start[0]
            j1=start[1]
            i2=destination[0]
            j2=destination[1]
            old_board=board_model_new.chessboard.getBoard()
            
            new_board=board_model_new.chessboard.movePiece(i1,j1,i2,j2,old_board,startpiece.colour)
            board_model_new.chessboard.updateBoard(new_board,infolist[1])
            player_turn=board_model_new.chessboard.getPlayerTurn()
            if board_model_new.chessboard.kingInCheck(startpiece.colour):
                notice=player_turn+"'s king is in check!"
                game_result["text"]=notice
            else:
                game_result["text"]="Game in progress..."
            #update display
            drawChessBoard(canvas)
            drawChessPieces(canvas)
            statement="It is "+player_turn+"'s turn."
            game_status["text"]=statement
            
           
        else:
            print('out of bounds')
    board_model_new.chessboard.setHighlightedField((8,8))
    updated=board_model_new.chessboard.updateGameStatus(oppositeColour(player_turn))
    no_repetitions=True
    if board_model_new.chessboard.game_status=='3 repetitions reached. You may claim a draw now.':
        game_status['text']="It is "+player_turn+" 's turn."+" "+board_model_new.chessboard.game_status
        no_repeptitions=False
    #game over condition
    if updated and no_repetitions:
        game_result['text']=board_model_new.chessboard.game_status 
        game_status['text']="Game over!"
            
    
#root setup
root=Tk()
root.configure(background='light blue')
canvas=Canvas(root,width=780,height=780)
#canvas setup
canvas.configure(background='black')
canvas.bind('<Button-1>',moveFirst)
canvas.bind('<Button-3>',moveSecond)
  
drawChessBoard(canvas)
drawChessPieces(canvas)
game_status=Label(root,text="It is white's turn.")
game_status.pack({'side' : 'right'})

game_result=Label(root,text="Game in progress...")
game_result.pack()
canvas.pack()

    
root.mainloop()

    
