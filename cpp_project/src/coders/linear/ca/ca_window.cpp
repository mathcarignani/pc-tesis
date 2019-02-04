
#include "ca_window.h"

#include "math_utils.h"
#include "constants.h"
#include "assert.h"
#include <iostream>
#include "line_utils.h"

CAWindow::CAWindow(int window_size_, int error_threshold_): Window(window_size_, error_threshold_){
    createNanWindow();
    length = 0;
}

void CAWindow::createNonNanWindow(int incoming_value){
    nan_window = false;
    length = 0;
    constant_value = incoming_value;
    x_coord = 0;
    archived_value = new Point(incoming_value, x_coord);
    snapshot_value = archived_value;
    s_min = NULL;
    s_max = NULL;
}

void CAWindow::createNanWindow(){
    nan_window = true;
    length = 1;
    constant_value = Constants::NO_DATA_INT;
    // we don't use the rest of the values
}

bool CAWindow::conditionHolds(int value_delta, int value){
    int new_x_coord = x_coord + value_delta;
    Point* incoming_point = new Point(value, new_x_coord);

    if (s_min->pointIsBelow(incoming_point) || s_max->pointIsAbove(incoming_point)){
        return false;
    }

    increaseLength();
    x_coord = new_x_coord;
    snapshot_value = incoming_point;
    constant_value = value;

    Line* s_min_new = sMin(archived_value, snapshot_value, error_threshold);
    Line* s_max_new = sMax(archived_value, snapshot_value, error_threshold);
    if (s_min_new->getYProjection(snapshot_value) > s_min->getYProjection(snapshot_value)){ s_min = s_min_new; }
    if (s_max_new->getYProjection(snapshot_value) < s_max->getYProjection(snapshot_value)){ s_max = s_max_new; }

    return true;
}

void CAWindow::setWindow(int value_delta, int value){
    assert(length == 0);
    int new_x_coord = x_coord + value_delta;
    Point* incoming_point = new Point(value, new_x_coord);

    increaseLength(); // = 1
    x_coord = new_x_coord;
    snapshot_value = incoming_point;
    constant_value = value;

    s_min = sMin(archived_value, snapshot_value, error_threshold);
    s_max = sMax(archived_value, snapshot_value, error_threshold);
}

void CAWindow::increaseLength(){
    length++;
}

bool CAWindow::isFull(){
    return length == window_size;
}

bool CAWindow::isEmpty(){
    return length == 0;
}

Line* CAWindow::sMin(Point* point1, Point* point2, int error_threshold){
    Point* point_minus_threshold = new Point(point2->y - error_threshold, point2->x);
    Line* line = new Line(point1, point_minus_threshold);
    return line;
}

Line* CAWindow::sMax(Point* point1, Point* point2, int error_threshold){
    Point* point_plus_threshold = new Point(point2->y + error_threshold, point2->x);
    Line* line = new Line(point1, point_plus_threshold);
    return line;
}
