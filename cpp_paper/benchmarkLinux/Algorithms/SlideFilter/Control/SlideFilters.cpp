#ifndef __SLIDEFILTERS_CPP
#define __SLIDEFILTERS_CPP

#include "../../../stdafx.h"
#include "stdio.h"
#include "stdlib.h"
#include "math.h"
#include "../../../DataStructures/Line/Line.h"
#include "SlideFilters.h"

// Add ----> A
//#include <crtdbg.h>
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif
// Add <---- A

SlideFilters::SlideFilters(SlideFiltersInput* data)
{
	m_pSFData = data;
	m_pSFOutput = new SlideFiltersOutput(m_pSFData);
	m_nBegin_Point = 0;
}

SlideFilters::~SlideFilters()
{
	delete m_pSFData;
	delete m_pSFOutput;
}

SlideFiltersOutput* SlideFilters::getOutput()
{
	return m_pSFOutput;
}

// compress raw data
void SlideFilters::compress()
{
	int inputSize = m_pSFData->getDataLength();
	if (inputSize == 1)
	{
		DataItem item = m_pSFData->getAt(0);
		SlideFiltersEntry recording(item.value, item.timestamp, true);
		m_pSFOutput->getCompressData()->add(recording);
		m_nBegin_Point = 1;
		return;
	}

	// Initialize upper bound and lower bound
	double eps = m_pSFData->getEsp();
	DataItem item1 = m_pSFData->getAt(0);
	DataItem item2 = m_pSFData->getAt(1);
	initializeU_L(item1.timestamp, item1.value, item2.timestamp, item2.value, eps);

	//Read the input
	double upperValue, lowerValue;
	DataItem item;
	for (int i = 2; i <= inputSize; i++)
	{
		//Read if it is not the end of the input
		if (i < inputSize)
		{
			item = m_pSFData->getAt(i);
			upperValue = m_curU.getValue(item.timestamp);
			lowerValue = m_curL.getValue(item.timestamp);
		}

		//recording mechanism
		if ((i == inputSize) || (item.value - upperValue > eps) || (lowerValue - item.value > eps))
		{
			recording_mechanism(i);
		}
		else //filtering mechanism
		{
			filtering_mechanism(i);
		}
	}
}

// Initialize upper bound and lower bound
void SlideFilters::initializeU_L(double t1, double v1, double t2, double v2, double eps)
{
	Point top1(v1 + eps, t1);
	Point bottom1(v1 - eps, t1);
	Point top2(v2 + eps, t2);
	Point bottom2(v2- eps, t2);
	m_curL.update(&top1, &bottom2);
	m_curU.update(&bottom1, &top2);
}

// Update upper bound and lower bound
bool SlideFilters::updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG)
{
	if (m_nBegin_Point ==0)
		return false;

	Point ul = curU.getIntersection(&curL);
	DataItem preItem= m_pSFData->getAt(m_nBegin_Point - 1);
	DataItem firstItem = m_pSFData->getAt(m_nBegin_Point);

	// Compute alpha, beta
	Point alpha(prevG.getValue(preItem.timestamp), preItem.timestamp);
	Point beta(prevG.getValue(firstItem.timestamp), firstItem.timestamp);
	Line alpha_ul(&ul,&alpha);
	Line beta_ul(&ul, &beta);

	double minSlope, maxSlope;
	if (alpha_ul.getSlope() < beta_ul.getSlope())
	{
		minSlope = alpha_ul.getSlope();
		maxSlope = beta_ul.getSlope();
	}
	else
	{
		maxSlope = alpha_ul.getSlope();
		minSlope = beta_ul.getSlope();
	}

	// Check whether current segment is connected with previous 'prevG'
	bool isConnected = false;
	if (minSlope < curU.getSlope() && maxSlope > curL.getSlope())
	{
		Point ul = curU.getIntersection(&curL);
		isConnected = true;

		// Update bounds
		if (maxSlope < curU.getSlope())
		{
			curU.update(&ul,maxSlope);
		}
		if (minSlope > curL.getSlope())
		{
			curL.update(&ul,minSlope);
		}
	}

	return isConnected;
}

// Find the fittest line in range of lower bound and upper bound
Line SlideFilters::getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL)
{
	Point ul = curU.getIntersection(curL);
	double numberator = 0;
	double denominator = 0;

	for (int j = beginPoint + 1; j < endPoint;  j++)
	{
		DataItem item = m_pSFData->getAt(j);
		numberator += (item.value - ul.y) * (item.timestamp - ul.x);
		denominator += (item.timestamp - ul.x) * (item.timestamp - ul.x);
	}

	double fraction = numberator / denominator;
	double slopeU = curU.getSlope();
	double slopeL = curL.getSlope();

	// Get fittest slope in range of lower and upper bounds
	double fittestSlope = fraction > slopeU ? slopeU : fraction;
	fittestSlope = fittestSlope > slopeL ? fittestSlope : slopeL;

	// Create fittest line
	Line fittestLine;
	fittestLine.setSlope(fittestSlope);
	fittestLine.setIntercept(ul.y - (fittestSlope * ul.x));
	return fittestLine;
}

