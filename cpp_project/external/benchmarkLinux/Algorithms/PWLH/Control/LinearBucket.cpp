#ifndef __LINEARBUCKET_CPP
#define __LINEARBUCKET_CPP

#include "../../../stdafx.h"
#include "LinearBucket.h"
#include <float.h>

// Add ----> A
//#include <crtdbg.h>
// Add <---- A

//Add ----> A
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif
// Add <---- A

LinearBucket::LinearBucket()
{
	esp = 1;
	polygon = new CPolygon();
}

LinearBucket::LinearBucket(double e)
{
	esp = e;
	polygon = new CPolygon();
}

LinearBucket::~LinearBucket(void)
{
	delete polygon;
}

int LinearBucket::getSize()
{
	return polygon->getSize();
}

// Purpose  : Get approximated line of this bucket
// Parameter:
//            Point &vertex1: first point
//            Point &vertex2: second point
void LinearBucket::getAproximatedLine(Point &vertex1, Point &vertex2)
{
	getAproximatedLineMOD(vertex1, vertex2, -1);
}


void LinearBucket::getAproximatedLineMOD(Point &vertex1, Point &vertex2, int x_coord) ////////////////////////////// MOD
{
    std::cout << "        LinearBucket::getAproximatedLineMOD(...) BEGIN" << std::endl;
	DynArray<Point*>* hull = polygon->getConvexHull();
	int size = hull->size();
	double minWidth = 0;
	Point* point1 = NULL;
	Point* point2 = NULL;

	//Get max distance from an any point in hull to
	//an any edge in hull
	if (size > 1)
	{
		point1 = hull->getAt(size - 1);
		point2 = hull->getAt(0);
		minWidth = getMaxDisForEdge(point1, point2);
	}

	double width = 0;
	for (int i = 1; i < size; i++)
	{
		width = getMaxDisForEdge(hull->getAt(i - 1), hull->getAt(i));
		if (fabs(width) < fabs(minWidth))
		{
			minWidth = width;
			point1 = hull->getAt(i - 1);
			point2 = hull->getAt(i);
		}
	}

	//Calculate approximated line
	if (point1 != NULL && point2 != NULL)
	{
		double haftWidth = minWidth / 2;
		Line l1(point1, point2);
		Line l2(l1.getSlope(), l1.getIntercept() + haftWidth);
		vertex1.x = 0;
		vertex1.y = l2.getValue(vertex1.x);
		if (x_coord == -1){ vertex2.x = polygon->getSize() - 1; } // original code
		else {  			vertex2.x = x_coord; } // MOD code
		vertex2.y = l2.getValue(vertex2.x);
	}
	else if( size == 1)
	{
		point1 = hull->getAt(0);
	}
}

void LinearBucket::addPoint(double value)
{
	polygon->addPoint(polygon->getSize(), value);
}

void LinearBucket::addPointMOD(double time, double value) ////////////////////////////////////////////////////////// MOD
{
    polygon->addPoint(time, value);
}

void LinearBucket::removePoint()
{
	polygon->removePoint();
}

void LinearBucket::resetBucket()
{
	delete polygon;
	polygon = new CPolygon();
}

// Check if bucket is valid with respect to error tolerance
bool LinearBucket::checkEpsConstraint()
{
	std::cout << "        LinearBucket::checkEpsConstraint() BEGIN" << std::endl;
	DynArray<Point*>* hull = polygon->getConvexHull();
	int size = hull->size();
	if (size < 2)	return true;

	double width; // = getMaxDisForEdge(hull->getAt(size - 1), hull->getAt(0));

	for (int i = 1; i < size; i++)
	{
		width = getMaxDisForEdge(hull->getAt(i - 1), hull->getAt(i));
		Point* p1 = hull->getAt(i - 1);
		Point* p2 = hull->getAt(i);
		std::cout << "            i = " << i << " - (" << p1->x << ", " << p1->y << ")<>(" << p2->x << "," << p2->y << ")  width = " << width << std::endl;
		if (fabs(width) <= (2 * esp)){
			std::cout << "            return true;" << std::endl;
			return true;
		}

	}
	std::cout << "            return false;" << std::endl;
	return false;
}

double LinearBucket::getDistance(Point *p, Line* l)
{
	double distance = p->y - l->getValue(p->x);
	return distance;
}

// Purpose  : Calculate max distance from any point in hull to 2 points
// Parameter:
//            Point* vertex1: first point
//            Point* vertex2: second point
// Return   :
//            double maxDis: max distance from any point in hull to the line created by vertex1, vertex2
double LinearBucket::getMaxDisForEdge(Point *vertex1, Point *vertex2)
{
    std::cout << "            LinearBucket::getMaxDisForEdge(...) BEGIN" << std::endl;
	Line l(vertex1, vertex2);
	DynArray<Point*>* hull = polygon->getConvexHull();
	int size = hull->size();
	double maxDis = 0;
	double distance = 0;

	int max_i = 0;
	for (int i = 0; i < size; i++)
	{
		distance = getDistance(hull->getAt(i), &l);
		if (fabs(distance) > fabs(maxDis)){
			max_i = i;
			maxDis = distance;
		}

	}
	Point* p = hull->getAt(max_i);
	std::cout << "            max_point = (" << p->x << ", " << p->y << ")" << std::endl;
	return maxDis;
}

#endif
