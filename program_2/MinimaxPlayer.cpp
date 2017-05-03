/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include <limits>
#include "MinimaxPlayer.h"


using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}


int MinimaxPlayer::utility(OthelloBoard* b){
    return b->count_score(b->get_p1_symbol() - b->count_score(b->get_p2_symbol()));
}


vector<OthelloBoard*> MinimaxPlayer::successors(char p_symbol, OthelloBoard* b){
    vector<OthelloBoard*> b_vector;
    int dimensions = 4;
    
    for(int i = 0; i < dimensions; i++){
        for(int j = 0; j < dimensions; j++){
            if (b->is_legal_move(i, j, p_symbol)){
                b_vector.push_back(new OthelloBoard(*b));
                b_vector.back()->play_move(i, j, symbol);
                
                b_vector.back()->set_column(i);
                b_vector.back()->set_row(j);
            }
        }
    }
    return b_vector;
}


int MinimaxPlayer::min_value(int &row, int &col, char p_symbol, OthelloBoard* b){
    vector<OthelloBoard*> b_vector;
    int min_row = 0;
    int min_col = 0;
    int min = 32767;
    
    if(p_symbol == 'X'){
        b_vector = successors('X', b);
    }
    
    if(p_symbol == 'O'){
        b_vector = successors('O', b);
    }
    
    if(b_vector.size() == 0){
        return utility(b);
    }
    
    for(int i = 0; i < b_vector.size(); i++){
        if(min_value(row, col, p_symbol, b_vector[i]) > min){
            min_row = b_vector[i]->get_row();
            min_col = b_vector[i]->get_column();
            min = min_value(row, col, p_symbol, b_vector[i]);
        }
    }
    row = min_row;
    col = min_col;
    
    return min;
}


int MinimaxPlayer::max_value(int &row, int &col, char p_symbol, OthelloBoard* b){
    vector<OthelloBoard*> b_vector;
    int max_row = 0;
    int max_col = 0;
    int max = -32767;
    
    if(p_symbol == 'X'){
        b_vector = successors('X', b);
    }
    
    if(p_symbol == 'O'){
        b_vector = successors('O', b);
    }
    
    if(b_vector.size() == 0){
        return utility(b);
    }
    
    for(int i = 0; i < b_vector.size(); i++){
        if(min_value(row, col, p_symbol, b_vector[i]) > max){
            max_row = b_vector[i]->get_row();
            max_col = b_vector[i]->get_column();
            max = min_value(row, col, p_symbol, b_vector[i]);
        }
    }
    row = max_row;
    col = max_col;
    return max;
}


void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    if (symbol == b->get_p1_symbol()){
        max_value(row, col, 'X', b);
    }
    else if (symbol == b->get_p2_symbol()){
        max_value(row, col, 'O', b);
    }
}


MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