// Generate line segments for the filtering intervals and update the latest-executed point
void SlideFilters::recording_mechanism(int& position)
{
	int inputSize = m_pSFData->getDataLength();
	bool existInter = false;
	Point ul = m_curU.getIntersection(m_curL);
	DataItem begin_curSeg = m_pSFData->getAt(m_nBegin_Point);

	existInter = updateUandLforConnectedSegment(m_curU,m_curL,m_prevG);
	m_curG = getFittestLine_G(m_nBegin_Point, position, m_curU, m_curL);

	if (m_nBegin_Point == 0)
	{
		//Create first recording
		double t = begin_curSeg.timestamp;
        SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t , true);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t , true));
        m_pSFOutput->getCompressData()->add(*sfe);
	}
	else if (existInter)
	{
		//m_curG cut m_prevG at valid section
		Point inter = m_curG.getIntersection(m_prevG);
		SlideFiltersEntry recording(inter, existInter);
		m_pSFOutput->getCompressData()->add(recording);
	}
	else
	{
		//m_curG cut m_prevG at invalid section
		DataItem end_prevSeg = m_pSFData->getAt(m_nBegin_Point - 1);
		double t = end_prevSeg.timestamp;
        SlideFiltersEntry* sfe = &SlideFiltersEntry(m_prevG.getValue(t), t, existInter);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_prevG.getValue(t), t, existInter));
        m_pSFOutput->getCompressData()->add(*sfe);
		t = begin_curSeg.timestamp;
        sfe = &SlideFiltersEntry(m_curG.getValue(t), t, true);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, true));
         m_pSFOutput->getCompressData()->add(*sfe);
	}

	if (position < inputSize -1)
	{
		//Create new interval by two points
		m_nBegin_Point = position;
		DataItem curItem = m_pSFData->getAt(position);
		position++;
		DataItem nextItem = m_pSFData->getAt(position);
		double eps = m_pSFData->getEsp();
		initializeU_L(curItem.timestamp, curItem.value, nextItem.timestamp, nextItem.value, eps);
		m_prevG = m_curG;
	}
	//if last interval has only one point --> Create last recording and finish compressing
	else if (position == (inputSize - 1))
	{
		m_nBegin_Point = position;
		DataItem preItem = m_pSFData->getAt(m_nBegin_Point - 1);
		DataItem item = m_pSFData->getAt(position);
		double t = preItem.timestamp;
		SlideFiltersEntry(m_curG.getValue(t), t, true);
        SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t, true);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, true));
        m_pSFOutput->getCompressData()->add(*sfe);
        sfe = &SlideFiltersEntry(item.value, item.timestamp, false);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(item.value, item.timestamp, false));
        m_pSFOutput->getCompressData()->add(*sfe);
		position++;
	}
	//position == inputSize --> Create last recording
	else
	{
		DataItem item = m_pSFData->getAt(position - 1);
		double t = item.timestamp;
        SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t, false);
		//m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, false));
        m_pSFOutput->getCompressData()->add(*sfe);
	}
}

// Adjust upper bound and lower bound with the arrival of each new data point at 'position'
void SlideFilters::filtering_mechanism(int position)
{
	DataItem item = m_pSFData->getAt(position);
	double upperValue = m_curU.getValue(item.timestamp);
	double lowerValue = m_curL.getValue(item.timestamp);
	int j;

	double eps = m_pSFData->getEsp();
	Point top(item.value + eps, item.timestamp);
	Point bottom(item.value - eps, item.timestamp);
	DataItem tmpItem;

	//item is above L a distance which is larger than epsilon
	if (item.value - lowerValue > eps)
	{
		//Update L
		for (j = m_nBegin_Point; j < position; j++)
		{
			tmpItem = m_pSFData->getAt(j);
			Point tmpTop(tmpItem.value + eps, tmpItem.timestamp);
			Line tmpL(&tmpTop, &bottom);

			if (tmpL.getSlope() > m_curL.getSlope())
			{
				m_curL.setSlope(tmpL.getSlope());
				m_curL.setIntercept(tmpL.getIntercept());
			}
		}
	}

	//item is under U a distance which is larger than epsilon
	if (upperValue - item.value > eps)
	{
		//Update U
		for (j = m_nBegin_Point; j < position; j++)
		{
			tmpItem = m_pSFData->getAt(j);
			Point tmpBottom(tmpItem.value - eps, tmpItem.timestamp);
			Line tmpU(&tmpBottom, &top);

			if (tmpU.getSlope() < m_curU.getSlope())
			{
				m_curU.setSlope(tmpU.getSlope());
				m_curU.setIntercept(tmpU.getIntercept());
			}
		}
	}
}

#endif