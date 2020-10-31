#ifndef __Line_CPP
#define __Line_CPP

#include "../../stdafx.h"
#include "Line.h"

// Add ----> debug
//#include <crtdbg.h>
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif
// Add <---- debug


Line::Line()
{
	slope = 0;
	intercept = 0;
	p1 = NULL;
	p2 = NULL;
}

Line::Line(Line *original)
{
	slope = original->getSlope();
	intercept = original->getIntercept();
    p1 = NULL;
    p2 = NULL;
}

//create a line going through point1 and point2
Line::Line(Point* point1, Point* point2)
{
	if (point1 != NULL && point2 != NULL)
	{
		if (point1->x != point2->x)
		{
			slope = (point2->y - point1->y)/(point2->x - point1->x);
			intercept = point1->y - slope*(point1->x);
			p1 = new Point(point1->y, point1->x);
			p2 = new Point(point2->y, point2->x);
		}
	}
}

//create a line going through point with given slope
Line::Line(Point *point, double slope)
{
	assert(point != NULL);
	this->slope = slope;
	intercept = point->y - this->slope*(point->x);
    p1 = point;
    p2 = NULL;
}

//create a line with given slope and given intercept
Line::Line(double slope, double intercept)
{
	this->slope = slope;
	this->intercept = intercept;
    p1 = NULL;
    p2 = NULL;
}

void Line::update(Point* point1, Point* point2)
{
	assert(point1 != NULL && point2 != NULL);

	if (point1->x != point2->x)
	{
		slope = (point2->y - point1->y) / (point2->x - point1->x);
		intercept = point1->y - slope*(point1->x);
		p1 = new Point(point1->y, point1->x);
		p2 = new Point(point2->y, point2->x);
	}

}

void Line::update(Point *point, double slope)
{
	assert(point != NULL);

	this->slope = slope;
	intercept = point->y - this->slope*(point->x);
}

double Line::getSlope()
{
	return slope;
}

void Line::setSlope(double slope)
{
	this->slope = slope;
}

double Line::getIntercept()
{
	if (p1 != NULL && p1->x == 0) {
		return p1->y;
	}
	else if (p2 != NULL && p2->x == 0) {
		return p2->y;
	}
	return intercept;
}

void Line::setIntercept(double intercept)
{
	this->intercept = intercept;
}

double Line::getValue(double x)
{
	if (p1 != NULL && p1->x == x) {
		return p1->y;
	}
	else if (p2 != NULL && p2->x == x) {
		return p2->y;
	}
	return slope * x + intercept;
}

Point Line::getPoint1(){
	Point res(p1->y, p1->x);
	return res;
}

Point Line::getPoint2(){
	Point res(p2->y, p2->x);
    return res;
}

Point Line::getIntersection(const Line& other)
{
	Point interPoint(intercept,0);
	if (this->p1 != NULL){
		if (other.p1 != NULL &&  this->p1->x == other.p1->x && this->p1->y == other.p1->y){
			// this->p1 and other.p1 are the same point
			interPoint.x = this->p1->x;
			interPoint.y = this->p1->y;
			return interPoint;
		}
		else if (other.p2 != NULL &&  this->p1->x == other.p2->x && this->p1->y == other.p2->y){
			// this->p1 and other.p2 are the same point
			interPoint.x = this->p1->x;
			interPoint.y = this->p1->y;
			return interPoint;
		}
	}
	if (this->p2 != NULL){
		if (other.p1 != NULL &&  this->p2->x == other.p1->x && this->p2->y == other.p1->y){
			// this->p2 and other.p1 are the same point
			interPoint.x = this->p2->x;
			interPoint.y = this->p2->y;
			return interPoint;
		}
		else if (other.p2 != NULL &&  this->p2->x == other.p2->x && this->p2->y == other.p2->y){
			// this->p2 and other.p2 are the same point
			interPoint.x = this->p2->x;
			interPoint.y = this->p2->y;
			return interPoint;
		}
	}
	if (this->slope - other.slope != 0)
	{
		interPoint.x = (other.intercept - this->intercept) / (this->slope - other.slope);
		interPoint.y = this->slope * interPoint.x + this->intercept;
	}
	return interPoint;
}

// New Methods

double Line::getYProjection(Point* point){
	return getValue(point->x);
}

double Line::getYDistanceToDot(Point* point){
    // using "abs" was working in mac but causing issues in ubuntu
    double diff = point->y - getYProjection(point);
    return (diff < 0) ? -diff : diff;
}

bool Line::pointIsAbove(Point* point){
	return (point->y > getYProjection(point));
}

bool Line::pointIsBelow(Point* point) {
	return (point->y < getYProjection(point));
}

void Line::print(){
    if (p1 != NULL){
        std::cout << "Line: p1=(" << p1->x << ", " << p1->y << "), p2=(" << p2->x << ", " << p2->y << ")" << std::endl;
    }
    else{
        std::cout << "Line: y = " << slope << "*x + " << intercept << std::endl;
    }

}

#endif
