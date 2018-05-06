#ifndef __PCAENTRY_H
#define __PCAENTRY_H

#pragma once

struct PCAEntry
{
public:
	double m_dValue;
	bool   m_isRawData;

	PCAEntry()
	{
		m_dValue = 0;
		m_isRawData = true;
	}

	PCAEntry(double value, bool isRawData)
	{
		m_dValue = value;
		m_isRawData = isRawData;
	}

};

#endif