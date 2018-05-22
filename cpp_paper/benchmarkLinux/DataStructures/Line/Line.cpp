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
}

Line::Line(Line *original)
{
	slope = original->getSlope();
	intercept = original->getIntercept();
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
		}
	}
}

//create a line going through point with given slope
Line::Line(Point *point, double slope)
{
	assert(point != NULL);
	this->slope = slope;
	intercept = point->y - this->slope*(point->x);
}

//create a line with given slope and given intercept
Line::Line(double slope, double intercept)
{
	this->slope = slope;
	this->intercept = intercept;
}

void Line::update(Point* point1, Point* point2)
{
	assert(point1 != NULL && point2 != NULL);

	if (point1->x != point2->x)
	{
		slope = (point2->y - point1->y) / (point2->x - point1->x);
		intercept = point1->y - slope*(point1->x);
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
	return intercept;
}

void Line::setIntercept(double intercept)
{
	this->intercept = intercept;
}

double Line::getValue(double x)
{
	return slope * x + intercept;
}

Point Line::getIntersection(const Line& other)
{
	Point interPoint(intercept,0);
	if (this->slope - other.slope != 0)
	{
		interPoint.x = (other.intercept - this->intercept) / (this->slope - other.slope);
		interPoint.y = this->slope * interPoint.x + this->intercept;
	}
	return interPoint;
}

bool Line::isParallel(Line *l)
{
	return abs(this->slope - l->slope) < 0.0000000001;
}

#endif
